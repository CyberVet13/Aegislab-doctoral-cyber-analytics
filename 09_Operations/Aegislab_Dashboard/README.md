# AegisLab Dashboard

**Purpose:** Customer-facing UI to kick off the agentic AI environment. Florida Gators themed.

**Repo:** https://github.com/CyberVet13/Aegislab-doctoral-cyber-analytics/tree/branch02132026

---

## How to Access

1. **Double-click** `Launch_Dashboard.bat` — opens `aegislab-dashboard.html` in your default browser
2. **Or** open `aegislab-dashboard.html` directly in Chrome, Edge, or Firefox

---

## Features

- **Repository Management** — Cursor IDE integration, GitHub links, Quick Configuration
- **Course Management** — 3-step workflow: Upload (10_Input) → Auto-Process → Results (11_Results)
- **Research Workflow Progress** — Visual progress tracking
- **Agent Control Panel** — All 11 AegisLab agents
- **Activity Log** — Real-time feedback

---

## Workflow

1. Click **Start Auto-Processor** (opens 09_Operations folder — double-click `Start_Auto_Processor.bat`)
2. Drag course documents into **10_Input** folder
3. AI agents process automatically (Agent 02 Applied Research Methodologist)
4. **Review Queue:** Approve deliverables in Streamlit or Gradio before committee-ready
5. Get approved deliverables from **11_Results** folder

**Note:** Dashboard and Auto-Processor use Agent 02 only. For full agent choice, use Streamlit Run Agent. See [Human_in_the_Loop_Map.md](../Human_in_the_Loop_Map.md).

**Requires:** `pip install watchdog` (auto-installed by Start_Auto_Processor.bat)

See [AUTO_PROCESSOR_README.md](../AUTO_PROCESSOR_README.md) for auto-processor details.

---

## Files

| File | Purpose |
|------|---------|
| `aegislab-dashboard.html` | Main dashboard (standalone, no server) |
| `Launch_Dashboard.bat` | Opens dashboard in browser |
| `README.md` | This file |
