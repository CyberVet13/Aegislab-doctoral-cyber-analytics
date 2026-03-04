# Agentic AI Readiness Checklist — AegisLab

**Purpose:** Assess organizational readiness before starting agentic AI projects. Use before scaling automation or adding new agent workflows. Align with [Human_in_the_Loop_Map.md](../09_Operations/Human_in_the_Loop_Map.md) and [Academic_Integrity_Policy.md](Academic_Integrity_Policy.md).

**Last Updated:** 2026-02-21

---

## Process maturity

| Check | AegisLab mapping |
|-------|------------------|
| ☐ Do you have clear, documented processes for the work you want to automate? | [BPNA_Workflow.md](../09_Operations/BPNA_Workflow.md), [Workflow_Visual.md](../09_Operations/Workflow_Visual.md), [Agentic_Environment_Workflow_View.md](../09_Operations/Agentic_Environment_Workflow_View.md) |
| ☐ Can you define success in specific, measurable terms? | [Performance_Criteria.md](../04_Praxis_Artifact/Benchmarks/Performance_Criteria.md), [Metrics_Definitions.md](../02_Agents/07_Security_Data_Analytics/Outputs/Metrics_Definitions.md), [Analysis_Plan.md](../03_Research_Methods/Research_Design/Analysis_Plan.md) |
| ☐ Do you have clean, accessible data for the processes? | [05_Data/README.md](../05_Data/README.md), [10_Input/README.md](../10_Input/README.md), 10_Input staging, PDF/DOCX extraction cache |

---

## Technical readiness

| Check | AegisLab mapping |
|-------|------------------|
| ☐ Do you have systems that can integrate with external agents? | Workflow API ([09_Operations/Workflow_API/](../09_Operations/Workflow_API/)), Zapier ([Zapier_Workflows/](../09_Operations/Zapier_Workflows/)), CLI ([run_agent_cli.py](../09_Operations/scripts/run_agent_cli.py)) |
| ☐ Is your data infrastructure production-ready? | Repo structure, [System_Architecture_v1.md](../04_Praxis_Artifact/Architecture/System_Architecture_v1.md), [Environment_Architecture_View.md](../04_Praxis_Artifact/Architecture/Environment_Architecture_View.md) |
| ☐ Do you have monitoring and logging capabilities? | [Session_Logs/](../09_Operations/Session_Logs/), [Decision_Logs/](../09_Operations/Decision_Logs/), [Authorship_Log.md](Authorship_Log.md), [LoggingAudit](../09_Operations/Streamlit_App/aegislab_ui/logging_audit.py) |

---

## Organizational readiness

| Check | AegisLab mapping |
|-------|------------------|
| ☐ Are the people who do this work involved in the design process? | PI authority ([Academic_Integrity_Policy.md](Academic_Integrity_Policy.md)), [Human_in_the_Loop_Map.md](../09_Operations/Human_in_the_Loop_Map.md), Review Queue (Streamlit/Gradio) |
| ☐ Do you have executive sponsorship for a 12-month timeline? | Program alignment ([Alignment_Matrix.md](../01_Program_Context/Alignment_Matrix.md)), [Methodology_Framework_v1.md](../03_Research_Methods/Research_Design/Methodology_Framework_v1.md) |
| ☐ Is there a budget for continuous improvement after launch? | [Change_Log.md](Change_Log.md), [BPNA_Workflow_Bottleneck_Analysis.md](../09_Operations/BPNA_Workflow_Bottleneck_Analysis.md), [STREAMLIT_HARDENING_PLAN.md](../09_Operations/Streamlit_App/STREAMLIT_HARDENING_PLAN.md) |

---

## Risk management

| Check | AegisLab mapping |
|-------|------------------|
| ☐ Have you identified what happens when the agent fails? | [BPNA_Workflow_Bottleneck_Analysis.md](../09_Operations/BPNA_Workflow_Bottleneck_Analysis.md), [SafetyGuard](../09_Operations/Streamlit_App/aegislab_ui/safety.py), error handling in run_agent_cli |
| ☐ Are there clear escalation paths to humans? | [Human_in_the_Loop_Map.md](../09_Operations/Human_in_the_Loop_Map.md), Review Queue (Approve / Request changes / Archive), `--confirm-defensive-scope` |
| ☐ Do you have compliance and audit requirements mapped out? | [Governance_Checklist.md](../02_Agents/11_Ethics_Governance_Risk/Outputs/Governance_Checklist.md), [Ethics_Approvals/](../00_Governance/Ethics_Approvals/), [AI_Use_Disclosure.md](AI_Use_Disclosure.md) |

---

## How to use

1. **Before starting a new agent workflow:** Review each section; check off items that are satisfied.
2. **Gap remediation:** For unchecked items, reference the AegisLab mapping to close gaps.
3. **Periodic review:** Re-assess when adding automation (Zapier, Auto-Processor, new agents) or scaling.
4. **Committee defensibility:** This checklist supports transparency about agentic AI readiness in proposals and defenses.

---

## Related

- [Human_in_the_Loop_Map.md](../09_Operations/Human_in_the_Loop_Map.md) — Where the PI approves or decides
- [Academic_Integrity_Policy.md](Academic_Integrity_Policy.md) — Human authority, AI disclosure
- [Proposal_Readiness_Checklist.md](../08_Defense/Proposal_Defense/Proposal_Readiness_Checklist.md) — Pre-submission
- [Governance_Checklist.md](../02_Agents/11_Ethics_Governance_Risk/Outputs/Governance_Checklist.md) — IRB, ethics, compliance
