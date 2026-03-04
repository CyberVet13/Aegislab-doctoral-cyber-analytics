# Gaps Summary — Consolidated View

**Purpose:** Single reference for all identified gaps across proposal defense, human-in-the-loop, and agentic readiness. Use to prioritize and track closure.

**Source:** Gap_Analysis.md, Human_in_the_Loop_Map.md, Agentic_AI_Readiness_Checklist.md.

---

## 1. Proposal Defense (Gap_Analysis)

| Gap | Status | Remediation | Location |
|-----|--------|-------------|----------|
| Citations for quasi-experimental rationale | Open | Add 2–3 peer-reviewed or NIST/SEAS citations | Methodology_Chapter_Draft; References |
| Power/sample size not computed | Open | Run power analysis when effect size set; add paragraph and table | Analysis_Plan; report |
| RQ2 (optional) not decided | Addressed | Sentence added; PI to include or remove | Methodology_Framework_v1 |
| Technology justification in narrative | Addressed | Sentence added citing Tool_Selection_Justification | Methodology_Chapter_Draft |
| Lab vs. operational assumption | Addressed | Lab deployment sentence in methodology | Methodology_Chapter_Draft; Zero_Trust_Design |
| IRB status placeholder | Open | Insert actual status; use Ethics_Approvals template | Methodology_Chapter_Draft; Ethics_Approvals/README |
| Governance_Checklist incomplete | Open | Complete checklist before submission | Governance_Checklist.md |
| Ethical_Boundaries certification | Open | PI to sign/date | Ethical_Boundaries_Statement.md |
| Results section placeholder | Open | Replace with actual results after analysis | Results_Ethics_Limitations_Draft.md |
| Figure 1 and 2 not generated | Open | Generate per Figure1_Spec, Figure2_Spec when analysis run | 06_Analysis/Results/Figures/ |
| Abstract and conclusion not drafted | Open | Add when proposal structure locked | 07_Writing/Drafts/ |
| Slide deck not created | Addressed | Template added | Proposal_Defense_Slides_Template.md |
| Rehearsal with advisor | Open | Schedule mock defense; incorporate feedback | — |

---

## 2. Human-in-the-Loop

| Gap | Status | Remediation | Location |
|-----|--------|-------------|----------|
| Gradio defensive-scope confirmation | Addressed | Checkbox added (same as Streamlit) | Gradio_App/app.py |
| CLI confirm-defensive-scope | Addressed | `--confirm-defensive-scope` flag | run_agent_cli.py |
| Workflow API confirm_defensive_scope | Addressed | API parameter when topic triggers | Workflow_API |
| Streamlit batch approve | Addressed | Checkboxes + Approve selected | Streamlit_App |
| Zapier/Agent 02 automation | Addressed | Documented | Human_in_the_Loop_Map.md |

---

## 3. Agentic AI Readiness

| Item | Status | Notes |
|------|--------|------|
| All 12 checklist items | Open | PI self-assessment; see Agentic_AI_Readiness_Checklist.md |

---

## 4. Other Placeholders

| Item | Status | Remediation |
|------|--------|-------------|
| Learning outcomes | Open | Replace or clarify placeholders in 01_Program_Context/Learning_Outcomes/ |
| System_Architecture key components | Partial | Table present; PI to confirm tech stack |
| Methodology citation placeholders | Open | PI to add `[*cite*]` references |

---

## 5. Cannot Be Fully Automated

- Actual analysis results and figures (require real analysis)
- IRB status and Ethical_Boundaries certification (PI action)
- Advisor rehearsal (human action)
- Agentic AI Readiness self-assessment (PI judgment)
- Citations (PI verification against primary sources)

---

**Last Updated:** 2025-02-21  
**Review:** Update after each major draft or gap closure.
