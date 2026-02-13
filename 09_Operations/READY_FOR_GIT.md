# Ready for Git — AegisLab

*Check before running git commands. See GETTING_STARTED_GIT.md for full steps.*

---

## Pre-commit checklist

- [ ] No secrets or API keys in any file (check .env, configs, scripts).
- [ ] .gitignore is in place (repo root); adjust if you exclude Session_Logs or 05_Data contents.
- [ ] Sensitive data: if 05_Data/Raw or Processed contains confidential data, ensure it is excluded or use a separate private repo for data.
- [ ] OneDrive: if you see "permission denied" or lock errors on `git init`, try closing OneDrive sync for this folder temporarily or run from a non-synced copy (see GETTING_STARTED_GIT troubleshooting).

---

## Commands (run from AegisLab root)

```powershell
cd "C:\Users\kelvi\OneDrive - cybervetssolutions.com\AegisLab"
git init
git add .
git status
git commit -m "AegisLab scaffold: governance, 11 agents, methodology, artifact, defense prep, index"
git remote add origin https://github.com/CyberVet13/Aegislab-doctoral-cyber-analytics.git
git branch -M main
git push -u origin main
```

*If the repo already exists on GitHub with content, you may need `git pull origin main --allow-unrelated-histories` before push. Use a personal access token (PAT) or SSH for authentication.*

---

## After first push

- Consider branch protection for `main` (e.g. require PR for 00_Governance, 07_Writing, 08_Defense).
- Keep Session_Logs and Decision_Logs in sync with local work; re-commit and push as needed.

---

**Last Updated:** 2025-02-06
