# Local OCR Testing

A repository for experimenting with various LLM-based OCR solutions running locally. Contains both simple single-image experiments and more complete batch processing workflows.

## Repository Structure

- **`experiments/`** - Quick tests of different LLM models on single images
  - `deepseek-ocr/` - DeepSeek-OCR model testing
  - `qwen3/` - Qwen3-VL basic functionality testing
- **`workflows/`** - More complete demo workflows for specific use cases
  - `qwen3_pdf/` - Batch PDF processing with Qwen3-VL models
- **`data/`** - Input files and output results (git-ignored)

## Prerequisites

Before running any experiments or workflows, ensure you have:

1. **`uv` package manager** installed:
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
   See https://docs.astral.sh/uv/getting-started/installation/ for more info.

2. **System requirements**:
   - **CUDA version**: Run `nvidia-smi` to check (should be 11.8, 12.4, or 12.8)
   - **GPU architecture**: Nvidia 4xxx series (Ada/Hopper) or 3xxx series (Ampere) recommended
   - **Note**: Blackwell (5xxx series) may have compatibility issues with older PyTorch versions, will require tweaking pyproject.toml

## Quick Start

### Running Experiments

Simple single-image tests to evaluate different models:

1. Navigate to an experiment folder:
   ```powershell
   cd experiments/qwen3
   # or
   cd experiments/deepseek-ocr
   ```

2. Install dependencies and run:
   ```powershell
   uv sync
   .venv\Scripts\python.exe main.py
   ```

See individual experiment READMEs for model-specific configuration.

### Running Workflows

More complete demos for batch processing:

1. Navigate to a workflow folder:
   ```powershell
   cd workflows/qwen3_pdf
   ```

2. Install dependencies:
   ```powershell
   uv sync
   ```

3. Run the workflow:
   ```powershell
   .venv\Scripts\python.exe pdf_workflow.py
   ```

4. View results with the GUI viewer:
   ```powershell
   .venv\Scripts\python.exe viewer.py
   ```

See individual workflow READMEs for detailed usage instructions.

## Flash Attention

You may notice the commented-out lines, e.g. ` # attn_implementation="flash_attention_2"`, in the scripts.
Flash Attention is a package that can increase the RAM efficiency and speed of the model, but requires installing the correct version for the existing version of PyTorch/CUDA.

ONLY works on Linux
ONLY add this if you are comfortable with the package management, any issues can be more complicated to resolve.

You can install the package from https://github.com/mjun0812/flash-attention-prebuild-wheels/
e.g. to get flash-attn v2.8.3, for my environment using CUDA 12.4, PyTorch 2.6 and Python 3.12, run `uv pip install https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/download/v0.4.11/flash_attn-2.8.3+cu124torch2.6-cp312-cp312-linux_x86_64.whl`
If successfully installed, you can uncomment the line to use flash attention
