# AegisLab Streamlit UI — Operational Console

- **Purpose:** Production-ready operational console for the AegisLab doctoral research environment (not a chatbot).
- **Location:** `09_Operations/Streamlit_App/`
- **Integration:** Uses existing `02_Agents/*/Prompt_Templates.md`, `09_Operations/Session_Logs/`, `00_Governance/`; does not replace any existing structure.

## Quick start

- **Prerequisites:** Python 3.10+, API keys for OpenAI and Anthropic.
- **Install:** From `09_Operations/Streamlit_App/` run `pip install -r requirements.txt`.
- **Configure:** Copy `.env.example` to repo root as `.env` (or set `AEGISLAB_ROOT`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).
- **Run:** From `09_Operations/Streamlit_App/` run `streamlit run app.py`, or double-click **Launch_Streamlit_UI.bat** (Windows).

## Features

- **Dashboard:** Repository health, last 10 sessions, pending reviews count.
- **Run Agent:** Agent 1–11, template type (Daily Driver / Deep Dive / Review-QA), model auto-route or manual override with rationale logging, session log + authorship log + draft to review queue.
- **Review Queue:** List drafts, view content, PI actions: Approve / Request changes / Archive (decision log entries).
- **Governance Audit:** Filterable session logs (date, agent, model, hashes), diff-friendly view, optional committee packet ZIP export.
- **Settings / Routing:** Display routing rules, per-agent defaults, append routing notes to Decision_Log.

## Governance

- Every run writes a session log to `09_Operations/Session_Logs/YYYY-MM-DD_AgentXX_SessionID.md` with prompt and output SHA-256 hashes.
- Artifacts get YAML front-matter (AI_Assisted, Model_Used, Prompt_Summary, PI_Review_Status).
- Authorship_Log append-only; decision logs for overrides and PI actions.
- No auto-approval; PI must Approve / Request changes / Archive from Review Queue.
- Safety: defensive-scope confirmation when topic may involve offensive security; no writes outside repo.

## Structure

- `app.py` — main shell.
- `pages/` — 1_Dashboard, 2_Run_Agent, 3_Review_Queue, 4_Governance_Audit, 5_Settings_Routing.
- `aegislab_ui/` — config, repo_validator, model_gateway, router, logging_audit, metadata, safety, templates_loader.

## Hardening & defense readiness

- **Plan:** [STREAMLIT_HARDENING_PLAN.md](STREAMLIT_HARDENING_PLAN.md) — security, reproducibility, AI disclosure, deployment, testing, and documentation checklist for committee and publication readiness.
- Use the plan to prioritize validation, auth (if required), hashing, governance alignment, and tests.

## Tests

- Run from repo root or Streamlit_App: `pytest tests/ -v`
