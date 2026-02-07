# First Run — AegisLab Agent Session

Use this guide to run your first agent session, log it, and confirm the workflow. Recommended first agent: **02 Applied Research Methodologist** (Daily Driver).

---

## 1. Prerequisites

- [ ] Cursor IDE open with workspace root = `AegisLab`
- [ ] Model access: Claude Sonnet 4.5 (or per `09_Operations/Model_Routing.md`)
- [ ] You have read `00_Governance/Academic_Integrity_Policy.md` and `00_Governance/AI_Use_Disclosure.md`

---

## 2. Open agent context

1. Open `02_Agents/02_Applied_Research_Methodologist/Role_Charter.md`
2. Open `02_Agents/02_Applied_Research_Methodologist/Prompt_Templates.md`
3. In Cursor, select model **Claude Sonnet 4.5** (or per Model_Routing)

---

## 3. Build the prompt

Copy the **Reproducibility Block** from Prompt_Templates.md and fill it in:

```
---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5
Prompt_Version: v1.0
Assumptions: First run; no existing research design yet.
Output_Path: 03_Research_Methods/Research_Design/ or 02_Agents/02_Applied_Research_Methodologist/Outputs/
PI_Review_Required: Yes
---
```

Then copy the **Daily Driver** template (full "1. Daily Driver" section from Prompt_Templates.md) and fill in:

- **Context:** e.g., "First run. I need a short list of validity threats for a quasi-experimental pre/post design in cybersecurity analytics."
- **Inputs provided:** e.g., "None yet; assume a single treatment group and before/after metrics."
- **Task:** e.g., "Identify 3–5 internal validity threats and one mitigation each. Use handoff format from Role_Charter."

Paste the combined block + template into Cursor chat and send.

---

## 4. Save output and add reproducibility

1. Create or open a file, e.g. `02_Agents/02_Applied_Research_Methodologist/Outputs/First_Run_Validity_Notes.md`
2. Paste or adapt the agent’s response into that file
3. At the top of the file, add the same reproducibility block (Session_Date, Model_Used, Prompt_Summary, PI_Review_Status: Draft)

---

## 5. Create session log

1. Create `09_Operations/Session_Logs/2025-02-06_Agent02_Applied_Research_Methodologist_FirstRun.md`
2. Use this content (adjust as needed):

```markdown
# Session Log - 2025-02-06 - Agent 02 - Applied Research Methodologist (First Run)

- **Model:** Claude Sonnet 4.5
- **Template:** Daily Driver
- **Prompt summary:** Validity threats for quasi-experimental pre/post design; 3–5 internal validity threats with mitigations.
- **Output path(s):** 02_Agents/02_Applied_Research_Methodologist/Outputs/First_Run_Validity_Notes.md
- **PI decision:** Draft — to be reviewed and refined.
- **Notes:** First run to validate workflow and logging.
```

---

## 6. Optional: Authorship log

If this output will be used in a committee-facing document, add an entry to `00_Governance/Authorship_Log.md` (Active Artifacts Log table) with artifact name, path, date, AI %, PI %, validation method, status, approval date.

---

## 7. Next steps

- Run another agent (e.g., 01 PI/Orchestrator for a status or task list)
- Replace learning outcome placeholders in `01_Program_Context/Learning_Outcomes/` with official syllabi when available
- Initialize Git and connect to GitHub using `09_Operations/GETTING_STARTED_GIT.md`

**Last Updated:** 2025-02-06
