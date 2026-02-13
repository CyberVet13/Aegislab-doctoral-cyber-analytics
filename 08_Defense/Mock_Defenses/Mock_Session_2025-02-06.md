---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 10)
Prompt_Summary: Mock defense session log (5 Q&A pairs); proposal defense simulation.
PI_Review_Status: Draft
Caveat: Simulation only; not actual committee feedback.
---

# Mock Defense Session — 2025-02-06 (Proposal)

*Simulated Q&A for preparation. Prioritize advisor and committee feedback.*

---

## Q1 (Methodology): Why quasi-experimental rather than random assignment?

**Answer (summary):** RCT is infeasible in our context—we cannot randomly assign organizations or withhold the artifact from a control in the same environment. Pre/post single group with documented validity mitigations is standard in applied security research and supports our RQ (detection rate improvement).

**Feedback note:** Ensure one citation for quasi-experimental use in security/analytics; add to Gap_Analysis (done).

---

## Q2 (Validity): How did you address internal validity?

**Answer (summary):** We have a structured Validity_Frameworks document with five internal validity threats and mitigations: history (timeline, sensitivity analysis), maturation (fixed window, same procedures), testing (non-reactive measures where possible), instrumentation (constant definition and source), selection (inclusion criteria, attrition reporting).

**Feedback note:** Committee may ask for one concrete example; prepare “instrumentation” or “history” example.

---

## Q3 (Technical): What are the main components of the pipeline and how do they support evaluation?

**Answer (summary):** Ingest (collect/normalize data), detection engine (rules or ML producing detections), output store (results for evaluation), evaluation harness (computes detection rate pre/post). The harness uses the same operational definition in both periods so detection rate is comparable.

**Feedback note:** Align with System_Architecture_v1; consider one simple diagram for slides.

---

## Q4 (Ethics): How have you disclosed AI use?

**Answer (summary):** We have an AI_Use_Disclosure and Academic_Integrity_Policy. The methodology chapter includes the required disclosure statement; we maintain session logs and an Authorship_Log. All AI-assisted content is reviewed and validated by the PI; we do not cite AI as an authority.

**Feedback note:** Have the exact disclosure sentence ready to read if asked.

---

## Q5 (Limitations): What are the main limitations?

**Answer (summary):** Causal inference is tentative (quasi-experimental); generalizability is limited to similar contexts; sample size and power may limit what we can detect. We state these in the limitations section and rely on effect sizes and CIs rather than overclaiming.

**Feedback note:** Do not minimize limitations; committee appreciates honesty.

---

**Next:** Run another mock session after draft revision; incorporate advisor feedback into Rebuttal_Bank and Gap_Analysis.
