# n8n setup reference — your AegisLab workspace

Use this when configuring n8n. All values below are filled for your machine.

---

## 1. Repo path (for Execute Command node)

**Working directory (cwd):**
```
C:\Users\kelvi\OneDrive - cybervetssolutions.com\AegisLab
```

In n8n Execute Command node, use the same path with **forward slashes** (n8n often accepts both):
```
C:/Users/kelvi/OneDrive - cybervetssolutions.com/AegisLab
```

---

## 2. Command (Execute Command node)

**Command:**
```
python
```

**Arguments (one per line, or as a single string):**
```
09_Operations/scripts/run_agent_cli.py
--input
10_Input/brief.md
--agent
2
--template-type
Daily Driver
--output
11_Results/artifact.md
```

**Single-line form (if your n8n node wants one string):**
```
09_Operations/scripts/run_agent_cli.py --input 10_Input/brief.md --agent 2 --template-type "Daily Driver" --output 11_Results/artifact.md
```

---

## 3. HTTP Request (optional — Workflow API)

If you use the **HTTP Request** node instead of Execute Command:

- **Method:** POST  
- **URL:** `http://127.0.0.1:8000/run-agent`  
- **Body (JSON):**
```json
{
  "input_path": "10_Input/brief.md",
  "agent_num": 2,
  "template_type": "Daily Driver",
  "output_path": "11_Results/artifact.md"
}
```

Start the API first (from repo root):  
`python 09_Operations/Workflow_API/app.py`

---

## 4. Agent and template reference

| Agent # | Name |
|--------|------|
| 1 | 01 PI/Orchestrator |
| 2 | 02 Applied Research Methodologist |
| 3 | 03 Engineering Praxis Architect |
| 4 | 04 Cyber Threat & Adversary Analysis |
| 5 | 05 Cybersecurity Architecture & Zero Trust |
| 6 | 06 Applied Cryptography & Data Protection |
| 7 | 07 Security Data Analytics |
| 8 | 08 Visualization & Decision Support |
| 9 | 09 Doctoral Writing & Argumentation |
| 10 | 10 Committee & Defense Simulation |
| 11 | 11 Ethics, Governance & Risk |

**Template types:** `Daily Driver` | `Deep Dive` | `Review/QA`

---

## 5. Import a workflow in n8n

1. Open n8n (e.g. http://localhost:5678).
2. **Workflows** → **Add workflow** → **Import from File** (or the three-dots menu → Import).
3. Choose one of (from this repo):
   - **AegisLab_Run_Agent_Example.json** — Manual trigger + Execute Command (CLI).
   - **AegisLab_Run_Agent_HTTP_Example.json** — Manual trigger + HTTP Request to Workflow API (start API first: `python 09_Operations/Workflow_API/app.py`).
   - **AegisLab_Run_Agent_Schedule_Example.json** — Runs every hour via Execute Command; edit the schedule node for a different interval (e.g. daily).
4. Each workflow is already set with your repo path / API URL. Click **Execute** to run once (manual workflows), or **Save** and **Activate** for the scheduled workflow.
5. Ensure repo root `.env` has `OPENAI_API_KEY` and `ANTHROPIC_API_KEY`.

---

## 6. Verify your n8n node

After importing a workflow, confirm in the n8n UI:

- **Execute Command node:** Working directory = `C:\Users\kelvi\OneDrive - cybervetssolutions.com\AegisLab` (or same with `/`). Command runs `python` and the CLI script with `--input`, `--agent`, `--template-type`, `--output`.
- **HTTP Request node:** URL = `http://127.0.0.1:8000/run-agent`, Method = POST, Body = JSON (input_path, agent_num, template_type, output_path).
- **Test:** Open the workflow → **Test workflow** / **Execute**. If the run completes without error, the node is set up correctly.

---

## 7. Start n8n (Windows)

- **Double-click:** `09_Operations/n8n_Workflows/Launch_n8n.bat` (starts n8n; open http://localhost:5678).
- **Or in a terminal:** `npx n8n` from any folder (Node.js required).

---

## 8. See your workflow in n8n

**To view the workflow in the n8n UI:**

1. **Start n8n** (Launch_n8n.bat or `npx n8n`), then open **http://localhost:5678** in your browser.
2. Log in if prompted (local account you created).
3. **Workflows** → open **"AegisLab Run Agent"** (or the HTTP/Schedule workflow if you imported those).
4. You’ll see the **canvas** with:
   - **Manual trigger** (or **Every hour** for the schedule workflow) on the left.
   - **Run AegisLab Agent** (Execute Command) or **Run Agent via Workflow API** (HTTP Request) on the right, connected by a line.
5. Click a node to see its settings (command, working directory, or URL and body). Use **Test workflow** / **Execute** to run and see results under each node.

**What each workflow looks like in n8n:**

| Workflow | What you see on the canvas |
|----------|----------------------------|
| **AegisLab Run Agent** (Manual) | `[Manual Trigger]` → `[Run AegisLab Agent]` (runs CLI in your repo). |
| **AegisLab Run Agent (HTTP API)** | `[Manual Trigger]` → `[Run Agent via Workflow API]` (POST to localhost:8000). |
| **AegisLab Run Agent (Scheduled)** | `[Every hour]` → `[Run AegisLab Agent]` (same CLI, triggered on a schedule). |

End-to-end: **10_Input** (your brief) → **this n8n workflow** (trigger + run) → **artifact + session log + review queue** → you review in Streamlit/Gradio → **11_Results** when approved.

**Canvas view (Manual + CLI workflow):**

```
┌─────────────────┐      ┌──────────────────────────────┐
│ Manual Trigger  │ ───► │ Run AegisLab Agent           │
│                 │      │ (Execute Command: python     │
│                 │      │  run_agent_cli.py ...)       │
└─────────────────┘      └──────────────────────────────┘
                                    │
                                    ▼
                          artifact + Session_Log +
                          review_queue.json
```

---

**Last updated:** 2025-02-11
