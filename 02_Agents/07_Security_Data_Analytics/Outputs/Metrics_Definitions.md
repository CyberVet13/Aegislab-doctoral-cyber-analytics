---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 07)
Prompt_Summary: Operational definitions for praxis evaluation metrics (pre/post design).
PI_Review_Status: Draft
---

# Metrics Definitions — Praxis Evaluation (Pre/Post)

**Purpose:** Operational definitions for metrics used in quasi-experimental pre/post evaluation. Align with SEAS 8410/8414 and RQ1 in `03_Research_Methods/Research_Design/Methodology_Framework_v1.md`.

---

## Primary metric

*Primary for RQ1; substitute if PI chooses a different metric.*

| Metric name | Operational definition | Unit | Data source | Pre/post same? |
|-------------|------------------------|------|--------------|-----------------|
| **Detection rate** | Proportion of [defined security events] correctly detected by the artifact (or baseline) in [time window, e.g., 30 days] | Proportion (0–1) or % | Artifact/SIEM logs; ground truth or labeled set | Yes |
| Mean time to detect (MTTD) | Mean time from event start to first detection in [window] | Minutes or seconds | Artifact + timestamps | Yes (optional secondary) |

---

## Secondary / contextual (optional)

| Metric name | Operational definition | Unit | Use |
|-------------|------------------------|------|-----|
| [e.g., False positive rate] | Proportion of alerts that are false positives in [window] | Proportion | Context; document if used in analysis |
| [e.g., Count of detections] | Raw count of [defined] detections in [window] | Count | Descriptive |

---

## Criteria for “same” pre/post

- Same time-window length (e.g., 30 days pre, 30 days post).
- Same population (e.g., same systems, same team).
- Same instrumentation (same tool versions, same log sources); document any change and note in limitations.

---

**Last Updated:** 2025-02-06  
**Update:** When artifact and data sources are fixed; cross-check with `04_Praxis_Artifact/Benchmarks/Performance_Criteria.md`.
