# Cursor IDE Configuration - AegisLab

## Workspace
- **Root:** Open `AegisLab` (repository root) so all paths in agent prompts resolve.
- **Local path:** `C:\Users\kelvi\OneDrive - cybervetssolutions.com\AegisLab`

## Agent Invocation Checklist
1. Open `02_Agents/[AgentNN_Name]/Role_Charter.md` and `Prompt_Templates.md`.
2. Copy the **Reproducibility Block** from Prompt_Templates; fill Session_Date, Model_Used, Assumptions, Output_Path.
3. Select model per `09_Operations/Model_Routing.md` (Daily Driver → often Sonnet 4.5; Deep Dive/Review → Opus 4.6 or GPT-5.2).
4. Paste the chosen template (Daily Driver / Deep Dive / Review/QA) into chat; fill **Context** and **Inputs provided**.
5. After response: save outputs to specified paths; add reproducibility block to file header; log session in `09_Operations/Session_Logs/`.

## Session Log Filename
`09_Operations/Session_Logs/YYYY-MM-DD_AgentNN_Name_ShortID.md`

## Rules (Optional .cursor/rules or project rule)
- Use repository-relative paths (e.g., `02_Agents/01_PI_Orchestrator/Outputs/`).
- Do not override PI authority; mark "Decision Required: PI" where appropriate.
- Include reproducibility block in new agent output files.
- Reference `00_Governance/Academic_Integrity_Policy.md` and `AI_Use_Disclosure.md` for AI use.
