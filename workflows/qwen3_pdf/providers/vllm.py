"""VLLM provider for locally hosted vision-language models."""

from typing import Optional

from .openai_compatible import OpenAICompatibleProvider


class VLLMProvider(OpenAICompatibleProvider):
    """Provider for VLLM-hosted models via OpenAI-compatible API.

    Thin wrapper around OpenAICompatibleProvider for VLLM servers.
    VLLM exposes an OpenAI-compatible API endpoint that this provider uses.

    VLLM typically doesn't require an API key for local deployments.

    Documentation: https://docs.vllm.ai/en/latest/
    """

    def __init__(
        self,
        model_name: str,
        host: str = "localhost",
        port: int = 8000,
        api_key: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.1,
    ):
        """Initialize the VLLM provider.

        Args:
            model_name: Model identifier as configured in VLLM server
            host: Hostname or IP address where VLLM server is running
            port: Port number for the VLLM server
            api_key: API key if VLLM server requires authentication (default: "dummy")
            max_tokens: Maximum tokens to generate in response
            temperature: Sampling temperature (0.0 to 2.0)
        """
        # Construct base URL from host and port
        base_url = f"http://{host}:{port}/v1"

        # Use "dummy" as default API key for local VLLM servers
        resolved_api_key = api_key or "dummy"

        # Initialize the parent OpenAI-compatible provider
        super().__init__(
            base_url=base_url,
            api_key=resolved_api_key,
            model_name=model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            provider_name=f"VLLM ({host}:{port})",
        )
