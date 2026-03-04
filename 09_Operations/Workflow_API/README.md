# AegisLab Workflow API

**Purpose:** HTTP API so Zapier (or other tools) can trigger agent runs with **HTTP Request** instead of Execute Command. Uses the same logic as `09_Operations/scripts/run_agent_cli.py`.

**Run:** From repo root or this folder:
```bash
cd 09_Operations/Workflow_API
pip install -r requirements.txt
python app.py
```
API: **http://127.0.0.1:8002** (localhost only).

**Endpoints:**
- `POST /run-agent` — JSON body: `input_path`, `agent_num`, `template_type`, `output_path`, optional `assumptions`, `constraints`, `model_override`, `override_rationale`, `confirm_defensive_scope` (required when topic may involve offensive security). Returns `{ "success": true, "message": "..." }` or 400 with detail.
- `POST /upload` — Multipart form with `files` (one or more). Saves to `10_Input/`. Accepts .docx, .xlsx, .pdf, .md, .txt. Used by Aegislab Dashboard for direct upload.
- `POST /process-input` — Process all documents in `10_Input/`; runs Agent 02 on each. Used by Dashboard Auto-Process.
- `GET /health` — Returns `{ "status": "ok" }`.
- `GET /assignment-status` — Returns `{ queued: [...], completed: [...] }` for Course Management status widget.

**Verify (API running):** Open http://127.0.0.1:8002/health in a browser, or `curl http://127.0.0.1:8002/health`. You should see `{"status":"ok"}`.

**Zapier:** Use Webhooks by Zapier → POST to `http://127.0.0.1:8002/run-agent` (or ngrok URL if exposed), body type JSON.

**Last updated:** 2025-02-07
