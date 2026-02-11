# 10_Input — Workflow trigger

**Purpose:** Placing information here **kicks off the process**. Add prompts, briefs, or context files; then use the Streamlit **Run Agent** page to load that content and start the agent workflow.

**How it works:**
1. **Place** a file in `10_Input/` (`.md`, `.txt`, or `.json`). This is your workflow trigger.
2. Open **Run Agent** (Streamlit → http://localhost:8501 → Run Agent).
3. Under **Load context from 10_Input**, select the file and click **Load into context**. The file content fills the research objective / context field.
4. Choose agent, template, output path, and **Run agent**. The process runs; output is logged and queued for PI review; completed deliverables go to **11_Results/** after approval.

**Usage:**
- Add markdown notes, outlines, or task descriptions that agents will use as input.
- Reference files in `05_Data/` or `03_Research_Methods/` inside your brief when needed.
- Optionally keep a copy of the staged brief here for audit (e.g. `10_Input/YYYY-MM-DD_Agent02_brief.md`).

**Governance:** Inputs that lead to committee-facing outputs should be traceable; session logs in `09_Operations/Session_Logs/` record prompt summaries and output paths. No PII in committed input files without governance approval.

**Last updated:** 2025-02-07
