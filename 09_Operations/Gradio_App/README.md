# AegisLab Gradio — Workflow Manager

**Purpose:** Manage the AegisLab workflow with Gradio: **10_Input** (trigger) → Run Agent → Review Queue → Session Logs. Uses the same backend as the Streamlit app (`aegislab_ui` in `09_Operations/Streamlit_App/`).

**Location:** `09_Operations/Gradio_App/`

---

## How to run

1. **Terminal:** Open PowerShell or Command Prompt.
2. **Go to app folder:**
   ```bash
   cd "09_Operations\Gradio_App"
   ```
   Or full path:
   ```bash
   cd "C:\Users\kelvi\OneDrive - cybervetssolutions.com\AegisLab\09_Operations\Gradio_App"
   ```
3. **Install dependencies (first time only):**
   ```bash
   pip install -r requirements.txt
   ```
4. **API keys:** Same as Streamlit — `.env` at **repo root** (`AegisLab`) with `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`.
5. **Start the app:**
   - Double-click **`Launch_Gradio_UI.bat`** (Windows), or
   - Run: `python app.py`
6. **Open in browser:** **http://127.0.0.1:7860**

**To stop:** Press **Ctrl+C** in the terminal.

---

## Tabs

| Tab | Purpose |
|-----|---------|
| **Workflow** | Load context from **10_Input** (dropdown + Load into context); Run Agent (agent, template, model, output path); status and output preview. |
| **Review Queue** | List drafts; paste artifact path and use **Approve** / **Request changes** / **Archive** (logged to Decision_Log). |
| **Session Logs** | Filter by date/agent; select log; view content (governance audit). |
| **Settings** | Show AEGISLAB_ROOT and routing rules. |

---

## Backend

- **Shared with Streamlit:** `aegislab_ui` (config, repo_validator, templates_loader, router, model_gateway, logging_audit, metadata, safety) is loaded from `09_Operations/Streamlit_App/`.
- **Review queue:** Stored in `09_Operations/Gradio_App/review_queue.json` (persists across restarts; separate from Streamlit’s in-memory queue unless you add shared state later).
- **Session logs / Decision logs:** Same paths as Streamlit (`09_Operations/Session_Logs/`, `09_Operations/Decision_Logs/`).

---

## Security

- **Binding:** App launches with `server_name="127.0.0.1"` and `server_port=7860` — localhost only.
- **Governance:** Same as Streamlit — session logs, front-matter, Authorship_Log, Decision_Log; no writes outside repo.

---

**Last updated:** 2025-02-07
