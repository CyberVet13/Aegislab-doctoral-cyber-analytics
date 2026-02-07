---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 10)
Prompt_Summary: Rebuttal bank for simulated proposal defense questions.
PI_Review_Status: Draft
Caveat: Evidence-based; consistent with repository docs. PI to refine for actual defense.
---

# Rebuttal Bank — Proposal Defense (Simulated)

*One paragraph per high-priority question. Source: Methodology_Framework, Validity_Frameworks, Threat_Model, Risk_Register, Ethical_Boundaries, AI_Use_Disclosure.*

---

## Q1: Why quasi-experimental rather than random assignment?

Randomized control is typically infeasible in operational cybersecurity settings: we cannot randomly assign organizations or systems to treatment, and ethical and access constraints preclude withholding the artifact from a control group in the same environment. Quasi-experimental pre/post with a single group allows us to measure detection rate before and after artifact deployment while documenting internal validity threats and mitigations (fixed window, stable instrumentation, timeline documentation). This approach is consistent with applied security and engineering doctorate praxis [*cite*].

---

## Q2: How have you addressed internal validity (history, instrumentation)?

We documented five internal validity threats—history, maturation, testing, instrumentation, selection—and specified mitigations in our Validity_Frameworks document. For history, we document the timeline and known external events and can run sensitivity analyses excluding shock periods. For instrumentation, we hold the measurement definition and data source constant between pre and post and document any change. We use a fixed measurement window and the same population and procedures at both time points to limit maturation and testing effects. Selection is addressed through explicit inclusion criteria and reporting of attrition.

---

## Q3: Sample size and power; what if you cannot achieve it?

Our analysis plan specifies a target power of 0.80 and requires a power analysis once the primary metric and effect size are set; we will document n, alpha, power, and effect size in the methodology. If achievable sample size is below the powered n, we will state this as a limitation, report confidence intervals and effect sizes, and avoid overclaiming null results. We will not interpret a non-significant result as evidence of no effect without considering power and interval width.

---

## Q4: Operational definition of detection rate and pre/post consistency?

Detection rate is defined as the proportion of defined security events correctly detected by the artifact (or baseline) in a specified time window. The operational definition, data source, and window are documented in our Metrics_Definitions and held constant for pre and post. The evaluation harness in our architecture computes the metric from artifact outputs and ground truth using the same definition in both periods; this is specified in our Performance_Criteria and Analysis_Plan.

---

## Q11: Ethical boundaries and no offensive activity?

We have an explicit Ethical_Boundaries_Statement. Our research is defensive only: we do not conduct penetration testing, exploit development, or unauthorized access. The threat model describes threats for defensive understanding and mitigation design; we do not use malware or offensive tools. All data and systems are authorized. We document this in the proposal and in our governance materials and will communicate it clearly in the defense.

---

## Q12: AI use disclosure and documentation?

We follow our Academic_Integrity_Policy and AI_Use_Disclosure. All AI-assisted work is logged in session logs; file-level metadata and the Authorship_Log track contribution. Our methodology chapter includes the required disclosure statement: AI tools were used as research assistants under PI supervision; all content was reviewed and validated by the PI; intellectual contribution and conclusions are the PI’s. We do not cite AI as an authority; all claims trace to primary sources. Committee can review our usage logs and governance docs.

---

**Last Updated:** 2025-02-06  
**Expand:** Add rebuttals for Q5–Q10, Q13–Q15 as needed; align with final proposal text.
