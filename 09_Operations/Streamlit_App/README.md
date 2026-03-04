# AegisLab Streamlit UI — Operational Console

- **Purpose:** Kickoff UI and operational console for the AegisLab agentic AI environment (not a chatbot).
- **Location:** `09_Operations/Streamlit_App/`
- **Integration:** Uses existing `02_Agents/*/Prompt_Templates.md`, `09_Operations/Session_Logs/`, `00_Governance/`; does not replace any existing structure.

---

## How to access the Streamlit app

1. **Open a terminal** in the repo (e.g. PowerShell or Command Prompt).
2. **Go to the app folder:**
   ```bash
   cd "09_Operations\Streamlit_App"
   ```
   Or in OneDrive path:
   ```bash
   cd "C:\Users\kelvi\OneDrive - cybervetssolutions.com\AegisLab\09_Operations\Streamlit_App"
   ```
3. **Install dependencies (first time only):**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set API keys (first time only):**  
   Create a `.env` at the **repo root** (`AegisLab`), or set in your shell:
   - `OPENAI_API_KEY` — for Run Agent (and RAG)
   - `ANTHROPIC_API_KEY` — for Run Agent  
   Or copy `.env.example` from `09_Operations/Streamlit_App/` to repo root and fill in the keys.
5. **Start the app:**  
   - **Option A:** Double-click **`Launch_Streamlit_UI.bat`** (Windows).  
   - **Option B:** In the terminal (from step 2), run:
     ```bash
     streamlit run app.py
     ```
6. **Open in browser:**  
   Go to **http://localhost:8501**  
   (Streamlit may open it automatically; if not, paste that URL into Chrome, Edge, or Firefox.)

**To stop:** In the terminal where the app is running, press **Ctrl+C**, or close the terminal window.

---

## Quick start (summary)

- **Prerequisites:** Python 3.10+, API keys for OpenAI and Anthropic.
- **Install:** From `09_Operations/Streamlit_App/` run `pip install -r requirements.txt`.
- **Configure:** Copy `.env.example` to repo root as `.env` (or set `AEGISLAB_ROOT`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).
- **Run:** From `09_Operations/Streamlit_App/` run `streamlit run app.py`, or double-click **Launch_Streamlit_UI.bat** (Windows).
- **Access:** **http://localhost:8501**

## Features

- **Dashboard:** Repository health, last 10 sessions, pending reviews count.
- **Run Agent:** Agent 1–11, template type (Daily Driver / Deep Dive / Review-QA), model auto-route or manual override with rationale logging, session log + authorship log + draft to review queue. Optional **RAG**: augment prompts with retrieved context from repo docs (governance, agents, methodology, praxis, session/decision logs); build index once from Run Agent page.
- **Review Queue:** List drafts, view content, PI actions: Approve / Request changes / Archive (decision log entries).
- **Governance Audit:** Filterable session logs (date, agent, model, hashes), diff-friendly view, optional committee packet ZIP export.
- **Settings / Routing:** Display routing rules, per-agent defaults, append routing notes to Decision_Log.

## Governance

- Every run writes a session log to `09_Operations/Session_Logs/YYYY-MM-DD_AgentXX_SessionID.md` with prompt and output SHA-256 hashes.
- Artifacts get YAML front-matter (AI_Assisted, Model_Used, Prompt_Summary, PI_Review_Status).
- Authorship_Log append-only; decision logs for overrides and PI actions.
- No auto-approval; PI must Approve / Request changes / Archive from Review Queue.
- Safety: defensive-scope confirmation when topic may involve offensive security; no writes outside repo.

## RAG (single index)

- One retrieval-augmented index over repo markdown: `00_Governance`, `02_Agents`, `03_Research_Methods`, `04_Praxis_Artifact`, `09_Operations/Session_Logs`, `09_Operations/Decision_Logs`.
- **Build:** On Run Agent page, open "RAG (optional)" and click **Build RAG index** (requires `OPENAI_API_KEY`; uses OpenAI `text-embedding-3-small` via ChromaDB). Index is stored under `09_Operations/Streamlit_App/rag_index/` (gitignored).
- **Use:** Check "Augment this run with retrieved context from repo docs" before running; the prompt is augmented with top-k retrieved chunks. No second RAG needed for the current setup.

## Structure

- `app.py` — kickoff/launcher UI (repo info, status, Run Agent, Dashboard, Review Queue).
- `pages/` — 1_Dashboard, 2_Run_Agent, 3_Review_Queue, 4_Governance_Audit, 5_Settings_Routing.
- `aegislab_ui/` — config, repo_validator, model_gateway, router, logging_audit, metadata, safety, templates_loader, **rag**.

## UI improvements

- **Ideas & roadmap:** [09_Operations/Tool_Configurations/Streamlit_UI_Improvements.md](../Tool_Configurations/Streamlit_UI_Improvements.md) — what’s done and what’s next (metric cards, grouped Run Agent, Review Queue labels, tips, persistence, etc.).

## Hardening & defense readiness

- **Plan:** [STREAMLIT_HARDENING_PLAN.md](STREAMLIT_HARDENING_PLAN.md) — security, reproducibility, AI disclosure, deployment, testing, and documentation checklist for committee and publication readiness.
- Use the plan to prioritize validation, auth (if required), hashing, governance alignment, and tests.

## Security (local use)

- **Binding:** The app is configured to listen only on **127.0.0.1** (localhost). Only **http://localhost:8501** will work; the "Network URL" and "External URL" shown at startup will not be reachable from other devices or the internet.
- **To confirm:** After starting the app, you should see only `Local URL: http://localhost:8501` as the usable address. Access the UI from the same machine only.
- **If you need network access:** Change `address` in `.streamlit/config.toml` (e.g. to `"0.0.0.0"`) only on a trusted network, and use a reverse proxy with authentication (see STREAMLIT_HARDENING_PLAN.md).

## Tests

- Run from repo root or Streamlit_App: `pytest tests/ -v`
