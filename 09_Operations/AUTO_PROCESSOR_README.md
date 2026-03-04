# AegisLab Auto-Processor

**Purpose:** Monitors `10_Input` and automatically triggers AI agents when new files appear.

---

## Quick Start

1. **Install dependency:** `pip install watchdog`
2. **Start:** Double-click `09_Operations/Start_Auto_Processor.bat`
3. **Upload:** Drag files into `10_Input` folder
4. **Results:** Check `11_Results` for deliverables

---

## How It Works

```
10_Input (new file) → Auto-Processor detects → run_agent_cli.py (Agent 02) → 11_Results
```

- **Supported formats:** .pdf, .docx, .txt, .md, .xlsx, .pptx, .json
- **Default agent:** Agent 02 (Applied Research Methodologist), Daily Driver template
- **Output:** `11_Results/{filename}_deliverable.md`

---

## Customize

Edit `aegislab_auto_processor.py` to change:
- `--agent` (1–11)
- `--template-type` (Daily Driver, Deep Dive, Review/QA)
- Output path pattern

---

## Requirements

- Python 3.10+
- `watchdog` package
- `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` in repo root `.env`
