# Claude GitHub Connector — Troubleshooting

**Error:** "The connector still cannot access your repository"
- Server error - Can't fetch the main page
- Permissions error - Can't access the API or raw files

---

## Step 1: Reconfigure the Claude GitHub App

1. Go to **GitHub** → **Settings** → **Applications** → **Installed GitHub Apps**
2. Find **Claude** → click **Configure**
3. Under **Repository access:**
   - If "Only select repositories" — ensure `Aegislab-doctoral-cyber-analytics` is selected
   - Try **All repositories** temporarily to test
4. Click **Save**
5. If prompted, approve any new permissions

**Direct link:** https://github.com/settings/installations

---

## Step 2: Uninstall and Reinstall (if Step 1 fails)

1. **Uninstall:** GitHub → Settings → Applications → Installed GitHub Apps → Claude → **Uninstall**
2. **Reinstall:** Go to https://github.com/apps/claude/installations/new
3. Select **Only select repositories** → add `Aegislab-doctoral-cyber-analytics`
4. Complete the install
5. In **Claude** (claude.ai or desktop): Disconnect and reconnect GitHub in Settings

---

## Step 3: Check Repository Visibility

**Known issue:** Claude sometimes has trouble with personal-account repos.

- If **Aegislab-doctoral-cyber-analytics** is under your personal account (e.g. `CyberVet13`), try:
  - **Option A:** Temporarily make the repo **public** to test access
  - **Option B:** Move the repo under an **organization** if you have one

---

## Step 4: Use Alternative — Add Files Manually

If the connector still fails, use **Claude Projects** instead:

1. In Claude → **Projects** → Create or open a project
2. Click **+** in the knowledge section
3. **Paste a file URL** directly, e.g.:
   `https://github.com/CyberVet13/Aegislab-doctoral-cyber-analytics/blob/main/README.md`
4. Or **clone locally** and add files from your `AegisLab` folder on disk

---

## Step 5: Verify GitHub App Permissions

The Claude GitHub App needs:
- **Contents:** Read (to fetch files)
- **Metadata:** Read (repository info)

These are usually granted by default. If you reinstalled, ensure you accept all requested permissions.

---

## Quick Links

- [Configure installed apps](https://github.com/settings/installations)
- [Reinstall Claude app](https://github.com/apps/claude/installations/new)
- [Claude GitHub integration help](https://support.claude.com/en/articles/10167454-using-the-github-integration)
