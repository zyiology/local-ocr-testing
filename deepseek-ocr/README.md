# Configuration
Minimum CUDA version = 11.8

deepseek-ocr recommends using torch==2.6.0, transformers==4.46.3, tokenizers==0.20.3
However, these are not supported on newer CUDA versions, like 12.8. You can use newer versions of these packages instead. Replace the `--` with `>=` instead before you run `uv sync`.

Read main.py to adjust file paths.
