# Figure 2 — Effect Size and 95% CI (Spec)

**Purpose:** Support significance and magnitude of pre/post difference (RQ1).  
**Source:** Visualization_Design.md. Generate when analysis is run.

---

## Spec

- **Chart type:** Interval plot or forest-style (point estimate and 95% CI for difference: post − pre).
- **X-axis:** Difference in detection rate (or effect size); mark 0 (null).
- **Y-axis:** Single comparison (e.g., "Detection rate (post − pre)").
- **Data:** Difference, 95% CI, optional effect size from analysis script.
- **Tool:** R (ggplot2) or Python (matplotlib); same as Figure 1.
- **Accessibility:** Colorblind-safe; show interval clearly.

---

## Caption (draft)

*Figure 2. Difference in detection rate (post − pre) with 95% CI. [Interpretation: CI excludes 0 → significant improvement; effect size per Analysis_Plan.]*

---

## Output filename

When generated: `Figure2_Effect_CI.png` (or .svg/.pdf). Save in this folder.

---

**Last Updated:** 2025-02-06
