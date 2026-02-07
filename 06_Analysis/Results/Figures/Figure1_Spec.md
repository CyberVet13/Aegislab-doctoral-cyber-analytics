# Figure 1 — Detection Rate: Pre vs. Post (Spec)

**Purpose:** Communicate primary result for RQ1 (detection rate improvement).  
**Source:** Visualization_Design.md. Generate when analysis is run.

---

## Spec

- **Chart type:** Bar chart (pre vs. post) with error bars (95% CI).
- **X-axis:** Period (e.g., "Baseline (pre)", "Post artifact").
- **Y-axis:** Detection rate (proportion 0–1 or %); label clearly.
- **Data:** Output from analysis script (pre/post detection rate, 95% CI); path 06_Analysis/Statistical/ or Results/.
- **Tool:** R (ggplot2) or Python (matplotlib); document in Tool_Selection_Justification.
- **Accessibility:** Colorblind-safe palette; sufficient contrast.

---

## Caption (draft)

*Figure 1. Detection rate (proportion of defined security events correctly detected) at baseline (pre) and after artifact deployment (post). Error bars show 95% CI. [Source: 06_Analysis/Results/; methodology: Analysis_Plan.]*

---

## Output filename

When generated: `Figure1_Detection_Rate_Pre_Post.png` (or .svg/.pdf per report requirements). Save in this folder.

---

**Last Updated:** 2025-02-06
