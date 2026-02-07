---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 03)
Prompt_Summary: Performance criteria for praxis artifact evaluation; from methodology and Agent 02 handoff.
PI_Review_Status: Draft
Modifications: [PI to set artifact scope and confirm primary metric]
---

# Performance Criteria — Praxis Artifact

**Source:** `02_Agents/02_Applied_Research_Methodologist/Outputs/Evaluation_Requirements_For_Agent03.md`, `03_Research_Methods/Research_Design/Methodology_Framework_v1.md`, `02_Agents/07_Security_Data_Analytics/Outputs/Metrics_Definitions.md`.

---

## Primary evaluation criterion

- **Metric:** **Detection rate** (proportion of defined events correctly detected). Change if RQ1 uses a different primary metric.
- **Comparison:** Pre vs. post (single group); improvement (or non-inferiority) with statistical test and effect size per Analysis_Plan.
- **Success (for reporting):** [e.g., “Statistically significant improvement (α = 0.05) with meaningful effect size” or “95% CI for difference excludes 0 in favor of improvement.”]  
  *PI to define “success” for proposal and report.*

---

## Instrumentation

- Artifact (and/or existing pipeline) must produce or expose data needed to compute the primary metric in pre and post periods.
- Same operational definition and data source in both periods (see Metrics_Definitions).

---

## Baseline and post windows

- **Pre (baseline):** [e.g., 30 days] before intervention; stable instrumentation.
- **Post:** [e.g., 30 days] after artifact deployment; same length where feasible.
- Document any gap or change in data availability.

---

## Ties to research questions and standards

- **RQ1:** Directly addressed by primary criterion.
- **SEAS 8410/8414:** Metrics and tool choices justified in Metrics_Definitions and Tool_Selection_Justification; decision pathway in Agent 08 outputs when available.

---

**Last Updated:** 2025-02-06  
**Next:** When artifact architecture exists (Agent 03 Deep Dive), map these criteria to specific components and data flows in `04_Praxis_Artifact/Architecture/`.
