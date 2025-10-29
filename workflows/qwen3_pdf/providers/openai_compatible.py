"""Generic OpenAI-compatible API provider for OCR processing."""

import base64
from pathlib import Path

from openai import OpenAI

from .base import BaseProvider


class OpenAICompatibleProvider(BaseProvider):
    """Generic provider for any OpenAI-compatible API endpoint.

    This provider can work with any service that implements the OpenAI API format,
    including:
    - Alibaba Cloud DashScope
    - VLLM
    - Together.ai
    - Azure OpenAI
    - And many others

    The provider handles image encoding and API communication in a standardized way.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        model_name: str,
        max_tokens: int = 1024,
        temperature: float = 0.1,
        provider_name: str = "OpenAI-Compatible",
    ):
        """Initialize the OpenAI-compatible provider.

        Args:
            base_url: Base URL for the API endpoint (e.g., "https://api.openai.com/v1")
            api_key: API key for authentication (use "dummy" for services that don't require one)
            model_name: Model identifier to use
            max_tokens: Maximum tokens to generate in response
            temperature: Sampling temperature (0.0 to 2.0)
            provider_name: Human-readable name for logging purposes
        """
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.provider_name = provider_name

        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        print(f"{self.provider_name} initialized")
        print(f"  Model: {self.model_name}")
        print(f"  Base URL: {self.base_url}")

    def _encode_image_base64(self, image_path: str) -> str:
        """Encode image file to base64 string.

        Args:
            image_path: Path to the image file

        Returns:
            Base64-encoded image string
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def _get_image_mime_type(self, image_path: str) -> str:
        """Determine MIME type from image file extension.

        Args:
            image_path: Path to the image file

        Returns:
            MIME type string (e.g., "image/png", "image/jpeg")
        """
        suffix = Path(image_path).suffix.lower()
        mime_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        return mime_types.get(suffix, "image/png")

    def process_image(self, image_path: str, prompt: str) -> str:
        """Process a single image with the OpenAI-compatible API.

        Args:
            image_path: Path to the image file to process
            prompt: The prompt/instruction for the OCR model

        Returns:
            The extracted text from the image
        """
        # Encode image to base64
        base64_image = self._encode_image_base64(image_path)
        mime_type = self._get_image_mime_type(image_path)

        # Construct image URL in data URI format
        image_url = f"data:{mime_type};base64,{base64_image}"

        # Create messages in OpenAI format
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ]

        # Call the API
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,  # type: ignore
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            # Extract the response text
            result = response.choices[0].message.content
            if result is None:
                raise RuntimeError("API returned empty response")
            print(result)
            return result

        except Exception as e:
            error_msg = f"Error calling {self.provider_name} API: {str(e)}"
            print(error_msg)
            raise RuntimeError(error_msg) from e
