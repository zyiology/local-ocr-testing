# Experiments

This folder contains simple, single-purpose scripts for testing different OCR models on individual images. Each experiment is self-contained with its own dependencies and virtual environment.

## Purpose

These experiments are designed for:
- Quick model evaluation and comparison
- Testing model capabilities on sample images
- Prototyping prompts and configurations
- Learning how to use different OCR models

## Available Experiments

### DeepSeek-OCR
**Location**: `deepseek-ocr/`

Tests the DeepSeek-OCR model for document and image OCR tasks.

**Features**:
- Multiple OCR modes (document, free OCR, figure parsing)
- Configurable image sizes and cropping
- Grounding support for precise text localization

**Usage**:
```powershell
cd deepseek-ocr
uv sync
.venv\Scripts\python.exe main.py
```

See `deepseek-ocr/README.md` for detailed configuration options.

---

### Qwen3-VL Basic
**Location**: `qwen3/`

Basic single-image testing with Qwen3-VL vision-language models.

**Features**:
- Multiple model sizes (2B, 4B, 8B, 30B)
- Custom prompts for table extraction
- Simple image-to-text pipeline

**Usage**:
```powershell
cd qwen3
uv sync
.venv\Scripts\python.exe main.py
```

See `qwen3/README.md` for model options and VRAM requirements.

---

## General Setup

All experiments follow the same pattern:

1. Navigate to the experiment folder
2. Run `uv sync` to install dependencies
3. Edit `main.py` to configure paths and prompts
4. Run `.venv\Scripts\python.exe main.py`

## Notes

- Each experiment has its own `pyproject.toml` and isolated virtual environment
- Read the individual README in each folder for model-specific requirements
- These are intentionally simple - for production workflows, see `../workflows/`
