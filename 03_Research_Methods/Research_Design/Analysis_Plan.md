---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 07)
Prompt_Summary: Analysis plan for quasi-experimental pre/post design; tests, power, assumptions, reproducibility.
PI_Review_Status: Draft
Modifications: [PI to confirm primary metric and sample size]
---

# Analysis Plan — Quasi-Experimental Pre/Post (Single Group)

**Source:** `03_Research_Methods/Research_Design/Methodology_Framework_v1.md`  
**Design:** Pre/post, single group; primary outcome = **detection rate** (proportion of defined events correctly detected). *Change if RQ1 uses a different primary metric.*

---

## 1. Primary Analysis

- **Objective:** Compare pre vs. post for **detection rate** (proportion).
- **Data:** One value per unit (e.g., system, team, or time window) per period (pre, post); paired or repeated-measures structure.
- **Test (choose one, justify):**
  - **Paired t-test** if metric is continuous and differences are approximately normal; report mean difference, 95% CI, Cohen’s d.
  - **Wilcoxon signed-rank** if normality of differences is violated; report median difference, CI, rank-biserial or equivalent.
  - **McNemar or binomial** if metric is binary (e.g., detected yes/no) and paired; report proportion change, CI. *For detection rate as proportion, paired t on proportions or binomial/McNemar depending on data structure; document choice.*
- **Alpha:** 0.05 (two-tailed unless one-tailed pre-specified and justified).
- **Software/code:** Versioned in `06_Analysis/Statistical/`; environment and random seed (if any) documented.

---

## 2. Power and Sample Size

- **Target power:** 0.80.
- **Effect size:** [PI/Agent 07 to set: e.g., “medium” (d ≈ 0.5) or minimum meaningful change in [metric].]
- **Sample size:** Compute from power analysis (e.g., G*Power, R pwr); document n, α, power, effect size. For paired t, assume moderate pre-post correlation (e.g., r = 0.5) if unknown.
- **Feasibility:** If achievable n is below powered n, state as limitation and report CIs; avoid overclaiming null results.
- **Methodology paragraph:** When effect size is set, add one short paragraph and table to methodology or report summarizing: target n, achieved n (if known), power, effect size, and alpha.

---

## 3. Assumptions to Check (before reporting)

| Assumption | Check | Action if violated |
|------------|--------|----------------------|
| Normality of differences (paired t) | Shapiro–Wilk or Q–Q; report result | Use Wilcoxon signed-rank or report both |
| Independence | Design (no repeated units across periods unless repeated-measures) | Document; if clustered, consider cluster-robust or multilevel |
| Same instrumentation pre/post | Documentation | Already in validity mitigations; note in report |

---

## 4. Reproducibility

- **Code:** `06_Analysis/Statistical/` — script(s) for data read, checks, test, effect size, with comments.
- **Random seed:** Set if any resampling or randomization (e.g., `set.seed(20250206)` or equivalent).
- **Environment:** Note software and version (e.g., R 4.x, Python 3.x + packages) in README or script header.
- **Data:** Paths to `05_Data/Processed/` (or Raw with processing steps); no hardcoded local-only paths in committed code.

---

## 5. Secondary / Exploratory (optional)

- Descriptive stats (pre/post means, SDs, counts).
- Subgroup or sensitivity analyses only if pre-specified; otherwise label exploratory and do not overinterpret.

---

## 6. Handoff to Agent 08 and 09

- **Agent 08:** Primary result (point estimate, CI, p-value, effect size) and recommendation for figure(s) (e.g., pre/post bar or paired difference plot).
- **Agent 09:** One-sentence result statement and limitations paragraph for results section.

---

**Last Updated:** 2025-02-06  
**Owner:** Agent 07; PI approves test choice and power/sample size.
