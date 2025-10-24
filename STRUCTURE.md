# Repository Structure

Quick reference for navigating the local-ocr-testing repository.

```
local-ocr-testing/
│
├── README.md                    # Main documentation (start here)
├── AGENTS.md                    # Development guidelines for AI agents
├── .gitignore                   # Git ignore rules (excludes data/, .venv/, etc.)
│
├── experiments/                 # Simple single-image tests
│   ├── README.md               # Overview of experiments
│   │
│   ├── deepseek-ocr/           # DeepSeek-OCR testing
│   │   ├── main.py
│   │   ├── pyproject.toml
│   │   ├── README.md
│   │   └── .venv/
│   │
│   └── qwen3/                  # Qwen3-VL basic testing  
│       ├── main.py
│       ├── pyproject.toml
│       ├── README.md
│       └── .venv/
│
├── workflows/                   # Complete demo workflows
│   ├── README.md               # Overview of workflows
│   │
│   └── qwen3_pdf/              # PDF batch processing workflow
│       ├── pdf_workflow.py     # Main processing script
│       ├── converter.py        # PDF conversion utilities
│       ├── viewer.py           # GUI for viewing results
│       ├── pyproject.toml
│       ├── README.md
│       └── .venv/
│
└── data/                        # Data files (git-ignored)
    ├── pdfs/                   # Input PDF files
    └── output/                 # OCR results
        └── [pdf_name]/
            ├── image0.png
            ├── image0.txt
            └── ...
```

## Quick Navigation

### I want to...

**Test a model on a single image**
→ Go to `experiments/` and pick a model

**Process multiple PDFs**
→ Go to `workflows/qwen3_pdf/`

**See what models are available**
→ Check `experiments/README.md`

**Find sample output**
→ Look in `data/output/` (created after running workflows)

**Understand the project**
→ Start with the main `README.md`

**Follow coding standards**
→ See `AGENTS.md`

## Notes

- Each experiment/workflow has its own virtual environment (`.venv/`)
- All experiments and workflows are self-contained
- Dependencies are managed per-folder with `pyproject.toml`
- The `data/` folder is excluded from git to keep the repo lightweight
