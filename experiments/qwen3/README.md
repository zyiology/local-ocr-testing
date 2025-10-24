# Qwen3-VL Basic Experiment

> **Note**: This is a simple experiment for testing Qwen3-VL models on single images. For batch PDF processing, see `../../workflows/qwen3_pdf/`.

## Overview

A minimal script to test Qwen3-VL vision-language models on individual images. Useful for quick model evaluation and prompt experimentation.

## Requirements

- **Minimum CUDA version**: 11.8
- **VRAM**: See model requirements below

## Configuration

Edit `main.py` to adjust:
- Image file path
- Model selection
- Prompt customization

### Available Models

| Model | VRAM Required |
|-------|---------------|
| `Qwen/Qwen3-VL-2B-Instruct` | 8GB |
| `Qwen/Qwen3-VL-4B-Instruct` | 16GB |
| `Qwen/Qwen3-VL-8B-Instruct` | 2GB |
| `Qwen/Qwen3-VL-30B-A3B-Instruct` | 80GB |

**Default**: The script is configured to run `Qwen/Qwen3-VL-2B-Instruct`.

To change the model, edit the model name in `main.py`:
```python
model = Qwen3VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen3-VL-2B-Instruct",  # Change this line
    dtype="auto",
    device_map="auto",
)
```

## Usage

1. **Install dependencies**:
   ```powershell
   uv sync
   ```

2. **Place your test image** in the same directory or specify a path

3. **Edit `main.py`**:
   - Update `image` value in the `messages` content to your image path
   - Customize the `prompt` as needed

4. **Run the script**:
   ```powershell
   .venv\Scripts\python.exe main.py
   ```

## Example Use Cases

- Testing table extraction prompts
- Evaluating OCR accuracy on sample images
- Comparing different model sizes
- Prototyping custom prompts for specific tasks


