---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 08)
Prompt_Summary: Figure list and visualization design for primary result (detection rate pre/post) and metrics.
PI_Review_Status: Draft
---

# Visualization Design — Praxis Results and Metrics

**Source:** `03_Research_Methods/Research_Design/Analysis_Plan.md`, `02_Agents/07_Security_Data_Analytics/Outputs/Metrics_Definitions.md`, Performance_Criteria.  
**Audience:** Committee (proposal and final report); optional operator view if artifact includes dashboard.

---

## 1. Proposed figures for report

| # | Title | Purpose | Data source | Chart type | Caption (draft) |
|---|--------|---------|-------------|------------|------------------|
| 1 | Detection rate: pre vs. post | Communicate primary result for RQ1 | Analysis output (pre/post detection rate, CI) | Bar chart with error bars (95% CI) or paired comparison | Figure 1. Detection rate (proportion) at baseline (pre) and after artifact deployment (post). Error bars show 95% CI. [Source: 06_Analysis/Results/; methodology: Analysis_Plan.] |
| 2 | Effect size and confidence interval | Support significance and magnitude | Difference in detection rate, 95% CI, effect size | Interval plot or forest-style | Figure 2. Difference in detection rate (post − pre) with 95% CI. [Interpretation: excludes 0 → significant improvement; effect size per Analysis_Plan.] |
| 3 | (Optional) Pre/post by subgroup or time | Sensitivity or exploratory | Processed data | Bar or line | Only if pre-specified; otherwise label exploratory. |

---

## 2. Design and accessibility

- **Axes and units:** Label axes (e.g., "Detection rate (proportion)" or "Detection rate (%)"); same scale pre and post.
- **Uncertainty:** Show 95% CI or SE on all comparative figures; do not omit for narrative convenience.
- **Color:** Use colorblind-safe palette (e.g., blue/orange or viridis); sufficient contrast for print.
- **Tool:** [e.g., ggplot2 (R), matplotlib (Python)] — document in Tool_Selection_Justification; output to `06_Analysis/Results/Figures/`.

---

## 3. Dashboard (if artifact includes UI)

- **Metrics to display:** Detection rate (current window); optional: count of detections, false positive rate (if defined).
- **Refresh:** Define window (e.g., rolling 7 days); document in `04_Praxis_Artifact/Documentation/Dashboard_Spec.md` when implemented.
- **Stakeholder:** Operators for monitoring; committee for defense demo if applicable.

---

## 4. Handoff to Agent 09 (Writing)

- **Figure list:** Above table; file paths in `06_Analysis/Results/Figures/` when generated.
- **Caption drafts:** In table; expand with source and methodology in report.
- **Narrative hook:** e.g., "Figure 1 presents the primary result: detection rate improved from pre to post (95% CI excludes 0; see Analysis_Plan for test and effect size)."

---

**Last Updated:** 2025-02-06  
**Update:** When analysis is run, generate figures and save to `06_Analysis/Results/Figures/`; add exact file names to this doc.
