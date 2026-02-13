---
Session_Date: 2025-02-06
Source: Methodology_Framework_v1 + Agent 02 handoff to Agent 03
Prompt_Summary: Evaluation requirements for Engineering Praxis Architect (metrics, baseline, benchmarking).
PI_Review_Status: Draft
---

# Evaluation Requirements — Handoff to Agent 03 (Praxis Architect)

*Per Agent 02 Role_Charter: "To Agent 03 (Praxis Architect)". Source: `03_Research_Methods/Research_Design/Methodology_Framework_v1.md` and `02_Agents/07_Security_Data_Analytics/Outputs/Metrics_Definitions.md`.*

---

## Evaluation requirements

- **What the artifact must measure/demonstrate:** Improvement (or non-inferiority) on **detection rate** (and optional secondary metrics) from pre to post in a single group; operational definitions in Metrics_Definitions.
- **Metrics needed:** Primary metric (see Analysis_Plan and Metrics_Definitions); optional secondary (e.g., false positive rate, counts) for context.
- **Baseline data:** Pre-period values of primary (and secondary) metrics over defined window; same instrumentation and population as post.
- **Benchmarking standards:** Industry or literature benchmarks for [metric] where available (e.g., “MTTD < X minutes”); otherwise pre/post comparison is the benchmark.
- **Reproducibility requirements:** Instrumentation and data collection documented; metrics computable from artifact and/or existing logs; versioned analysis in `06_Analysis/Statistical/`.

---

## Constraints for artifact design

- Artifact must produce (or enable collection of) detection rate (and any secondary metrics) in a way that allows pre/post comparison (same definition, same source type).
- Baseline data collection must be feasible before artifact deployment (or use historical data if justified and documented).

---

**Last Updated:** 2025-02-06  
**Consumer:** Agent 03 (Engineering Praxis Architect) — use for Performance_Criteria and architecture instrumentation points.
