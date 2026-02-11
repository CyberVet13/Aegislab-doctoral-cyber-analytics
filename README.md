# AegisLab — Doctoral Research Environment in Cybersecurity Analytics

**Repository:** [https://github.com/CyberVet13/Aegislab-doctoral-cyber-analytics](https://github.com/CyberVet13/Aegislab-doctoral-cyber-analytics)  
**Local path:** `C:\Users\kelvi\OneDrive - cybervetssolutions.com\AegisLab`

AegisLab is a rigorous, auditable, and committee-defensible virtual research laboratory for a Doctor of Engineering (D.Eng.) in Cybersecurity Analytics. It provides a complete agentic system architecture aligned to seven doctoral courses (SEAS 8400, 8405, 8410, 8414, 8415, 8499, 8188), with full human-in-the-loop authority, audit trails, and AI disclosure standards.

---

## Quick navigation

- **Document index:** [AegisLab_Index.md](AegisLab_Index.md) — Key deliverables and where to find them (governance, methodology, artifact, defense, operations).
- **Environment architecture:** [04_Praxis_Artifact/Architecture/Environment_Architecture_View.md](04_Praxis_Artifact/Architecture/Environment_Architecture_View.md) — Repo, Streamlit console, agents, LLM gateway, governance, RAG.
- **Proposal readiness:** [08_Defense/Proposal_Defense/Proposal_Readiness_Checklist.md](08_Defense/Proposal_Defense/Proposal_Readiness_Checklist.md). **Committee:** [Research_Summary_One_Pager](08_Defense/Proposal_Defense/Research_Summary_One_Pager.md), [Submission_Package_Checklist](08_Defense/Proposal_Defense/Submission_Package_Checklist.md).
- **First run:** [09_Operations/FIRST_RUN.md](09_Operations/FIRST_RUN.md). **Git:** [09_Operations/GETTING_STARTED_GIT.md](09_Operations/GETTING_STARTED_GIT.md) and [09_Operations/READY_FOR_GIT.md](09_Operations/READY_FOR_GIT.md).
- **Operational console (Streamlit UI):** [09_Operations/Streamlit_App/README.md](09_Operations/Streamlit_App/README.md) — run agents, review queue, governance audit. Run from `09_Operations/Streamlit_App/` via `streamlit run app.py` or **Launch_Streamlit_UI.bat**; open **http://localhost:8501**.
- **Workflow manager (Gradio):** [09_Operations/Gradio_App/README.md](09_Operations/Gradio_App/README.md) — manage workflow with Gradio: 10_Input → Run Agent → Review Queue. Run `python app.py` from `09_Operations/Gradio_App/` or **Launch_Gradio_UI.bat**; open **http://127.0.0.1:7860**.
- **Workflow automation (n8n):** [09_Operations/n8n_Workflows/README.md](09_Operations/n8n_Workflows/README.md) — trigger agent runs via n8n (Manual/Schedule + CLI, or HTTP to Workflow API). See [SETUP_REFERENCE.md](09_Operations/n8n_Workflows/SETUP_REFERENCE.md) for your repo path and import steps; import any of `AegisLab_Run_Agent_Example.json`, `AegisLab_Run_Agent_HTTP_Example.json`, or `AegisLab_Run_Agent_Schedule_Example.json`.
- **Workflow visual:** [09_Operations/Workflow_Visual.md](09_Operations/Workflow_Visual.md) — diagram (10_Input → Run Agent → Review Queue → 11_Results); Streamlit, Gradio, n8n.
- **Full agentic environment:** [09_Operations/Agentic_Environment_Workflow_View.md](09_Operations/Agentic_Environment_Workflow_View.md) — entire AI environment: all entry points, 11 agents, governance, RAG, data flow.

---

## Purpose

- **Principal Investigator (PI) authority:** All research decisions and committee-facing outputs require PI review and approval.
- **Academic integrity:** Governance policies and AI use disclosure ensure transparent, defensible use of AI tools (OpenAI GPT-5.2, Anthropic Claude Opus 4.6, Claude Sonnet 4.5).
- **Course alignment:** Research activities and deliverables map to program learning outcomes via `01_Program_Context/Alignment_Matrix.md`.
- **Auditability:** Session logs, decision logs, authorship log, and change log support reproducibility and committee review.

---

## Repository Structure

| Folder | Purpose |
|--------|---------|
| **00_Governance/** | Academic integrity policy, AI use disclosure, authorship log, change log, ethics approvals |
| **01_Program_Context/** | Course syllabi, learning outcomes, course–research alignment matrix |
| **02_Agents/** | 11 specialized agents: role charters, prompt templates (Daily Driver, Deep Dive, Review/QA), Outputs/, Reviews/ |
| **03_Research_Methods/** | Literature reviews, research design, validity frameworks |
| **04_Praxis_Artifact/** | Architecture, implementation, benchmarks, documentation |
| **05_Data/** | Raw, processed, and synthetic data (with provenance) |
| **06_Analysis/** | Exploratory, statistical, and results (including figures) |
| **07_Writing/** | Drafts, peer reviews, final submissions |
| **08_Defense/** | Proposal defense, mock defenses, final defense materials |
| **09_Operations/** | Model routing, tool configurations, session logs, decision logs |
| **10_Input/** | Workflow staging — information to start agent runs (prompts, briefs, context) |
| **11_Results/** | Deliverables (complete) — PI-approved outputs ready for committee or submission |
| **99_Archive/** | Deprecated and historical materials |

---

## Agents (11)

| # | Agent | Primary Course Alignment |
|---|--------|---------------------------|
| 01 | PI/Orchestrator | 8499, 8188 |
| 02 | Applied Research Methodologist | 8499, 8188, 8414 |
| 03 | Engineering Praxis Architect | 8405, 8188, 8410, 8414 |
| 04 | Cyber Threat & Adversary Analysis | 8400, 8405, 8410, 8188 |
| 05 | Cybersecurity Architecture & Zero Trust | 8405, 8414, 8188 |
| 06 | Applied Cryptography & Data Protection | 8415, 8405, 8188 |
| 07 | Security Data Analytics | 8410, 8414, 8188 |
| 08 | Visualization & Decision Support | 8410, 8414, 8188 |
| 09 | Doctoral Writing & Argumentation | 8499, 8188 |
| 10 | Committee & Defense Simulation | 8499, 8188 |
| 11 | Ethics, Governance & Risk | 8499, 8188, 8414 |

Each agent has a **Role_Charter.md**, **Prompt_Templates.md** (Daily Driver, Deep Dive, Review/QA), **Outputs/**, and **Reviews/**.

---

## Getting Started

1. **Governance:** Read `00_Governance/Academic_Integrity_Policy.md` and `00_Governance/AI_Use_Disclosure.md`. Complete PI acknowledgment and certification where indicated.
2. **Alignment:** Review `01_Program_Context/Alignment_Matrix.md` and add course syllabi/learning outcomes in `01_Program_Context/` as needed (stubs in `Learning_Outcomes/`; replace with official outcomes when available).
3. **First agent run:** Follow `09_Operations/FIRST_RUN.md` to run Agent 02 (Daily Driver), save output, and create a session log.
4. **Agents:** For each task, open the relevant agent folder under `02_Agents/`, use the Reproducibility Block and the appropriate prompt template from `Prompt_Templates.md`, and select model per `09_Operations/Model_Routing.md`.
5. **Logging:** After each session, log in `09_Operations/Session_Logs/` and add the reproducibility block to any new output file. Update `00_Governance/Authorship_Log.md` for committee-facing artifacts.
6. **Git and GitHub:** Connect the repo and push the scaffold using `09_Operations/GETTING_STARTED_GIT.md`. Use the included `.gitignore` as needed.
7. **Tools:** See `09_Operations/Tool_Configurations/` for Cursor and GitHub setup.
8. **Streamlit UI (optional):** From `09_Operations/Streamlit_App/`, run `pip install -r requirements.txt`, set `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` (e.g. in a `.env` at repo root), then run `streamlit run app.py` or double-click **Launch_Streamlit_UI.bat**. Open **http://localhost:8501** for Dashboard, Run Agent, Review Queue, and Governance Audit.
9. **Gradio workflow manager (optional):** From `09_Operations/Gradio_App/`, run `pip install -r requirements.txt` (same API keys as above), then run `python app.py` or double-click **Launch_Gradio_UI.bat**. Open **http://127.0.0.1:7860** for Workflow (10_Input + Run Agent), Review Queue, Session Logs, and Settings. Uses the same backend (`aegislab_ui`) as Streamlit.
10. **n8n (optional):** Install n8n (`npx n8n` or Docker). See [n8n_Workflows/README.md](09_Operations/n8n_Workflows/README.md) and [SETUP_REFERENCE.md](09_Operations/n8n_Workflows/SETUP_REFERENCE.md). Import one of: **AegisLab_Run_Agent_Example.json** (Manual + CLI), **AegisLab_Run_Agent_HTTP_Example.json** (Manual + Workflow API), **AegisLab_Run_Agent_Schedule_Example.json** (e.g. hourly + CLI).

---

## Model Routing

- **Daily Driver (routine tasks):** Claude Sonnet 4.5 (default).
- **Deep Dive (methodology, architecture, writing, ethics):** Claude Opus 4.6 or GPT-5.2.
- **Review/QA:** Claude Opus 4.6.

Details: `09_Operations/Model_Routing.md`.

---

## AI Disclosure (Committee-Facing)

All committee-facing documents must include the disclosure statement in `00_Governance/AI_Use_Disclosure.md`. Every AI-assisted file must include file-level metadata (session date, model, prompt summary, PI_Review_Status, modifications).

---

## Quality and Safety

- **No unsafe instructions:** No malware, hacking, or unauthorized access. Threat and adversary work is defensive only.
- **Citations:** All claims trace to primary sources; PI verifies references.
- **Reproducibility:** Analysis code versioned; random seeds and environment documented; session logs and decision logs maintained.

---

## License and Ownership

Research outputs are owned by the Principal Investigator and institution per applicable policies. This scaffold is for doctoral research use within the stated governance and integrity framework.

---

**Last Updated:** 2025-02-06  
**Principal Investigator:** [Kelvin Barton]  
**Program:** Doctor of Engineering in Cybersecurity Analytics
