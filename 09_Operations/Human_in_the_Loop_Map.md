# AegisLab — Human-in-the-Loop Map

**Purpose:** Map all points where you (the PI) make decisions, confirm, or approve in the workflow. Supports governance, committee defensibility, and identifying gaps.

**Last Updated:** 2026-02-21

---

## Summary

| Phase | Your role | Where | Required? |
|-------|-----------|-------|-----------|
| **Trigger** | Place content in 10_Input | Dashboard, file drag, or manual | Optional (Zapier/API can trigger) |
| **Run Agent** | Choose agent, template, context, model | Streamlit, Gradio | Optional (Auto-Processor skips) |
| **Defensive scope** | Confirm defensive/authorized scope | Run Agent (Streamlit/Gradio) | When topic triggers |
| **Model override** | Provide rationale for override | Run Agent, CLI, API | When overriding model |
| **Review Queue** | Approve / Request changes / Archive | Streamlit, Gradio | **Required** for committee-ready |
| **Settings** | Per-agent model overrides | Streamlit Settings | Optional |
| **Governance** | Authorship_Log, Decision_Logs | Manual / after actions | Per policy |
| **Git** | Approve merges to main | GitHub | Per Tool_Configurations |

---

## 1. Trigger (10_Input)

**You are in the loop when:**
- You place a brief, prompt, or document in `10_Input/`
- You use the Dashboard **Upload** to add files
- You choose which file to load in Streamlit/Gradio "Load context from 10_Input"

**You are NOT in the loop when:**
- Zapier webhook triggers `/run-agent` with a predefined `input_path`
- Auto-Processor picks up files dropped by someone else
- Scheduled Zapier run uses `10_Input/brief.md` automatically

**Gap:** Zapier and Auto-Processor can run without you choosing the input. Output still goes to Review Queue.

---

## 2. Run Agent (Agent, Template, Context, Output)

**You are in the loop when:**
- Streamlit **Run Agent** or Gradio **Workflow** tab: you select agent, template, context, output path, and click Run
- You type or edit the research objective / context

**You are NOT in the loop when:**
- **Dashboard Auto-Process:** Always Agent 02, Daily Driver; no agent/template choice
- **Zapier / Workflow API:** `POST /run-agent` with fixed params
- **CLI:** Scripted `run_agent_cli.py --input ... --agent 2 ...`
- **Auto-Processor:** Always Agent 02, Daily Driver; output `11_Results/{stem}_deliverable.md`

**Gap:** Dashboard and Auto-Processor assume Agent 02. No human choice of agent or template.

---

## 3. Defensive Scope Confirmation

**You are in the loop when:**
- Run Agent (Streamlit/Gradio) shows: "This topic may involve offensive security..."
- You must check **"I confirm this is defensive/authorized scope only"** before Run

**You are NOT in the loop when:**
- CLI, Workflow API, Auto-Processor: no defensive-scope checkbox; safety guard only blocks blocked patterns
- Gradio: has safety check but no explicit defensive-scope confirmation UI (relies on check_prompt)

**Gap:** CLI and API do not require explicit defensive-scope confirmation. Safety blocks obviously bad prompts but does not require affirmative PI confirmation for edge cases.

---

## 4. Model Override

**You are in the loop when:**
- Streamlit/Gradio: you choose "Manual override", pick model, and provide **rationale** (logged to Decision_Log)
- CLI: `--model-override` requires `--override-rationale`
- API: `model_override` requires `override_rationale`

**You are NOT in the loop when:**
- Auto-route: no override; model chosen by template/agent
- Auto-Processor, Dashboard: always auto-route (Claude Sonnet 4.5 for Daily Driver)

**No gap:** Override always requires rationale when used.

---

## 5. Review Queue — Approve / Request / Archive

**You are in the loop when:**
- Streamlit **Review Queue** or Gradio **Review Queue** tab
- You click **Approve**, **Request changes**, or **Archive** for each draft
- You click **Approve all** (batch)

**You are NOT in the loop when:**
- No automated path to "Approved" without Review Queue
- All agent outputs go to `review_queue.json`; none skip to Approved

**No gap:** This is the mandatory human gate. Committee-ready artifacts require PI approval here.

---

## 6. Settings / Model Routing

**You are in the loop when:**
- Streamlit **Settings** → per-agent model overrides
- You edit `09_Operations/Model_Routing.md` (if used)

**Optional:** Default routing works without your input.

---

## 7. Governance (Authorship_Log, Decision_Logs)

**You are in the loop when:**
- You update `00_Governance/Authorship_Log.md` for committee-facing artifacts
- You review `09_Operations/Decision_Logs/` for overrides and PI actions
- You maintain `00_Governance/Change_Log.md`

**Policy:** Monthly self-audits; pre-submission checklist.

---

## 8. Git / Branch Strategy

**You are in the loop when:**
- You approve PRs and merges to `main` (per Tool_Configurations)
- You commit committee-ready artifacts after Review Queue approval

**Policy:** No automated deployment; PI approves merges for governance and 07_Writing, 08_Defense.

---

## Flow by Entry Point

| Entry point | You choose input? | You choose agent/template? | Defensive confirm? | You approve in Review Queue? |
|-------------|-------------------|----------------------------|--------------------|------------------------------|
| **Streamlit Run Agent** | Yes (load or type) | Yes | Yes (if triggered) | Yes |
| **Gradio Workflow** | Yes (load or type) | Yes | Via safety check | Yes |
| **Dashboard Upload + Auto-Process** | Yes (upload) | No (Agent 02) | No | Yes |
| **Auto-Processor** (file watcher) | No (any new file) | No (Agent 02) | No | Yes |
| **Zapier / API** | No (fixed in payload) | No (fixed in payload) | No | Yes |
| **CLI** | Yes (--input) | Yes (--agent, --template-type) | No | Yes |

---

## Zapier and Agent 02 Automation

**Zapier runs** (POST /run-agent) and **Dashboard Auto-Process** / **Auto-Processor** use fixed parameters:
- Agent 02 (Applied Research Methodologist) only
- Daily Driver template
- Output: `11_Results/{stem}_deliverable.md`

**Human-in-the-loop:** All outputs go to Review Queue. No auto-approve. You must Approve in Streamlit or Gradio before artifacts are committee-ready.

**Defensive scope:** When input content triggers offensive-security heuristics (e.g., "exploit", "red team"), CLI and API require `--confirm-defensive-scope` or `confirm_defensive_scope: true`. Auto-Processor and Dashboard /process-input do not pass this; such files will fail and require manual run with confirmation.

**Use Streamlit** when you need full agent choice, template selection, or defensive-scope confirmation.

---

## Implemented Strengthenings (2026-02-21)

| Recommendation | Status |
|----------------|--------|
| **Defensive scope (CLI/API)** | ✅ CLI: `--confirm-defensive-scope`; API: `confirm_defensive_scope: true` when topic triggers |
| **Batch Approve** | ✅ Streamlit: checkboxes + "Approve selected" (review before approving) |
| **Zapier** | ✅ Documented above: Review Queue required; no auto-approve |
| **Agent 02–only** | ✅ Documented above: use Streamlit for full agent choice |

---

## Related

- [Workflow_Visual.md](Workflow_Visual.md) — End-to-end flow
- [BPNA_Workflow.md](BPNA_Workflow.md) — Process model
- [00_Governance/Academic_Integrity_Policy.md](../00_Governance/Academic_Integrity_Policy.md) — Human authority
- [Tool_Configurations/README.md](Tool_Configurations/README.md) — PI authority, Decision Required
