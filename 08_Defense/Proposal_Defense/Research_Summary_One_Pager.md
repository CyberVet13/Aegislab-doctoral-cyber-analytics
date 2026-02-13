# Research Summary — One Page (Proposal / Committee)

*Use for defense opening, committee packet, or quick reference. Align with full proposal.*

---

## Problem and research question

- **Problem:** Detection of security events in [target context] may be improved by a structured detection pipeline; baseline detection rate is [X or TBD].
- **RQ1:** Does the praxis artifact (AegisLab Security Detection Pipeline) improve **detection rate** (proportion of defined security events correctly detected) compared to baseline in the target context?
- **RQ2 (optional):** [Exploratory factor question or omit.]

---

## Design and methodology

- **Design:** Quasi-experimental, pre/post, single group (RCT infeasible in operational cybersecurity context).
- **Validity:** Internal, external, construct, and conclusion validity addressed with documented threats and mitigations (see Validity_Frameworks).
- **Data:** Pre period (baseline) → artifact deployment → post period; same metric definition and instrumentation; provenance in 05_Data.
- **Analysis:** Pre vs. post comparison (paired or appropriate test); effect size and 95% CI; alpha 0.05; reproducibility via versioned code and environment (Analysis_Plan).

---

## Artifact (praxis)

- **Name:** AegisLab Security Detection Pipeline (or [your title]).
- **Purpose:** Ingest security-relevant data, run detection logic, produce outputs for detection-rate evaluation.
- **Key components:** Ingest → Detection engine → Output/store → Evaluation harness (detection rate pre/post).
- **Security:** Threat model (defensive only); Zero Trust and Defense-in-Depth; cryptographic design for data at rest/transit; controls mapped to D3FEND/NIST (see Architecture, Threat_Model, Zero_Trust_Design).

---

## Timeline (example)

- Phase 1: Design and approval (proposal defense).
- Phase 2: Baseline data collection.
- Phase 3: Artifact deployment; post data collection.
- Phase 4: Analysis and write-up; final defense.

*Adjust to your program dates.*

---

## Limitations

- Causal inference is tentative (quasi-experimental).
- Generalizability limited to similar contexts.
- Sample size and power may limit detection of effects; CIs and effect sizes reported.
- AI tools used with full disclosure and PI review (00_Governance/AI_Use_Disclosure).

---

## Program alignment

- SEAS 8400 (attack types/mitigations), 8405 (Zero Trust, MITRE), 8410 (metrics), 8414 (analytics-to-policy), 8415 (crypto), 8499 (methodology/proposal), 8188 (praxis/final report). See 01_Program_Context/Alignment_Matrix.md.

---

**Last Updated:** 2025-02-06 | **Owner:** PI
