# OCR Providers

This directory contains provider implementations for different OCR backends.

## Architecture

The provider architecture follows a hierarchical design pattern:

```
BaseProvider (Abstract)
├── LocalProvider (Transformers-based)
└── OpenAICompatibleProvider (Generic OpenAI API)
    ├── AlibabaCloudProvider
    └── VLLMProvider
```

### Base Classes

- **`BaseProvider`**: Abstract base class defining the provider interface
- **`OpenAICompatibleProvider`**: Generic provider for any OpenAI-compatible API endpoint

### Concrete Providers

- **`LocalProvider`**: Runs models locally using Hugging Face Transformers
- **`AlibabaCloudProvider`**: Uses Alibaba Cloud DashScope API (thin wrapper around `OpenAICompatibleProvider`)
- **`VLLMProvider`**: Connects to local VLLM server (thin wrapper around `OpenAICompatibleProvider`)

## Usage

### Local Provider

```python
from providers import LocalProvider

provider = LocalProvider(
    model_name="Qwen/Qwen3-VL-30B-A3B-Instruct",
    use_moe=True
)
result = provider.process_image("image.png", "Extract text from this image")
```

### Alibaba Cloud Provider

Requires `DASHSCOPE_API_KEY` environment variable.

```python
from providers import AlibabaCloudProvider

provider = AlibabaCloudProvider(
    model_name="qwen3-vl-30b-a3b",
    region="singapore",  # or "beijing"
    max_tokens=1024,
    temperature=0.1
)
result = provider.process_image("image.png", "Extract text from this image")
```

### VLLM Provider

```python
from providers import VLLMProvider

provider = VLLMProvider(
    model_name="Qwen/Qwen3-VL-30B-A3B-Instruct",
    host="localhost",
    port=8000,
    max_tokens=1024,
    temperature=0.1
)
result = provider.process_image("image.png", "Extract text from this image")
```

### Generic OpenAI-Compatible Provider

For other OpenAI-compatible services (Together.ai, Azure OpenAI, etc.):

```python
from providers import OpenAICompatibleProvider

provider = OpenAICompatibleProvider(
    base_url="https://api.service.com/v1",
    api_key="your-api-key",
    model_name="model-name",
    max_tokens=1024,
    temperature=0.1,
    provider_name="Custom Provider"  # For logging
)
result = provider.process_image("image.png", "Extract text from this image")
```

## Adding New Providers

### For OpenAI-Compatible APIs

If the service uses OpenAI's API format, create a thin wrapper:

```python
from .openai_compatible import OpenAICompatibleProvider

class NewProvider(OpenAICompatibleProvider):
    def __init__(self, **kwargs):
        # Handle provider-specific configuration
        base_url = self._configure_base_url(**kwargs)
        api_key = self._get_api_key(**kwargs)
        
        super().__init__(
            base_url=base_url,
            api_key=api_key,
            model_name=kwargs.get("model_name"),
            provider_name="New Provider"
        )
```

### For Custom APIs

Extend `BaseProvider` and implement the `process_image` method:

```python
from .base import BaseProvider

class CustomProvider(BaseProvider):
    def process_image(self, image_path: str, prompt: str) -> str:
        # Your custom implementation
        pass
```

## Design Benefits

1. **Code Reuse**: All OpenAI-compatible providers share the same implementation
2. **Easy Maintenance**: Bug fixes in `OpenAICompatibleProvider` benefit all child classes
3. **Extensibility**: Easy to add new providers (just configure the base URL and API key)
4. **Consistency**: Same behavior across all OpenAI-format providers
5. **Type Safety**: Proper type hints and error handling throughout
