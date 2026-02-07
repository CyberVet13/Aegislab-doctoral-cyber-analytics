# GitHub Workflows - AegisLab

## Repository
- **Remote:** https://github.com/CyberVet13/Aegislab-doctoral-cyber-analytics
- **Local:** Clone into `AegisLab` workspace; sync with OneDrive path as needed.

## Suggested Workflows (Optional)
- **Markdown lint:** On push/PR, run markdownlint (or similar) on `00_Governance/`, `01_Program_Context/`, `02_Agents/` to enforce structure.
- **No automated deployment** of research content; committee-facing outputs are committed after PI approval.

## Branch Strategy
- **main:** Approved, committee-ready artifacts; protect with PR + PI review.
- **develop / feature branches:** Drafts and work-in-progress; merge to main after PI approval.
- Avoid force-push to main; preserve audit trail.

## .gitignore Recommendations
- API keys, secrets, local `.env`.
- Large or sensitive data in `05_Data/Raw/` or `Processed/` if not to be shared (document in `05_Data/README.md`).
- Optionally: `09_Operations/Session_Logs/*` if logs contain full prompts; otherwise use sanitized logs and commit.

## Branch Protection (Recommended)
- Require pull request and at least one approval (PI) for changes to `00_Governance/`, `07_Writing/`, `08_Defense/`, and `01_Program_Context/Alignment_Matrix.md`.
