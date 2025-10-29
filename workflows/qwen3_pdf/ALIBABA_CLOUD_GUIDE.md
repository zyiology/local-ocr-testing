# Alibaba Cloud Provider Guide

## Overview

The Alibaba Cloud provider enables you to use Qwen-VL models via Alibaba Cloud's DashScope API, eliminating the need for local GPU resources. It uses the OpenAI-compatible API endpoint for easy integration.

## Prerequisites

1. **Alibaba Cloud Account**: You need an active Alibaba Cloud account
2. **API Key**: Obtain from [Model Studio](https://www.alibabacloud.com/help/en/model-studio/get-api-key)
3. **Credits/Billing**: Ensure you have credits or billing set up for API usage

## Setup

### 1. Install Dependencies

The `openai` package is required for the Alibaba Cloud provider:

```powershell
cd workflows/qwen3_pdf
uv sync
```

This will automatically install all required dependencies including `openai>=1.0.0`.

### 2. Configure API Key

Set your DashScope API key as an environment variable:

**PowerShell (Session-specific)**:
```powershell
$env:DASHSCOPE_API_KEY = "sk-your-api-key-here"
```

**PowerShell (Persistent - User level)**:
```powershell
[System.Environment]::SetEnvironmentVariable('DASHSCOPE_API_KEY', 'sk-your-api-key-here', 'User')
```

**Linux/Mac**:
```bash
export DASHSCOPE_API_KEY="sk-your-api-key-here"
```

### 3. Configure the Provider

Edit `config.py`:

```python
# Provider selection
DEFAULT_PROVIDER = "alibaba_cloud"  # Change from "local" to "alibaba_cloud"

# Alibaba Cloud configuration
ALIBABA_MODEL = "qwen-vl-max-latest"  # Or "qwen-vl-plus"
ALIBABA_REGION = "singapore"  # Or "beijing"
ALIBABA_MAX_TOKENS = 1024  # Maximum response length
ALIBABA_TEMPERATURE = 0.1  # Lower = more deterministic
```

## Available Models

| Model | Description | Best For |
|-------|-------------|----------|
| `qwen-vl-max-latest` | Latest VL Max model | Highest quality OCR, complex documents |
| `qwen-vl-plus` | VL Plus model | Balanced quality and speed |
| `qwen-vl-max` | Specific VL Max version | Stable version for production |

## Region Selection

Choose the region closest to you for lower latency:

- **Singapore** (`singapore`): International users, Southeast Asia
  - Endpoint: `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
  
- **Beijing** (`beijing`): China mainland users
  - Endpoint: `https://dashscope.aliyuncs.com/compatible-mode/v1`

**Important**: API keys are region-specific. Use the correct key for your selected region.

## Usage

### Basic Usage

With default configuration in `config.py`:

```powershell
.venv\Scripts\python.exe pdf_workflow.py
```

### Override Provider via CLI

```powershell
# Use Alibaba Cloud regardless of config.py setting
.venv\Scripts\python.exe pdf_workflow.py --provider alibaba_cloud

# Use local model regardless of config.py setting
.venv\Scripts\python.exe pdf_workflow.py --provider local
```

### Full Example

```powershell
# Process PDFs from custom folder using Alibaba Cloud API
.venv\Scripts\python.exe pdf_workflow.py `
    --provider alibaba_cloud `
    --pdf-folder "C:\MyDocuments\PDFs" `
    --output-folder "C:\MyDocuments\OCR_Results"
```

## Configuration Parameters

### Model Settings

```python
ALIBABA_MODEL = "qwen-vl-max-latest"
```
- Choose from available models (see table above)
- Different models have different pricing

### Region

```python
ALIBABA_REGION = "singapore"  # or "beijing"
```
- Determines API endpoint
- Affects latency and API key compatibility

### Max Tokens

```python
ALIBABA_MAX_TOKENS = 1024
```
- Maximum tokens in the response
- Higher values = longer responses but higher cost
- Typical range: 512-2048

### Temperature

```python
ALIBABA_TEMPERATURE = 0.1
```
- Controls randomness in responses
- Range: 0.0 to 2.0
- Lower (0.0-0.3): More deterministic, better for OCR
- Higher (0.7-1.0): More creative, for content generation

## Cost Considerations

- API calls are billed per token (input + output)
- Check current pricing at [Alibaba Cloud Model Studio Pricing](https://www.alibabacloud.com/help/en/model-studio/billing)
- Monitor your usage in the DashScope console
- Consider using `qwen-vl-plus` for lower costs

## Troubleshooting

### "DASHSCOPE_API_KEY environment variable not set"

**Solution**: Set the environment variable as shown in Setup step 2.

### "Invalid region: ..."

**Solution**: Ensure `ALIBABA_REGION` is either `"singapore"` or `"beijing"` (lowercase).

### API Key Authentication Errors

**Solutions**:
1. Verify your API key is correct
2. Check that you're using the right key for your region
3. Ensure your account has credits or billing set up

### Rate Limiting Errors

**Solutions**:
1. Add delays between requests (modify `pdf_workflow.py`)
2. Use a lower-tier model
3. Contact Alibaba Cloud support to increase limits

### Connection Errors

**Solutions**:
1. Check your internet connection
2. Verify you can access the API endpoint URL
3. Check if there are any firewall/proxy restrictions

## Advantages vs Local Models

| Aspect | Alibaba Cloud | Local Models |
|--------|---------------|--------------|
| **GPU Required** | No | Yes (8-80GB VRAM) |
| **Setup Time** | Minutes | Hours |
| **Cost** | Pay per use | Hardware investment |
| **Scalability** | Unlimited | Limited by hardware |
| **Latency** | Network dependent | Immediate |
| **Privacy** | Data sent to cloud | Data stays local |

## API Documentation

For more details, see the official documentation:
- [Qwen API Reference](https://www.alibabacloud.com/help/en/model-studio/use-qwen-by-calling-api)
- [OpenAI Compatible Mode](https://www.alibabacloud.com/help/en/model-studio/use-qwen-by-calling-api#section-openai-compatible)
- [Getting API Keys](https://www.alibabacloud.com/help/en/model-studio/get-api-key)

## Example Configuration

Here's a complete `config.py` setup for Alibaba Cloud:

```python
"""Configuration settings for the PDF OCR workflow."""

from pathlib import Path

# Provider selection
DEFAULT_PROVIDER = "alibaba_cloud"

# Local model configuration (unused when using alibaba_cloud)
DEFAULT_MODEL = "Qwen/Qwen3-VL-30B-A3B-Instruct"
USE_MOE = True

# Alibaba Cloud configuration
ALIBABA_MODEL = "qwen-vl-max-latest"
ALIBABA_REGION = "singapore"
ALIBABA_MAX_TOKENS = 1024
ALIBABA_TEMPERATURE = 0.1

# Default paths
DEFAULT_PDF_FOLDER = Path(__file__).parent / "../../data/pdfs"
DEFAULT_OUTPUT_FOLDER = Path(__file__).parent / "../../data/output"

# Image conversion settings
TARGET_LONGEST_SIDE = 1800

# Default prompt for OCR extraction
DEFAULT_PROMPT = """There is a table in this image. I've extracted the row headers as a csv:

```
RFID Tag No. / Security Label No.,,
Identification no. of cube,Cube Mark,
,Lab Ref. No.,
Mould no.,,
Condition on received*,,
Edges/corners damaged**,,
Dimensions,W1 - width 1,mm
,W2 - height,
,W3 - width 2,
Mass,as received,kg
,saturated in air,
,in water,
Density***,by calculation,kg/m3
,by water-displacement,
Maximum load at failure kN,,
Compressive strength**** MPa,,
Type of fracture*****,,
```

Can you help me extract the data columns? You don't have to repeat the row headers again, just extract the data columns. You can ignore the rest of the document as well. Thanks!"""
```
