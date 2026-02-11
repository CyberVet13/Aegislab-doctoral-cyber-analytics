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

**Last updated:** 2025-02-11
