# Streamlit UI Workflow — AegisLab Operational Console

## Purpose

- Operational console (not a chatbot) for agent management, LLM session execution, governance enforcement, and audit trail.
- Committee-defensible; eliminates "mystery AI" through logging, metadata, and human-in-the-loop approval.

## Workflow checklist

### Before first run

- [ ] Python 3.10+ and `pip install -r 09_Operations/Streamlit_App/requirements.txt`
- [ ] `.env` at repo root with `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` (optional: `AEGISLAB_ROOT`)
- [ ] Run from `09_Operations/Streamlit_App/`: `streamlit run app.py`

### Run Agent

- [ ] Select Agent (1–11) and template type (Daily Driver / Deep Dive / Review-QA)
- [ ] Fill research objective, assumptions, constraints; set output path (within repo only)
- [ ] Defensive-scope confirmation if topic may involve offensive security
- [ ] Model: Auto-route or manual override (override requires rationale → Decision_Log)
- [ ] Run → session log written, hashes stored, artifact with front-matter, draft added to Review Queue

### Review Queue

- [ ] No auto-approval; PI must act on each draft
- [ ] Actions: **Approve** (update PI_Review_Status, Decision_Log) / **Request changes** / **Archive**
- [ ] Approval triggers decision log entry and metadata update

### Governance Audit

- [ ] Filter session logs by date/agent; view hashes and diff-friendly content
- [ ] Optional: generate committee packet ZIP (session + decision logs)

### Settings / Routing

- [ ] View default routing by template type and per-agent overrides
- [ ] Manual overrides always log rationale to Decision_Log
- [ ] Append routing notes to Decision_Log for auditors

## Path and safety rules

- All outputs constrained within AegisLab repo; no writes outside `AEGISLAB_ROOT`
- Session log naming: `09_Operations/Session_Logs/YYYY-MM-DD_AgentXX_SessionID.md`
- Decision log naming: `09_Operations/Decision_Logs/YYYY-MM-DD_Decision_Topic.md`
- Reproducibility: prompt_payload and model_output SHA-256 hashes in every session log

## Integration points

- **Templates:** Loaded from `02_Agents/*/Prompt_Templates.md` (Daily Driver, Deep Dive, Review/QA sections)
- **Governance:** Append to `00_Governance/Authorship_Log.md`; front-matter per `00_Governance/AI_Use_Disclosure.md`
- **Routing:** Aligned with `09_Operations/Model_Routing.md`

**Last Updated:** 2025-02-07
