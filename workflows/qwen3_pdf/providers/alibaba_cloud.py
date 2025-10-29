"""Alibaba Cloud (DashScope) OCR provider using OpenAI-compatible API."""

import os
from typing import Optional

from .openai_compatible import OpenAICompatibleProvider


class AlibabaCloudProvider(OpenAICompatibleProvider):
    """Provider for Alibaba Cloud Qwen-VL models via OpenAI-compatible API.

    Thin wrapper around OpenAICompatibleProvider that handles Alibaba Cloud
    specific configuration (region-based URLs and API key management).

    Requires DASHSCOPE_API_KEY environment variable to be set.

    Documentation: https://www.alibabacloud.com/help/en/model-studio/use-qwen-by-calling-api
    """

    def __init__(
        self,
        model_name: str = "qwen-vl-max-latest",
        region: str = "singapore",
        api_key: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.1,
    ):
        """Initialize the Alibaba Cloud provider.

        Args:
            model_name: Model identifier (e.g., "qwen-vl-max-latest", "qwen-vl-plus")
            region: Either "singapore" or "beijing" (determines base URL)
            api_key: API key for DashScope. If None, reads from DASHSCOPE_API_KEY env var
            max_tokens: Maximum tokens to generate in response
            temperature: Sampling temperature (0.0 to 2.0)
        """
        # Get API key from parameter or environment
        resolved_api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not resolved_api_key:
            raise ValueError(
                "DASHSCOPE_API_KEY environment variable not set. "
                "Please set it or pass api_key parameter. "
                "Get your API key from: https://www.alibabacloud.com/help/en/model-studio/get-api-key"
            )

        # Set base URL based on region
        region_lower = region.lower()
        if region_lower == "singapore":
            base_url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
        elif region_lower == "beijing":
            base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        else:
            raise ValueError(
                f"Invalid region: {region}. Must be 'singapore' or 'beijing'"
            )

        # Initialize the parent OpenAI-compatible provider
        super().__init__(
            base_url=base_url,
            api_key=resolved_api_key,
            model_name=model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            provider_name=f"Alibaba Cloud ({region})",
        )
