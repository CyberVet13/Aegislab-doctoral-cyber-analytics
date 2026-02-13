# AegisLab — Document Index

*Quick navigation to key deliverables. Use for proposal assembly, defense prep, and committee reference.*

---

## Governance (00_Governance)

| Document | Purpose |
|----------|---------|
| [Academic_Integrity_Policy.md](00_Governance/Academic_Integrity_Policy.md) | Human authority, transparency, citation, data integrity |
| [AI_Use_Disclosure.md](00_Governance/AI_Use_Disclosure.md) | Models used, scope of AI assistance, committee disclosure statement |
| [Authorship_Log.md](00_Governance/Authorship_Log.md) | Human vs. AI contribution tracking |
| [Change_Log.md](00_Governance/Change_Log.md) | Significant changes to environment and artifacts |
| [Ethics_Approvals/README.md](00_Governance/Ethics_Approvals/README.md) | IRB, data ethics, cybersecurity research ethics |

---

## Program and research design (01_Program_Context, 03_Research_Methods)

| Document | Purpose |
|----------|---------|
| [Alignment_Matrix.md](01_Program_Context/Alignment_Matrix.md) | Course–research–agent mapping |
| [Methodology_Framework_v1.md](03_Research_Methods/Research_Design/Methodology_Framework_v1.md) | Research questions, design, validity summary, timeline |
| [Analysis_Plan.md](03_Research_Methods/Research_Design/Analysis_Plan.md) | Statistical tests, power, assumptions, reproducibility |
| [Threats_and_Mitigations.md](03_Research_Methods/Validity_Frameworks/Threats_and_Mitigations.md) | Internal, external, construct, conclusion validity |

---

## Praxis artifact (04_Praxis_Artifact)

| Document | Purpose |
|----------|---------|
| [System_Architecture_v1.md](04_Praxis_Artifact/Architecture/System_Architecture_v1.md) | Pipeline architecture, components, evaluation instrumentation |
| [Threat_Model_v1.md](04_Praxis_Artifact/Architecture/Threat_Model_v1.md) | Threat model; defensive scope only |
| [Adversary_Profiles.md](04_Praxis_Artifact/Architecture/Adversary_Profiles.md) | Adversary profiles for threat model |
| [Zero_Trust_Design.md](04_Praxis_Artifact/Architecture/Zero_Trust_Design.md) | Zero Trust principles and pillars |
| [Defense_in_Depth_Map.md](04_Praxis_Artifact/Architecture/Defense_in_Depth_Map.md) | DiD layers and control placement |
| [Performance_Criteria.md](04_Praxis_Artifact/Benchmarks/Performance_Criteria.md) | Primary metric (detection rate), success criteria |
| [Cryptographic_Design.md](04_Praxis_Artifact/Architecture/Cryptographic_Design.md) | Algorithms, at rest/transit |
| [Control_Framework_Mapping.md](04_Praxis_Artifact/Documentation/Control_Framework_Mapping.md) | D3FEND, NIST CSF mapping |

---

## Metrics and analysis (02_Agents/07, 06_Analysis)

| Document | Purpose |
|----------|---------|
| [Metrics_Definitions.md](02_Agents/07_Security_Data_Analytics/Outputs/Metrics_Definitions.md) | Operational definitions; detection rate primary |
| [Tool_Selection_Justification.md](02_Agents/07_Security_Data_Analytics/Outputs/Tool_Selection_Justification.md) | SEAS 8414 tool justification |
| [Figure1_Spec.md](06_Analysis/Results/Figures/Figure1_Spec.md) | Pre/post detection rate figure spec |
| [Figure2_Spec.md](06_Analysis/Results/Figures/Figure2_Spec.md) | Effect and CI figure spec |

---

## Ethics, risk, governance (02_Agents/11)

| Document | Purpose |
|----------|---------|
| [Risk_Register.md](02_Agents/11_Ethics_Governance_Risk/Outputs/Risk_Register.md) | Research, data, ethics risks and mitigations |
| [Ethical_Boundaries_Statement.md](02_Agents/11_Ethics_Governance_Risk/Outputs/Ethical_Boundaries_Statement.md) | In/out scope; no offensive or unauthorized activity |
| [Governance_Checklist.md](02_Agents/11_Ethics_Governance_Risk/Outputs/Governance_Checklist.md) | Pre-submission governance checklist |

---

## Writing and defense (07_Writing, 08_Defense)

| Document | Purpose |
|----------|---------|
| [Methodology_Chapter_Draft.md](07_Writing/Drafts/Methodology_Chapter_Draft.md) | Draft methodology section; AI disclosure |
| [Results_Ethics_Limitations_Draft.md](07_Writing/Drafts/Results_Ethics_Limitations_Draft.md) | Results placeholder, ethics, limitations |
| [Methods_QA_Prep.md](08_Defense/Proposal_Defense/Methods_QA_Prep.md) | Methods Q&A for defense |
| [Committee_Questions_2025-02-06.md](08_Defense/Proposal_Defense/Committee_Questions_2025-02-06.md) | Simulated proposal defense questions |
| [Rebuttal_Bank.md](02_Agents/10_Committee_Defense_Simulation/Outputs/Rebuttal_Bank.md) | Rebuttals for key questions |
| [Gap_Analysis.md](02_Agents/10_Committee_Defense_Simulation/Outputs/Gap_Analysis.md) | Gaps and remediations before submission |
| [Proposal_Readiness_Checklist.md](08_Defense/Proposal_Defense/Proposal_Readiness_Checklist.md) | Pre-submission checklist |
| [Research_Summary_One_Pager.md](08_Defense/Proposal_Defense/Research_Summary_One_Pager.md) | One-page summary for committee or defense |
| [Submission_Package_Checklist.md](08_Defense/Proposal_Defense/Submission_Package_Checklist.md) | Documents to include in proposal or committee packet |

---

## Input and Results (10_Input, 11_Results)

| Folder | Purpose |
|--------|---------|
| [10_Input/README.md](10_Input/README.md) | Workflow staging — information to start agent runs (prompts, briefs, context) |
| [11_Results/README.md](11_Results/README.md) | Deliverables (complete) — PI-approved outputs for committee or submission |

---

## Operations (09_Operations)

| Document | Purpose |
|----------|---------|
| [Model_Routing.md](09_Operations/Model_Routing.md) | GPT-5.2 vs. Claude Opus 4.6 vs. Sonnet 4.5 by task |
| [FIRST_RUN.md](09_Operations/FIRST_RUN.md) | First agent session walkthrough |
| [GETTING_STARTED_GIT.md](09_Operations/GETTING_STARTED_GIT.md) | Git init and GitHub push |
| [Tool_Configurations/README.md](09_Operations/Tool_Configurations/README.md) | Cursor and GitHub configuration |
| [Streamlit_App/README.md](09_Operations/Streamlit_App/README.md) | Operational console (Dashboard, Run Agent, Review Queue, Audit) — http://localhost:8501 |
| [Gradio_App/README.md](09_Operations/Gradio_App/README.md) | Workflow manager (Gradio) — http://127.0.0.1:7860 |
| [n8n_Workflows/README.md](09_Operations/n8n_Workflows/README.md) | n8n automation (Manual/Schedule + CLI or HTTP API); [SETUP_REFERENCE.md](09_Operations/n8n_Workflows/SETUP_REFERENCE.md) for path and import |
| [Workflow_API/README.md](09_Operations/Workflow_API/README.md) | HTTP API for n8n (POST /run-agent) |
| [Workflow_Visual.md](09_Operations/Workflow_Visual.md) | Workflow diagram (10_Input → Run Agent → Review Queue → 11_Results) |
| [Agentic_Environment_Workflow_View.md](09_Operations/Agentic_Environment_Workflow_View.md) | Full agentic AI environment: entry points, 11 agents, governance, RAG |
| [Status_Report_2025-02-06.md](02_Agents/01_PI_Orchestrator/Outputs/Status_Report_2025-02-06.md) | Current status and upcoming tasks |
| [Decision_Logs/](09_Operations/Decision_Logs/) | PI decisions (design, threat model, etc.) |
| [Session_Logs/](09_Operations/Session_Logs/) | Agent session logs |

---

**Last Updated:** 2025-02-07
