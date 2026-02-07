# Getting Started — Git and GitHub (AegisLab)

Use these steps to connect your local AegisLab folder to GitHub and make the first push. Run commands from the repository root (`AegisLab`).

---

## Option A: This folder is not yet a Git repo

1. **Initialize and first commit**
   ```powershell
   cd "C:\Users\kelvi\OneDrive - cybervetssolutions.com\AegisLab"
   git init
   git add .
   git status
   git commit -m "Initial AegisLab scaffold: governance, 11 agents, operations, README"
   ```

2. **Add remote and push**
   ```powershell
   git remote add origin https://github.com/CyberVet13/Aegislab-doctoral-cyber-analytics.git
   git branch -M main
   git push -u origin main
   ```
   If the repo already has content (e.g., a README created on GitHub), you may need:
   ```powershell
   git pull origin main --allow-unrelated-histories
   git push -u origin main
   ```

3. **Authentication**  
   Use a personal access token (PAT) or SSH key if prompted. GitHub no longer accepts account password for Git over HTTPS.

---

## Option B: Repo already exists and you cloned it

If you cloned `Aegislab-doctoral-cyber-analytics` into this path and then added the scaffold here:

1. **Check remote**
   ```powershell
   cd "C:\Users\kelvi\OneDrive - cybervetssolutions.com\AegisLab"
   git remote -v
   ```

2. **Stage, commit, push**
   ```powershell
   git add .
   git status
   git commit -m "Initial AegisLab scaffold: governance, 11 agents, operations, README"
   git push -u origin main
   ```

---

## Recommended after first push

- **Branch protection:** On GitHub, set branch protection for `main` (e.g., require PR and review for changes to `00_Governance/`, `07_Writing/`, `08_Defense/`).
- **.gitignore:** Already present; adjust if you exclude `09_Operations/Session_Logs/` or `05_Data/` contents (see `.gitignore` comments).
- **Workflow:** Use feature branches for drafts; merge to `main` after PI approval for committee-facing artifacts.

---

## Using Git when a parent folder has its own .git

If running `git status` from AegisLab shows changes outside AegisLab (e.g. other folders or "Cyber PM Agent"), another Git repo is active (often in your user profile). To use **only** the AegisLab repo from a terminal in this folder, set:

```powershell
cd "C:\Users\kelvi\OneDrive - cybervetssolutions.com\AegisLab"
$env:GIT_DIR = (Get-Location).Path + "\.git"
$env:GIT_WORK_TREE = (Get-Location).Path
```

Then run `git status`, `git add`, `git commit`, `git push` as usual. They will apply only to AegisLab. (Close the terminal or unset `GIT_DIR` and `GIT_WORK_TREE` when done.)

---

## OneDrive and permission notes

- **OneDrive:** If this path is under OneDrive, ensure Git and OneDrive do not conflict (e.g., avoid real-time syncing of large or frequently changing files in `05_Data/` if excluded from Git). Document data location and sync rules in `05_Data/README.md`.
- **Permission denied on `git init`:** If you see "could not write config file" or "unable to unlink config.lock" when running `git init` inside AegisLab, try:
  1. Closing OneDrive sync for this folder temporarily, or
  2. Running PowerShell or Git Bash as Administrator from the AegisLab folder, or
  3. Running `git init` from a non-synced copy of AegisLab, then copying the `.git` folder back if needed.

---

**Last Updated:** 2025-02-06
