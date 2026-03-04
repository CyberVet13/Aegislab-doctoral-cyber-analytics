# Zapier Setup Checklist — AegisLab

Quick reference for connecting AegisLab to Zapier.

---

## 1. First Zap: GitHub Push → Slack

| Step | Action |
|------|--------|
| 1 | Go to [zapier.com](https://zapier.com) → **Create Zap** |
| 2 | **Trigger:** GitHub → **New Commit** |
| 3 | Connect GitHub, select `CyberVet13/Aegislab-doctoral-cyber-analytics` |
| 4 | **Action:** Slack → **Send Channel Message** |
| 5 | Message: `AegisLab: New push to {{branch}} by {{pusher}}` |
| 6 | **Test** → **Publish** |

**Or use template:** [Send new GitHub commits to Slack](https://zapier.com/webintent/create-zap?template=1608)

---

## 2. GitHub Secrets (optional — for zapier-push workflow)

If using `.github/workflows/zapier-push.yml`:

| Step | Action |
|------|--------|
| 1 | GitHub repo → **Settings** → **Secrets and variables** → **Actions** |
| 2 | Add: `ZAPIER_DEPLOYMENT_KEY`, `MAIN_ID`, `MAIN_APP_KEY`, `BASE_URL` |

---

## 3. Schedule Reminder

| Step | Action |
|------|--------|
| 1 | **Trigger:** Schedule by Zapier → **Every Week** (Monday 9am) |
| 2 | **Action:** Slack or Gmail → Send reminder |
| 3 | Message: `Weekly AegisLab: Check Review Queue` |

---

## 4. Webhook → Agent Run (advanced)

| Step | Action |
|------|--------|
| 1 | Start API: `python 09_Operations/Workflow_API/app.py` |
| 2 | Expose: `ngrok http 8002` → copy HTTPS URL |
| 3 | **Trigger:** Schedule or Webhooks catch |
| 4 | **Action:** Webhooks by Zapier → **POST** |
| 5 | URL: `https://YOUR-NGROK-URL/run-agent` |
| 6 | Body: `{"input_path":"10_Input/brief.md","agent_num":2,"template_type":"Daily Driver","output_path":"11_Results/artifact.md"}` |

---

## Quick links

- [Full Zapier README](README.md)
- [Workflow API](../Workflow_API/README.md)
- **Launch:** Double-click `Launch_Zapier_GitHub_Slack.bat` to open the GitHub→Slack template
