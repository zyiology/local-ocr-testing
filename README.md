# Local OCR Testing

## Overall Instructions

1. Each folder, e.g. deepseek-ocr, qwen3, contains a setup to run given LLMs locally for OCR testing.
2. Ensure you have `uv` installed. On Windows, run in powershell `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"` to install. Refer to https://docs.astral.sh/uv/getting-started/installation/ for more info
3. Make sure you know the following
- CUDA version installed (should be something like 11.8, 12.4, 12.8). Run `nvidia-smi` to check.
- GPU architecture (e.g. Nvidia 5xxx series GPUs are Blackwell, 4xxx series are Ada, etc)
- You may run into incompatibilities depending on the above... Currently, recommended to use Ada/Hopper GPUs if you don't want to troubleshoot incompatibilities.

## General Setup Instructions

To setup the Python environment for a given LLM
1. `cd` to the target folder
2. Run `uv sync` to install the packages
3. A `.venv` folder should be created with all the packages
4. While terminal is in that folder, run `.venv\Scripts\python.exe main.py` to run the main script

There may be more instructions depending on the given LLM, please read the README.md in the respective folder before doing the above steps.

# Flash Attention

You may notice the commented-out lines, e.g. ` # attn_implementation="flash_attention_2"`, in the scripts.
Flash Attention is a package that can increase the RAM efficiency and speed of the model, but requires installing the correct version for the existing version of PyTorch/CUDA.

You can install the package from https://github.com/mjun0812/flash-attention-prebuild-wheels/
e.g. to get flash-attn v2.8.3, for my environment using CUDA 12.4, PyTorch 2.6 and Python 3.12, run `uv pip install https://github.com/mjun0812/flash-attention-prebuild-wheels/releases/download/v0.4.11/flash_attn-2.8.3+cu124torch2.6-cp312-cp312-linux_x86_64.whl`
If successfully installed, you can uncomment the line to use flash attention
