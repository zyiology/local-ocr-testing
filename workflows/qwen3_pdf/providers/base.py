"""Abstract base class for OCR providers."""

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Abstract base class for all OCR providers.
    
    This defines the interface that all provider implementations must follow.
    """

    @abstractmethod
    def process_image(self, image_path: str, prompt: str) -> str:
        """Process a single image with the given prompt.
        
        Args:
            image_path: Path to the image file to process
            prompt: The prompt/instruction for the OCR model
            
        Returns:
            The extracted text from the image
        """
        pass
