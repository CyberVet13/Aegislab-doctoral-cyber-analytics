# Tool Configurations - AegisLab Doctoral Research

## Purpose
This directory holds configuration documentation and examples for tools used in the AegisLab environment: Cursor IDE (agent invocation, rules), GitHub (repository, workflows, branch policy), and any local scripts for session logging or model routing. Configurations support auditability, reproducibility, and academic integrity.

---

## Contents

| Item | Description | Location |
|------|-------------|----------|
| **Cursor Rules** | Project-specific rules for AI behavior and agent context | `.cursor/rules/` (repo root) or doc here |
| **Cursor Agent Context** | How to invoke agents (which file to open, which prompt template) | This README + 02_Agents/*/Prompt_Templates.md |
| **GitHub Workflows** | CI/linting, branch protection, release tagging (if used) | `.github/workflows/` (see below) |
| **Session Logging** | How to log sessions (manual or script) | 09_Operations/Session_Logs/ + this README |

---

## Cursor IDE Configuration

### Recommended Setup
- **Workspace:** Open repository root `AegisLab` so that paths in prompts (e.g., `00_Governance/`, `02_Agents/01_PI_Orchestrator/`) resolve correctly.
- **Agent invocation:** For each agent session:
  1. Open the agent’s `Role_Charter.md` and `Prompt_Templates.md` (or the specific template section).
  2. Copy the **Reproducibility Block** and fill in date, model, assumptions, output path.
  3. Paste the appropriate template (Daily Driver / Deep Dive / Review/QA) into the chat and fill in context and inputs.
  4. After the response, save any generated content to the specified output path and add the reproducibility block to the file header.
  5. Create or append a session log in `09_Operations/Session_Logs/YYYY-MM-DD_AgentNN_Name_SessionID.md` with prompt summary, model, output path, and PI decision.

### Cursor Rules (Optional)
If using `.cursor/rules/` or a single project rule file, include:
- Always use repository-relative paths (e.g., `02_Agents/01_PI_Orchestrator/Outputs/`).
- Never override PI authority; mark "Decision Required: PI" where appropriate.
- Include the reproducibility block in any new file created for an agent output.
- Reference `00_Governance/Academic_Integrity_Policy.md` and `AI_Use_Disclosure.md` for AI use and disclosure.

### Model Selection in Cursor
- Use Cursor’s model selector to choose GPT-5.2, Claude Opus 4.6, or Claude Sonnet 4.5 per `09_Operations/Model_Routing.md`.
- Record the model used in the session log and in the output file’s reproducibility block.

---

## GitHub Configuration

### Repository
- **Primary:** https://github.com/CyberVet13/Aegislab-doctoral-cyber-analytics  
- **Local clone:** Ensure local path matches workspace (e.g., `C:\Users\kelvi\OneDrive - cybervetssolutions.com\AegisLab` or clone into that path).
- **Branch strategy:** Document in repo (e.g., `main` for approved work; `develop` or feature branches for drafts). PI approves merges to `main` for committee-facing artifacts.

### Suggested Workflows (Optional)
- **Lint/format:** Markdown or YAML lint on push/PR (e.g., markdownlint, prettier) to keep governance and agent docs consistent.
- **No automated deployment** of research content; all committee-facing outputs are approved and committed by PI.

### Branch Protection (Recommended)
- Protect `main`: require PR and PI review before merge for governance and 07_Writing, 08_Defense changes.
- Do not force-push to `main`; keep history for audit trail.

### .gitignore
- Exclude: `09_Operations/Session_Logs/*` if logs contain full prompts/responses (or use sanitized logs only). Alternatively, keep session logs in repo with clear "CONFIDENTIAL - PI only" notice and restrict repo access.
- Exclude: Local secrets, API keys, `05_Data/Raw/` or `Processed/` if data cannot be shared. Use `05_Data/README.md` to document provenance and access.

---

## Session Logging

### Manual Logging
1. Create file: `09_Operations/Session_Logs/YYYY-MM-DD_AgentNN_ShortName_SessionID.md`.
2. Include: Date, model, agent number/name, prompt template type, brief prompt summary, output path(s), PI decision or follow-up.
3. Optionally paste full prompt and response (or store in Archive if too large); ensure no sensitive data if committed.

### Session Log Template
```markdown
# Session Log - YYYY-MM-DD - Agent NN - [ShortName]

- **Model:** [GPT-5.2 | Claude Opus 4.6 | Claude Sonnet 4.5]
- **Template:** [Daily Driver | Deep Dive | Review/QA]
- **Prompt summary:** [1–2 sentences]
- **Output path(s):** [List]
- **PI decision:** [Approved / Revise / Deferred / Rejected]
- **Notes:** [Optional]
```

---

## Decision Logs

- **Location:** `09_Operations/Decision_Logs/YYYY-MM-DD_Decision_[Topic].md`
- **Content:** Decision request (from Agent 01 or PI), options, recommendation, PI decision, rationale, impact. Supports audit trail and committee defensibility.

---

**Last Updated:** 2025-02-06  
**Owner:** Principal Investigator
