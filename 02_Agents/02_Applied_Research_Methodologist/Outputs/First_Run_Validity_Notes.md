---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5
Prompt_Summary: Validity threats for quasi-experimental pre/post design; internal validity threats and mitigations.
PI_Review_Status: Draft
Modifications: [None yet — PI to review]
---

# First-Run Example: Internal Validity Threats (Quasi-Experimental Pre/Post)

*This file illustrates the output of a first Agent 02 Daily Driver session. Replace or extend with your own content after PI review.*

## Design context
- Single group (or treatment group), before/after metrics
- Cybersecurity analytics (e.g., detection rate, mean time to detect before vs. after an artifact or intervention)
- No randomized control; quasi-experimental

## Internal validity threats (3–5) and mitigations

| Threat | Brief description | Mitigation |
|--------|-------------------|------------|
| **History** | External events (e.g., new threats, policy change) between pre and post could explain change | Document timeline; note and control for known external events; sensitivity analysis excluding periods with known shocks |
| **Maturation** | Natural change in operators, tools, or environment over time | Fixed measurement window; same population and procedures at pre and post; baseline trend if data available |
| **Testing** | Pre-test or repeated measurement affects post scores | Use non-reactive measures where possible; separate pilot from main measurement; document any training or familiarization |
| **Instrumentation** | Change in how the outcome is measured (e.g., tool upgrade, log source change) | Hold instrumentation constant or measure and control for version; document all data collection details |
| **Selection** | Differences between groups (if multiple groups) or attrition | Define inclusion criteria; report attrition; if comparative, document selection and consider propensity or matching (per Agent 02 full design) |

## Handoff to full methodology (Agent 02 Deep Dive)
- Expand to external, construct, and conclusion validity in `03_Research_Methods/Validity_Frameworks/Threats_and_Mitigations.md`
- Tie mitigations to data collection and analysis plan in `03_Research_Methods/Research_Design/`
- Committee defense: prepare 1–2 sentence rationale for "why quasi-experimental" and "how we addressed internal validity"

## PI action
- [ ] Review and edit as needed
- [ ] Move or copy content to `03_Research_Methods/Validity_Frameworks/` when approved
- [ ] Log in Authorship_Log if used in committee-facing document
