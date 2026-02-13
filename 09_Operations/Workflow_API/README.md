# AegisLab Workflow API

**Purpose:** HTTP API so n8n (or other tools) can trigger agent runs with **HTTP Request** instead of Execute Command. Uses the same logic as `09_Operations/scripts/run_agent_cli.py`.

**Run:** From repo root or this folder:
```bash
cd 09_Operations/Workflow_API
pip install -r requirements.txt
python app.py
```
API: **http://127.0.0.1:8000** (localhost only).

**Endpoints:**
- `POST /run-agent` — JSON body: `input_path`, `agent_num`, `template_type`, `output_path`, optional `assumptions`, `constraints`, `model_override`, `override_rationale`. Returns `{ "success": true, "message": "..." }` or 400 with detail.
- `GET /health` — Returns `{ "status": "ok" }`.

**Verify (API running):** Open http://127.0.0.1:8000/health in a browser, or `curl http://127.0.0.1:8000/health`. You should see `{"status":"ok"}`.

**n8n:** Use HTTP Request node: POST to `http://127.0.0.1:8000/run-agent`, body type JSON.

**Last updated:** 2025-02-07
