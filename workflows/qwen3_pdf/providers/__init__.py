"""Provider modules for OCR processing."""

from .base import BaseProvider
from .local import LocalProvider
from .openai_compatible import OpenAICompatibleProvider
from .alibaba_cloud import AlibabaCloudProvider
from .vllm import VLLMProvider

__all__ = [
    "BaseProvider",
    "LocalProvider",
    "OpenAICompatibleProvider",
    "AlibabaCloudProvider",
    "VLLMProvider",
]
