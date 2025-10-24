# DeepSeek-OCR Experiment

> **Note**: This is a simple experiment for testing DeepSeek-OCR on single images.

## Overview

A minimal script to test the DeepSeek-OCR model for document OCR, free-form OCR, and figure parsing.

## Requirements

- **Minimum CUDA version**: 11.8
- **Package versions**: See notes below

## Package Version Notes

DeepSeek-OCR officially recommends:
- `torch==2.6.0`
- `transformers==4.46.3`
- `tokenizers==0.20.3`

However, these versions are **not compatible** with newer CUDA versions like 12.8.

**Solution**: If using newer CUDA, replace `==` with `>=` in `pyproject.toml` before running `uv sync`. This allows newer compatible versions to be installed.

## Configuration

Edit `main.py` to adjust:
- `image_file`: Path to your test image
- `output_path`: Where to save results
- `prompt`: OCR instruction mode
- Image processing parameters (see below)

### OCR Modes (Prompts)

DeepSeek-OCR supports different prompts for different tasks:

| Task | Prompt |
|------|--------|
| **Documents** | `<image>\n<\|grounding\|>Convert the document to markdown.` |
| **General OCR** | `<image>\n<\|grounding\|>OCR this image.` |
| **Free OCR (no layout)** | `<image>\nFree OCR.` |
| **Figures in documents** | `<image>\nParse the figure.` |
| **Image description** | `<image>\nDescribe this image in detail.` |
| **Text location** | `<image>\nLocate <\|ref\|>xxxx<\|/ref\|> in the image.` |

**Note**: Escape the pipe character as `<\|` when using in code.

### Image Processing Modes

Configure `base_size`, `image_size`, and `crop_mode`:

| Mode | base_size | image_size | crop_mode | VRAM Usage |
|------|-----------|------------|-----------|------------|
| **Tiny** | 512 | 512 | False | Lowest |
| **Small** | 640 | 640 | False | Low |
| **Base** | 1024 | 1024 | False | Medium |
| **Large** | 1280 | 1280 | False | High |
| **Gundam** | 1024 | 640 | True | Medium |

**General rule**: Larger sizes = better results but more GPU memory required.

## Usage

1. **Install dependencies**:
   ```powershell
   uv sync
   ```
   
   If using newer CUDA, edit `pyproject.toml` first (change `==` to `>=`).

2. **Edit `main.py`**:
   ```python
   image_file = "your_image.jpg"  # Your test image
   output_path = "your/output/dir"  # Where to save results
   prompt = "<image>\n<|grounding|>Convert the document to markdown."
   ```

3. **Run the script**:
   ```powershell
   .venv\Scripts\python.exe main.py
   ```

## Output

Results are saved to the specified `output_path` with:
- Extracted text/markdown
- Layout information (if grounding mode used)
- Debug visualizations (if enabled)
