"""Local Transformers-based OCR provider."""

import importlib.util
from typing import Any

from transformers import (
    AutoProcessor,
    Qwen3VLForConditionalGeneration,
    Qwen3VLMoeForConditionalGeneration,
)

from .base import BaseProvider


class LocalProvider(BaseProvider):
    """Provider for local Qwen3-VL models using Transformers."""

    def __init__(self, model_name: str, use_moe: bool = False):
        """Initialize the local provider with a specific model.
        
        Args:
            model_name: Hugging Face model identifier (e.g., "Qwen/Qwen3-VL-30B-A3B-Instruct")
            use_moe: Whether to use the MoE model variant
        """
        self.model_name = model_name
        self.use_moe = use_moe
        
        # Check if Flash Attention 2 is available
        self.use_flash_attn = self._check_flash_attention_available()
        
        # Initialize model and processor
        self.model = self._load_model()
        self.processor = AutoProcessor.from_pretrained(self.model_name)
        
        print(f"LocalProvider initialized with model: {self.model_name}")
        if self.use_flash_attn:
            print("Using Flash Attention 2 for optimized performance")
    
    def _check_flash_attention_available(self) -> bool:
        """Check if Flash Attention 2 is available on the system.
        
        Returns:
            bool: True if flash_attn is installed and available, False otherwise.
        """
        is_available = importlib.util.find_spec("flash_attn") is not None
        if is_available:
            print("Flash Attention 2 detected - using optimized attention implementation")
        else:
            print("Flash Attention 2 not available - using default 'eager' implementation")
        return is_available
    
    def _load_model(self) -> Any:
        """Load the Qwen3-VL model with appropriate settings.
        
        Returns:
            The loaded model instance
        """
        # Configure model loading based on Flash Attention availability
        attn_implementation = "flash_attention_2" if self.use_flash_attn else "eager"
        dtype = "bfloat16" if self.use_flash_attn else "auto"
        
        model_kwargs = {
            "dtype": dtype,
            "device_map": "auto",
            "attn_implementation": attn_implementation,
        }
        
        # Load the appropriate model variant
        if self.use_moe:
            model = Qwen3VLMoeForConditionalGeneration.from_pretrained(
                self.model_name,
                **model_kwargs,  # type: ignore
            )
        else:
            model = Qwen3VLForConditionalGeneration.from_pretrained(
                self.model_name,
                **model_kwargs,  # type: ignore
            )
        
        print("Model loaded successfully")
        return model
    
    def process_image(self, image_path: str, prompt: str) -> str:
        """Process a single image with the Qwen3-VL model.
        
        Args:
            image_path: Path to the image file to process
            prompt: The prompt/instruction for the OCR model
            
        Returns:
            The extracted text from the image
        """
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": image_path,
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ]
        
        # Preparation for inference
        inputs = self.processor.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt",
        )
        inputs = inputs.to(self.model.device)
        
        # Inference: Generation of the output
        generated_ids = self.model.generate(**inputs, max_new_tokens=1024)
        generated_ids_trimmed = [
            out_ids[len(in_ids) :]
            for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = self.processor.batch_decode(
            generated_ids_trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )
        
        result = output_text[0]
        print(result)
        return result
