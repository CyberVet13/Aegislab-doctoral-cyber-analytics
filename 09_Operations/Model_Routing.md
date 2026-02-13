# Model Routing Guidance - AegisLab Doctoral Research

## Purpose
This document guides selection of OpenAI GPT-5.2, Anthropic Claude Opus 4.6, and Anthropic Claude Sonnet 4.5 for agent sessions to balance quality, cost, latency, and reproducibility. All usage must be logged in `09_Operations/Session_Logs/` with model identifier.

---

## Model Summary

| Model | Best For | Typical Session Types | Latency | Use When |
|-------|----------|------------------------|---------|----------|
| **OpenAI GPT-5.2** | Complex reasoning, long-context synthesis, technical writing | Deep Dive, multi-step integration, literature synthesis | Medium–High | Proposal/report integration, cross-agent synthesis, nuanced argumentation |
| **Claude Opus 4.6** | Deep analysis, methodology design, critical review, defense simulation | Deep Dive, Review/QA, methodology and ethics | Medium–High | Methods chapter, validity frameworks, committee Q&A, ethics/governance |
| **Claude Sonnet 4.5** | Fast iteration, code, data scripts, daily coordination | Daily Driver, scripts, metrics, short handoffs | Low | Day-to-day tasks, analysis scripts, quick decisions, diagram specs |

---

## By Agent (Recommended Defaults)

| Agent | Daily Driver | Deep Dive | Review/QA |
|-------|--------------|-----------|-----------|
| **01 PI/Orchestrator** | Sonnet 4.5 | GPT-5.2 or Opus 4.6 | Opus 4.6 |
| **02 Applied Research Methodologist** | Sonnet 4.5 | Opus 4.6 | Opus 4.6 |
| **03 Engineering Praxis Architect** | Sonnet 4.5 | GPT-5.2 or Opus 4.6 | Opus 4.6 |
| **04 Cyber Threat & Adversary Analysis** | Sonnet 4.5 | Opus 4.6 or GPT-5.2 | Opus 4.6 |
| **05 Cybersecurity Architecture & Zero Trust** | Sonnet 4.5 | Opus 4.6 | Opus 4.6 |
| **06 Applied Cryptography & Data Protection** | Sonnet 4.5 | Opus 4.6 | Opus 4.6 |
| **07 Security Data Analytics** | Sonnet 4.5 | GPT-5.2 or Sonnet 4.5 (code) | Opus 4.6 |
| **08 Visualization & Decision Support** | Sonnet 4.5 | GPT-5.2 or Opus 4.6 | Opus 4.6 |
| **09 Doctoral Writing & Argumentation** | Sonnet 4.5 | GPT-5.2 or Opus 4.6 | Opus 4.6 |
| **10 Committee & Defense Simulation** | Sonnet 4.5 | Opus 4.6 | Opus 4.6 |
| **11 Ethics, Governance & Risk** | Sonnet 4.5 | Opus 4.6 | Opus 4.6 |

**Rationale:**
- **Daily Driver:** Speed and cost matter; Sonnet 4.5 handles structured handoffs and short tasks well.
- **Deep Dive:** Opus 4.6 for methodology, ethics, and critical analysis; GPT-5.2 for large-scale synthesis and technical writing when long context is needed.
- **Review/QA:** Opus 4.6 for consistent critical review and checklist application.
- **Code/scripts (Agent 07):** Sonnet 4.5 or GPT-5.2 depending on complexity; Sonnet 4.5 is often sufficient for data/analysis code.

---

## By Task Type

- **Literature synthesis, long document integration:** GPT-5.2
- **Research design, validity, ethics, governance:** Opus 4.6
- **Threat modeling, ATT&CK/D3FEND mapping:** Opus 4.6 or GPT-5.2
- **Architecture and crypto design:** Opus 4.6 or GPT-5.2
- **Analysis scripts, metrics definitions, data pipelines:** Sonnet 4.5 (or GPT-5.2 if very complex)
- **Writing revision, argumentation, citations:** GPT-5.2 or Opus 4.6
- **Mock committee questions, rebuttals, gap analysis:** Opus 4.6
- **Quick status, task assignment, single decision request:** Sonnet 4.5

---

## Reproducibility and Logging

- **Session log:** Every session must be logged in `09_Operations/Session_Logs/` with:
  - Date, model used, agent, prompt template (Daily Driver / Deep Dive / Review/QA)
  - Brief prompt summary and output path
  - PI decision or follow-up
- **File header:** Every AI-assisted output file must include the reproducibility block (session date, model, prompt summary, PI_Review_Status) per `00_Governance/AI_Use_Disclosure.md`.
- **Cross-validation:** For high-stakes outputs (methods chapter, threat model, ethics section), consider running the same prompt with a second model and comparing; document in Session_Logs and Authorship_Log.

---

## Overrides

- **PI may override** any recommendation (e.g., use Opus for all Deep Dives for consistency).
- **Resource constraints:** If token or cost limits apply, prefer Sonnet 4.5 for Daily Driver and reserve Opus 4.6/GPT-5.2 for Deep Dive and Review/QA.
- **Reproducibility runs:** When re-running a prompt for reproducibility, use the same model and document in Session_Logs.

---

**Last Updated:** 2025-02-06  
**Owner:** Principal Investigator
