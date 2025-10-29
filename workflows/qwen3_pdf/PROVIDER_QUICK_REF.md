# Quick Provider Reference

## TL;DR - How to Switch Providers

### Option 1: Edit config.py (Persistent)
```python
DEFAULT_PROVIDER = "alibaba_cloud"  # or "local"
```

### Option 2: Use CLI Flag (One-time)
```powershell
.venv\Scripts\python.exe pdf_workflow.py --provider alibaba_cloud
# or
.venv\Scripts\python.exe pdf_workflow.py --provider local
```

---

## Local Provider

**When to use**: You have a GPU with sufficient VRAM

**Setup**:
1. `uv sync` (one time)
2. Edit `config.py`:
   ```python
   DEFAULT_PROVIDER = "local"
   DEFAULT_MODEL = "Qwen/Qwen3-VL-30B-A3B-Instruct"  # or smaller model
   USE_MOE = True  # False for non-MoE models
   ```

**Requirements**:
- GPU with 8-80GB VRAM (model dependent)
- CUDA 11.8+
- Sufficient disk space for model weights

**Pros**:
- ✅ Data stays local (privacy)
- ✅ No API costs
- ✅ No network latency
- ✅ Unlimited usage

**Cons**:
- ❌ Expensive GPU hardware required
- ❌ Long initial model download
- ❌ Slower on weak GPUs

---

## Alibaba Cloud Provider

**When to use**: No GPU, or want to try without hardware investment

**Setup**:
1. `uv sync` (one time)
2. Get API key: https://www.alibabacloud.com/help/en/model-studio/get-api-key
3. Set environment variable:
   ```powershell
   $env:DASHSCOPE_API_KEY = "sk-your-key"
   ```
4. Edit `config.py`:
   ```python
   DEFAULT_PROVIDER = "alibaba_cloud"
   ALIBABA_MODEL = "qwen-vl-max-latest"
   ALIBABA_REGION = "singapore"  # or "beijing"
   ```

**Requirements**:
- Internet connection
- Alibaba Cloud account with API access
- Credits or billing setup

**Pros**:
- ✅ No GPU needed
- ✅ Fast setup (minutes)
- ✅ Scalable
- ✅ Always latest models

**Cons**:
- ❌ Pay per use
- ❌ Data sent to cloud
- ❌ Network latency
- ❌ Requires internet

---

## Configuration Cheat Sheet

### config.py - Local
```python
DEFAULT_PROVIDER = "local"
DEFAULT_MODEL = "Qwen/Qwen3-VL-2B-Instruct"  # Start small!
USE_MOE = False
```

### config.py - Alibaba Cloud
```python
DEFAULT_PROVIDER = "alibaba_cloud"
ALIBABA_MODEL = "qwen-vl-max-latest"
ALIBABA_REGION = "singapore"
ALIBABA_MAX_TOKENS = 1024
ALIBABA_TEMPERATURE = 0.1
```

---

## Model Selection Quick Reference

### Local Models
| Model | VRAM | Speed | Quality |
|-------|------|-------|---------|
| 2B | 8GB | ⚡⚡⚡ | ⭐⭐ |
| 4B | 16GB | ⚡⚡ | ⭐⭐⭐ |
| 8B | 32GB | ⚡ | ⭐⭐⭐⭐ |
| 30B | 80GB | 🐌 | ⭐⭐⭐⭐⭐ |

### Cloud Models
| Model | Cost | Speed | Quality |
|-------|------|-------|---------|
| qwen-vl-plus | $ | ⚡⚡ | ⭐⭐⭐⭐ |
| qwen-vl-max-latest | $$ | ⚡ | ⭐⭐⭐⭐⭐ |

---

## Common Commands

```powershell
# Run with default settings
.venv\Scripts\python.exe pdf_workflow.py

# Override provider
.venv\Scripts\python.exe pdf_workflow.py --provider local
.venv\Scripts\python.exe pdf_workflow.py --provider alibaba_cloud

# Custom folders + provider
.venv\Scripts\python.exe pdf_workflow.py `
    --provider alibaba_cloud `
    --pdf-folder C:\path\to\pdfs `
    --output-folder C:\path\to\output

# View results
.venv\Scripts\python.exe viewer.py
```

---

## Troubleshooting

### Local Provider
```
Out of Memory → Use smaller model (2B/4B)
Slow processing → Reduce TARGET_LONGEST_SIDE in config.py
Model won't load → Check CUDA version, GPU VRAM
```

### Alibaba Cloud Provider
```
API key error → Check DASHSCOPE_API_KEY environment variable
Region error → Set ALIBABA_REGION to "singapore" or "beijing"
Rate limit → Add delays, reduce batch size
Network error → Check internet, firewall settings
```

---

## Environment Variable Setup

### PowerShell (Session)
```powershell
$env:DASHSCOPE_API_KEY = "sk-your-key"
```

### PowerShell (Persistent)
```powershell
[System.Environment]::SetEnvironmentVariable('DASHSCOPE_API_KEY', 'sk-your-key', 'User')
```

### Linux/Mac
```bash
export DASHSCOPE_API_KEY="sk-your-key"
# Add to ~/.bashrc or ~/.zshrc for persistence
```

---

## Cost Comparison

**Local**: High upfront (GPU hardware), zero ongoing
**Cloud**: Low/zero upfront, pay per document

**Break-even**: ~1000-5000 documents depending on GPU cost and API pricing

See: https://www.alibabacloud.com/help/en/model-studio/billing
