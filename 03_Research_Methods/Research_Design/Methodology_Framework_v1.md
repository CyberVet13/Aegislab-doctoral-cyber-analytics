---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 02 Deep Dive)
Prompt_Summary: Full methodology framework following PI approval of quasi-experimental design.
PI_Review_Status: Draft
Modifications: [PI to add research questions and refine constraints]
---

# Methodology Framework v1 — Praxis Research Design

**Design approved:** 2025-02-06 (Decision Log: `09_Operations/Decision_Logs/2025-02-06_Decision_Research_Design_Approach.md`)

---

## 1. Research Questions

*Replace with your exact RQs when finalized.*

- **RQ1:** Does the praxis artifact improve **detection rate** (proportion of defined security events correctly detected) compared to baseline in the target context? *Substitute another primary metric (e.g., mean time to detect) if preferred; update Metrics_Definitions and Analysis_Plan in parallel.*
- **RQ2:** (Optional) What operational or contextual factors are associated with variation in [metric]? (exploratory; can be descriptive.)
- **Scope:** Cybersecurity analytics; single organizational or lab context unless otherwise justified.

---

## 2. Recommended Methodology

- **Primary design:** Quasi-experimental, pre/post, single group.
- **Rationale:** (1) Engineering doctorate praxis requires an applied artifact with measurable outcomes. (2) Randomized control is typically infeasible in operational cybersecurity environments (access, ethics, unit of analysis). (3) Pre/post allows before/after comparison of key metrics (e.g., detection rate, mean time to detect, false positive rate) with explicit handling of internal validity threats (see `03_Research_Methods/Validity_Frameworks/Threats_and_Mitigations.md`).
- **Alternatives considered:** Matched comparison group (revisit if comparable group becomes available); case study (weaker causal inference; reserve for supplementary narrative).

---

## 3. Validity Summary

- **Internal:** History, maturation, testing, instrumentation, selection — mitigations documented in Validity_Frameworks.
- **External:** Generalizability limited to similar contexts; document population and setting.
- **Construct:** Operational definitions for all measured constructs; align with SEAS 8410/8414 metrics.
- **Conclusion:** Statistical power and alpha; document assumptions and sensitivity.

---

## 4. Data Collection Plan (overview)

- **Pre period:** Baseline metrics (defined per artifact) over defined window; same instrumentation and population as post.
- **Intervention:** Praxis artifact implementation (or deployment in lab/target environment).
- **Post period:** Same metrics, same window length where feasible; document any instrumentation or population changes.
- **Provenance:** All data documented in `05_Data/README.md`; no PII in analysis without IRB and governance approval.

---

## 5. Analysis Approach

- **Primary:** Pre vs. post comparison (e.g., paired or repeated-measures appropriate to metric type); effect size and confidence intervals; significance testing with stated alpha and power justification (Agent 02/07 to detail).
- **Assumptions:** Normality, independence, or robust alternatives; document checks (Agent 07).
- **Limitations:** Causal claims are tentative; confounds and alternative explanations stated in report.

---

## 6. Timeline and Resources

*Adjust dates to your program and proposal.*

- **Phase 1 — Design & approval:** Proposal defense; methodology and validity approved (e.g., Month 1–2).
- **Phase 2 — Baseline data:** Pre-intervention metrics collected; instrumentation stable (e.g., Month 2–3).
- **Phase 3 — Implementation:** Artifact deployed in target environment; post period defined (e.g., Month 4–6).
- **Phase 4 — Post data & analysis:** Post metrics collected; analysis per analysis plan; write-up (e.g., Month 6–8).
- **Resources:** Data access, tools (per SEAS 8414), compute; IRB if human subjects or sensitive data.

---

## 7. Handoff to Other Agents

- **Agent 03 (Praxis Architect):** Evaluation requirements = metrics in §4; baseline and post data needs; benchmarking criteria.
- **Agent 07 (Security Data Analytics):** Analysis plan = §5; assumption checks; reproducibility (code, seeds, environment).
- **Agent 09 (Writing):** Methodology chapter = this framework + Validity_Frameworks; limitations = §5 and validity doc.

---

## 8. Committee Defense Preview

- **Why quasi-experimental?** Operational constraints; RCT infeasible; pre/post with documented mitigations is standard in applied security research.
- **How internal validity addressed?** Explicit threat table and mitigations; sensitivity and documentation.
- **Limitations?** Causal inference limited; generalizability to similar contexts only; honest statement in report.

---

**Last Updated:** 2025-02-06  
**Next:** Replace [primary metric] in RQ1 with your chosen metric; lock timeline to proposal. Agent 07 analysis plan and Agent 03 evaluation requirements produced (see below).
