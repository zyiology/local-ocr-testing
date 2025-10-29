"""Configuration settings for the PDF OCR workflow."""

from pathlib import Path

# Provider selection
DEFAULT_PROVIDER = "local"  # Options: "local", "alibaba_cloud", "vllm"

# Local model configuration
DEFAULT_MODEL = "Qwen/Qwen3-VL-30B-A3B-Instruct"
USE_MOE = True  # Set to True if using the MoE model variant

# Alibaba Cloud configuration
ALIBABA_MODEL = "qwen3-vl-30b-a3b"  # Options: "qwen3-vl-30b-a3b", "qwen3-vl-235b"
ALIBABA_REGION = "singapore"  # Options: "singapore", "beijing"
ALIBABA_MAX_TOKENS = 1024
ALIBABA_TEMPERATURE = 0.1

# VLLM configuration
VLLM_MODEL = "Qwen/Qwen3-VL-30B-A3B-Instruct"  # Model name as configured in VLLM server
VLLM_HOST = "localhost"  # Hostname or IP address
VLLM_PORT = 8000  # Port number
VLLM_MAX_TOKENS = 1024
VLLM_TEMPERATURE = 0.1

# Default paths
DEFAULT_PDF_FOLDER = Path(__file__).parent / "../../data/pdfs"
DEFAULT_OUTPUT_FOLDER = Path(__file__).parent / "../../data/output"

# Image conversion settings
TARGET_LONGEST_SIDE = 1800  # Target resolution for PDF conversion

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
