---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 11)
Prompt_Summary: Risk register for praxis research and pipeline; from Agent 04 handoff and governance.
PI_Review_Status: Draft
Modifications: [PI to set likelihood/impact and accept residual risks]
---

# Risk Register — AegisLab Doctoral Research and Pipeline

**Source:** Threat_Model_v1, Mitigation_Recommendations (Agent 04), 00_Governance, pipeline scope.  
**Use:** Proposal and report; committee defense; SEAS 8499/8188.

---

## Research and methodology risks

| ID | Risk | Likelihood | Impact | Mitigation | Residual |
|----|------|------------|--------|------------|----------|
| R1 | Internal validity threats (history, maturation, instrumentation) affect causal claim | M | M | Validity_Frameworks mitigations; fixed window, same instrumentation | Document in limitations |
| R2 | Low power or small sample reduces ability to detect effect | M | M | Power analysis; report CIs and effect size; state as limitation | Accept or extend data collection |
| R3 | Generalizability limited to similar contexts | H | M | State in limitations; do not overgeneralize | Accept |

---

## Data and pipeline risks

| ID | Risk | Likelihood | Impact | Mitigation | Residual |
|----|------|------------|--------|------------|----------|
| R4 | Pipeline data tampering or evasion (T1565, T1070) | M | M | Input validation; detection-rate evaluation (RQ1) | Document; monitor drift |
| R5 | Unauthorized access to pipeline or output (confidentiality) | L | M | Zero Trust, encryption, least privilege (Agent 05, 06) | Accept with controls |
| R6 | PII or sensitive data in pipeline without approval | L | H | No PII in evaluation path per Metrics_Definitions; IRB if needed | Governance and audit |

---

## Ethics and compliance risks

| ID | Risk | Likelihood | Impact | Mitigation | Residual |
|----|------|------------|--------|------------|----------|
| R7 | AI use not disclosed or overstated | L | H | 00_Governance AI_Use_Disclosure; Authorship_Log; committee statement | Compliance |
| R8 | Research perceived as offensive or unauthorized | L | H | Ethical_Boundaries_Statement; defensive scope only; no unauthorized access | Document and communicate |

---

## Residual risks (summary)

- **Accepted:** R3 (generalizability), R5 (with controls), R7/R8 (with governance).
- **Documented:** R1, R2, R4 in limitations and validity sections.
- **PI to confirm:** Likelihood/impact ratings and acceptance; update when scope changes.

---

**Last Updated:** 2025-02-06  
**Next:** Review with Agent 10 (defense Q&A); cite in methodology and discussion.
