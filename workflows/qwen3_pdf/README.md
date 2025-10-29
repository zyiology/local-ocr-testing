# Qwen3 PDF Batch Processing Workflow

A complete workflow for batch processing PDFs with Qwen3-VL vision-language models. Converts PDFs to images, runs OCR extraction, and provides a GUI viewer for reviewing results.

## Overview

This workflow demonstrates:
- **PDF to Image Conversion**: Automatic conversion with configurable DPI
- **Batch OCR Processing**: Process multiple PDFs in one run
- **Table Extraction**: Specialized prompts for extracting tabular data
- **Result Viewing**: Tkinter-based GUI for browsing extracted text

## Requirements

- **Minimum CUDA version**: 11.8
- **VRAM**: Depends on model choice (see below)

## Architecture

The workflow uses a provider pattern for clean separation of concerns:

```
workflows/qwen3_pdf/
├── pdf_workflow.py       # Main orchestrator
├── config.py             # Configuration settings
├── converter.py          # PDF utilities
├── viewer.py             # GUI viewer
└── providers/            # OCR provider implementations
    ├── __init__.py
    ├── base.py           # Abstract base class
    ├── local.py          # Local Transformers provider
    └── alibaba_cloud.py  # Alibaba Cloud API provider
```

### Components

#### 1. `pdf_workflow.py`
Main script that orchestrates the batch processing pipeline.

**What it does**:
1. Initializes the OCR provider (local model)
2. Scans a folder for PDF files
3. Converts each PDF page to high-resolution images
4. Processes each image with the provider
5. Saves extracted text alongside images

#### 2. `config.py`
Centralized configuration for the workflow.

**Settings**:
- Model: `DEFAULT_MODEL = "Qwen/Qwen3-VL-30B-A3B-Instruct"`
- Target image size: `TARGET_LONGEST_SIDE = 1800`
- Default paths: `DEFAULT_PDF_FOLDER`, `DEFAULT_OUTPUT_FOLDER`
- OCR prompt: `DEFAULT_PROMPT`

#### 3. `providers/`
Provider implementations following a common interface.

**`base.py`**: Abstract base class defining the `process_image()` interface

**`local.py`**: Local Transformers-based provider
- Automatic Flash Attention detection
- Model loading with optimal settings
- Image processing with Qwen3-VL

**`alibaba_cloud.py`**: Alibaba Cloud DashScope API provider
- Uses OpenAI-compatible API endpoint
- Requires DASHSCOPE_API_KEY environment variable
- Supports Singapore and Beijing regions
- No local GPU required

#### 4. `converter.py`
Utility functions for PDF manipulation using PyMuPDF.

**Functions**:
- `pdf_to_images()`: Convert PDF pages to PIL Images
- `save_images()`: Save images to disk
- `get_pdf_page_size()`: Get PDF dimensions for DPI calculation

#### 5. `viewer.py`
GUI application for browsing OCR results.

**Features**:
- Side-by-side image and text display
- Keyboard navigation (arrow keys, Page Up/Down)
- Automatic folder scanning
- Scrollable text view

## Available Models

### Local Models (via Transformers)

Edit `DEFAULT_MODEL` in `config.py` to choose:

| Model | VRAM Required | MOE Setting |
|-------|---------------|-------------|
| `Qwen/Qwen3-VL-2B-Instruct` | 8GB | `MOE = False` |
| `Qwen/Qwen3-VL-4B-Instruct` | 16GB | `MOE = False` |
| `Qwen/Qwen3-VL-8B-Instruct` | 32GB | `MOE = False` |
| `Qwen/Qwen3-VL-30B-A3B-Instruct` | 80GB | `MOE = True` |

**Note**: Set `MOE = True` for Mixture-of-Experts models (30B-A3B), `False` for standard models.

### Cloud Models (via Alibaba Cloud DashScope)

Edit `ALIBABA_MODEL` in `config.py` to choose:

| Model | Description |
|-------|-------------|
| `qwen-vl-max-latest` | Latest VL Max model (best quality) |
| `qwen-vl-plus` | VL Plus model (balanced) |
| `qwen-vl-max` | Specific VL Max version |

**Regions**: `singapore` or `beijing` (set via `ALIBABA_REGION` in `config.py`)

## Setup & Usage

### 1. Install Dependencies
```powershell
cd workflows/qwen3_pdf
uv sync
```

### 2. Prepare Your PDFs
Place PDF files in `../../data/pdfs/` (relative to this workflow folder)

The default structure is:
```
local-ocr-testing/
├── workflows/qwen3_pdf/      # You are here
├── data/
│   ├── pdfs/                 # Put your PDFs here
│   └── output/               # Results will be saved here
```

### 3. Configure the Workflow

#### For Local Models

Edit `config.py` to customize settings:
```python
DEFAULT_PROVIDER = "local"
DEFAULT_MODEL = "Qwen/Qwen3-VL-30B-A3B-Instruct"  # Change to your preferred model
USE_MOE = True  # Set to False for non-MoE models
TARGET_LONGEST_SIDE = 1800  # Adjust image resolution
DEFAULT_PROMPT = "..."  # Customize the OCR extraction prompt
```

#### For Alibaba Cloud API

1. Get your API key from [Alibaba Cloud Model Studio](https://www.alibabacloud.com/help/en/model-studio/get-api-key)

2. Set the environment variable:
```powershell
$env:DASHSCOPE_API_KEY = "sk-your-api-key-here"
```

3. Edit `config.py`:
```python
DEFAULT_PROVIDER = "alibaba_cloud"
ALIBABA_MODEL = "qwen-vl-max-latest"  # Or "qwen-vl-plus"
ALIBABA_REGION = "singapore"  # Or "beijing"
ALIBABA_MAX_TOKENS = 1024
ALIBABA_TEMPERATURE = 0.1
```

### 4. Run the Workflow

**Using default provider** (configured in `config.py`):
```powershell
.venv\Scripts\python.exe pdf_workflow.py
```

**Specify provider via command line**:
```powershell
# Use local model
.venv\Scripts\python.exe pdf_workflow.py --provider local

# Use Alibaba Cloud API
.venv\Scripts\python.exe pdf_workflow.py --provider alibaba_cloud
```

**Custom paths**:
```powershell
# Custom PDF folder
.venv\Scripts\python.exe pdf_workflow.py --pdf-folder C:\path\to\pdfs

# Custom output folder
.venv\Scripts\python.exe pdf_workflow.py --output-folder C:\path\to\output

# All options combined
.venv\Scripts\python.exe pdf_workflow.py --provider alibaba_cloud --pdf-folder C:\pdfs --output-folder C:\output
```

Results will be saved to the output folder in subdirectories named after each PDF.

### 5. View Results

**Basic usage** (uses default path `../../data/output/`):
```powershell
.venv\Scripts\python.exe viewer.py
```

**Custom path**:
```powershell
.venv\Scripts\python.exe viewer.py C:\path\to\output
```

**Viewer Controls**:
- `→` / `Page Down`: Next folder
- `←` / `Page Up`: Previous folder
- `Esc` / `Q`: Quit

## Advanced: Flash Attention 2

Flash Attention 2 can improve memory efficiency and speed.

**Requirements**:
- Linux only (not available on Windows)
- Must match your CUDA/PyTorch versions exactly

**Installation**:
See https://github.com/mjun0812/flash-attention-prebuild-wheels/

Example:
```bash
uv pip install https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/download/v0.4.11/flash_attn-2.8.3+cu124torch2.6-cp312-cp312-linux_x86_64.whl
```

After installation, Flash Attention will be automatically detected and used.

## Customization Tips

### Change Input/Output Locations
You can specify custom paths using command-line arguments:

**pdf_workflow.py**:
```powershell
# See all options
.venv\Scripts\python.exe pdf_workflow.py --help

# Use custom folders
.venv\Scripts\python.exe pdf_workflow.py --pdf-folder <path> --output-folder <path>
```

**viewer.py**:
```powershell
# See all options
.venv\Scripts\python.exe viewer.py --help

# View custom output folder
.venv\Scripts\python.exe viewer.py <path-to-output>
```

### Adjust Image Resolution
Edit `config.py`:
```python
TARGET_LONGEST_SIDE = 1800  # Increase for higher quality (slower processing)
```

### Modify Extraction Prompt
Edit `DEFAULT_PROMPT` in `config.py` to change what gets extracted.

## Troubleshooting

**Out of Memory Error**:
- Use a smaller model (2B or 4B)
- Reduce `target_longest_side` in `pdf_workflow.py`

**Model Download Issues**:
- Ensure you have a HuggingFace account and token (for gated models)
- Check your internet connection
- Models are cached in `~/.cache/huggingface/`

**No PDFs Found**:
- Verify PDFs are in the correct folder
- Check the `pdf_folder_path` parameter in `main()`

**Viewer Shows No Folders**:
- Ensure PDFs have been processed (run `pdf_workflow.py` first)
- Check that `image0.png` and `image0.txt` exist in output folders
- Update `output_dir` path in `viewer.py` if needed
