---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 09)
Prompt_Summary: Draft methodology chapter/section for proposal; from Methodology_Framework and Validity_Frameworks.
PI_Review_Status: Draft
Modifications: [PI to add citations, tighten voice, verify all claims]
---

# Methodology Chapter — Draft (Proposal / Report)

*Source: 03_Research_Methods/Research_Design/Methodology_Framework_v1.md, Validity_Frameworks/Threats_and_Mitigations.md, Analysis_Plan.md. PI must verify citations and approve before submission. For `[*cite*]` placeholders: add peer-reviewed or NIST/SEAS citations; verify against primary sources before submission.*

---

## 3.X Research Design

Technology choices (Python, SQLite, Parquet, scikit-learn) are justified in `02_Agents/07_Security_Data_Analytics/Outputs/Tool_Selection_Justification.md` and SEAS 8414 alignment; one-sentence summary: open-source, reproducible, and suitable for lab-scale detection evaluation without vendor lock-in.

This study uses a quasi-experimental, pre/post, single-group design. The primary research question is whether the praxis artifact (AegisLab Security Detection Pipeline) improves detection rate—defined as the proportion of defined security events correctly detected—compared to baseline in the target context. A single group is used because randomized control is typically infeasible in operational cybersecurity environments (access, ethics, unit of analysis); pre/post comparison with documented internal validity mitigations is consistent with applied security research practice [*cite: e.g., relevant SEAS or NIST/peer-reviewed source*].

Validity threats (internal, external, construct, conclusion) are addressed in a structured framework. Internal validity threats—history, maturation, testing, instrumentation, and selection—are mitigated through fixed measurement windows, stable instrumentation, documented timeline and external events, and explicit inclusion criteria [*see Validity_Frameworks/Threats_and_Mitigations.md*]. External validity is limited to similar contexts; the population and setting are described to bound generalizability. Construct validity is supported by operational definitions of all metrics (detection rate and any secondaries), aligned with security metrics practice [*cite SEAS 8410/8414 or NIST as appropriate*]. Conclusion validity is addressed through a priori power considerations, stated alpha, and documentation of assumption checks [*cite Analysis_Plan*].

---

## 3.X Data Collection and Analysis

Data collection consists of a pre period (baseline detection rate over a defined window), artifact deployment, and a post period (same metrics and window length where feasible). All data provenance is documented [*05_Data/README*]; no personally identifiable information is used in the evaluation pipeline without IRB and governance approval.

The primary analysis compares pre versus post detection rate using an appropriate paired or repeated-measures approach (e.g., paired t-test for continuous proportion or McNemar/binomial for binary outcomes, per Analysis_Plan). Effect size and 95% confidence intervals are reported; alpha is set at 0.05 (two-tailed unless pre-specified). Assumptions (e.g., normality of differences) are checked and reported. Reproducibility is ensured through versioned analysis code, fixed random seeds where applicable, and documented environment [*06_Analysis/Statistical/*].

---

## 3.X Ethical Considerations and AI Use Disclosure

[*Insert institutional IRB status: approved, exempt, or not required, with rationale. See 00_Governance/Ethics_Approvals/README.md for template.*] The artifact is deployed in a lab environment; full Zero Trust (e.g., mTLS, HSM) is deferred per Zero_Trust_Design and Defense_in_Depth_Map. Data handling follows [*00_Governance and Metrics_Definitions*]; no PII in the evaluation path without approval. Cybersecurity research is conducted within authorized scope only; no offensive or unauthorized testing [*Ethical_Boundaries_Statement*].

This research was conducted with assistance from AI language models (OpenAI GPT-5.2, Anthropic Claude Opus 4.6/Sonnet 4.5) used as research tools under human supervision. All AI-generated content was reviewed, validated, and substantially modified by the Principal Investigator. AI tools assisted with literature discovery, technical writing, code generation, and analytical scaffolding. All factual claims are independently verified against primary sources. The intellectual contribution, research design, and conclusions are the original work of the Principal Investigator. Complete AI usage logs are available for committee review [*per 00_Governance/AI_Use_Disclosure.md*].

---

**Next:** PI to add citations, lock RQ2 if used, and align with proposal word limit. Cross-check with 08_Defense/Proposal_Defense/Methods_QA_Prep.md for defense readiness.
