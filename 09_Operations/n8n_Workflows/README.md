# n8n — Workflow automation for AegisLab

**Purpose:** Use [n8n](https://n8n.io) to manage the AegisLab workflow: trigger on **10_Input**, run agents via CLI or API, and place outputs in **11_Results** (or agent Outputs). Same governance (session logs, decision logs, review queue) applies.

**Location:** `09_Operations/n8n_Workflows/`

---

## Quick start (do this on your machine)

1. **Install n8n:** If `npx` is not in PATH, install [Node.js](https://nodejs.org/) (LTS), then run `npx n8n`. Or use Docker: `docker run -it --rm -p 5678:5678 n8nio/n8n`. Open http://localhost:5678 and create local credentials.
2. **Import workflow:** In n8n, import `AegisLab_Run_Agent_Example.json` from this folder. Confirm the **Execute Command** node’s `cwd` is your AegisLab repo root.
3. **Env:** Ensure repo root `.env` has `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`.
4. **Optional (HTTP):** Run Workflow API from repo root: `cd 09_Operations/Workflow_API && pip install -r requirements.txt && python app.py`, then use an n8n **HTTP Request** node to POST to `http://127.0.0.1:8000/run-agent`.

---

## How n8n fits

1. **Trigger:** Schedule, webhook, or file watch (e.g. new file in 10_Input).
2. **Action:** Run the agent — either **Execute Command** (CLI) or **HTTP Request** (Workflow API).
3. **Result:** Artifact written to repo; session log and review queue updated. PI reviews in Streamlit or Gradio.

---

## Option A: n8n + CLI (Execute Command)

### 1. Install n8n

- **Local:** `npx n8n` (Node.js) or `npm install -g n8n && n8n start`
- **Docker:** `docker run -it --rm -p 5678:5678 n8nio/n8n`
- Open **http://localhost:5678** and create an account (local credentials).

### 2. Run the CLI from n8n

Use an **Execute Command** node:

- **Command:** `python`
- **Arguments:** (one per line or as array)
  - Path to script: `09_Operations/scripts/run_agent_cli.py` (use full path to AegisLab repo + this path)
  - `--input`, `10_Input/{{ $json.fileName }}` (or a fixed file)
  - `--agent`, `2`
  - `--template-type`, `Daily Driver`
  - `--output`, `11_Results/{{ $json.fileName }}.md` (or fixed path)

**Working directory:** Set to **AegisLab repo root** (e.g. `C:\Users\kelvi\OneDrive - cybervetssolutions.com\AegisLab`) so that `get_path()` and `.env` resolve correctly.

**Example (single run):**
```text
Working directory: C:\Users\kelvi\OneDrive - cybervetssolutions.com\AegisLab
Command: python
Arguments:
  09_Operations/scripts/run_agent_cli.py
  --input 10_Input/brief.md
  --agent 2
  --template-type "Daily Driver"
  --output 11_Results/artifact.md
```

### 3. CLI reference

```text
python 09_Operations/scripts/run_agent_cli.py --input <path> --agent <1-11> --template-type <Daily Driver|Deep Dive|Review/QA> --output <path> [--assumptions ""] [--constraints ""] [--model-override ""] [--override-rationale ""]
```

- **--input:** Repo-relative path (e.g. `10_Input/brief.md`) or `-` for stdin.
- **--agent:** 1–11.
- **--template-type:** `Daily Driver`, `Deep Dive`, or `Review/QA`.
- **--output:** Repo-relative path (e.g. `11_Results/artifact.md`).
- **--model-override** / **--override-rationale:** Optional; override is logged to Decision_Log.

---

## Option B: n8n + Workflow API (HTTP Request)

A small API runs next to the repo and exposes `POST /run-agent` so n8n can trigger runs without Execute Command.

### 1. Start the Workflow API

From repo root:

```bash
cd 09_Operations/Workflow_API
pip install -r requirements.txt
python app.py
```

API listens on **http://127.0.0.1:8000** (localhost only).

### 2. n8n HTTP Request node

- **Method:** POST  
- **URL:** `http://127.0.0.1:8000/run-agent`  
- **Body (JSON):**
  - `input_path`: e.g. `10_Input/brief.md`
  - `agent_num`: 1–11
  - `template_type`: `Daily Driver` | `Deep Dive` | `Review/QA`
  - `output_path`: e.g. `11_Results/artifact.md`
  - Optional: `assumptions`, `constraints`, `model_override`, `override_rationale`

Response: `{ "success": true, "message": "..." }` or `{ "success": false, "error": "..." }`.

---

## Example workflow (conceptual)

1. **Trigger:** Manual, Schedule (e.g. every hour), or Webhook (e.g. when you drop a file via a small watcher).
2. **List / get input:** If using file-based trigger, get the path of the new file in 10_Input.
3. **Run agent:** Execute Command (CLI) or HTTP Request (API) with that input path and chosen agent/output.
4. **Optional:** Send notification (email, Slack) with output path or status.

See **AegisLab_Run_Agent_Example.json** for an importable n8n workflow (Manual Trigger → Execute Command).

---

## Governance

- Session logs go to `09_Operations/Session_Logs/`.
- Override rationale goes to `09_Operations/Decision_Logs/`.
- Drafts are appended to `09_Operations/Gradio_App/review_queue.json` so Gradio (and optionally Streamlit) show them for PI approval.
- All outputs use front-matter per `00_Governance/AI_Use_Disclosure.md`.

---

## Files

| File | Purpose |
|------|---------|
| **README.md** (this file) | How to use n8n with AegisLab |
| **SETUP_REFERENCE.md** | Your repo path, command, and import steps (ready to use) |
| **AegisLab_Run_Agent_Example.json** | Example n8n workflow (import in n8n) |
| **../scripts/run_agent_cli.py** | CLI for Execute Command |
| **../Workflow_API/** | Optional FastAPI for HTTP trigger |

---

**Last updated:** 2025-02-11
