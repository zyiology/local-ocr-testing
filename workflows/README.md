# Workflows

This folder contains more complete demo workflows that showcase end-to-end OCR processing pipelines. Unlike the simple experiments, these workflows include proper architecture, batch processing, and utilities.

## Purpose

These workflows are designed to:
- Demonstrate production-ready patterns and architecture
- Process multiple files in batch operations
- Include helper utilities (converters, viewers, validators)
- Serve as templates for building actual applications

## Available Workflows

### Qwen3 PDF Batch Processing
**Location**: `qwen3_pdf/`

A complete workflow for batch processing multiple PDFs with Qwen3-VL models. Includes PDF-to-image conversion, OCR extraction, and a GUI viewer for browsing results.

**Features**:
- Batch PDF processing with automatic conversion
- Configurable DPI and image sizing
- Multiple Qwen3-VL model support (2B to 30B)
- GUI viewer for reviewing results
- Flash Attention 2 support (Linux only)

**Components**:
- `pdf_workflow.py` - Main batch processing script
- `converter.py` - PDF to image conversion utilities
- `viewer.py` - Tkinter-based GUI for browsing OCR results

**Usage**:
```powershell
cd qwen3_pdf
uv sync

# Process PDFs (place PDFs in ../../data/pdfs/)
.venv\Scripts\python.exe pdf_workflow.py

# View results
.venv\Scripts\python.exe viewer.py
```

See `qwen3_pdf/README.md` for detailed configuration and model options.

---

## Key Differences from Experiments

| Aspect | Experiments | Workflows |
|--------|-------------|-----------|
| **Scope** | Single image testing | Batch processing pipelines |
| **Structure** | Single script | Multiple modules |
| **Purpose** | Quick evaluation | Demo of complete systems |
| **Architecture** | Minimal | Proper separation of concerns |
| **Utilities** | None | Converters, viewers, validators |

## General Pattern

Workflows typically include:
1. **Main script** - Orchestrates the entire pipeline
2. **Utility modules** - Reusable functions (conversion, processing)
3. **Helper tools** - Viewers, validators, analyzers
4. **Configuration** - Clear model and path settings
5. **Documentation** - Detailed usage instructions

## Notes

- Workflows are still demos, not production-ready applications
- For actual production use, consider creating a separate repository with proper:
  - Testing framework
  - Error handling and logging
  - Configuration management
  - API/GUI architecture
  - Deployment setup
