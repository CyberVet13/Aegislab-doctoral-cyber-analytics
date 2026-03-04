# AegisLab Zapier Workflows

**Purpose:** Connect AegisLab to Zapier for automation—GitHub push notifications, scheduled reminders, and webhook-triggered agent runs.

**Last Updated:** 2026-02-13

---

## Overview

Zapier connects AegisLab to your workflow tools (Slack, Gmail, Google Sheets, etc.) without code. Use it to:

1. **Get notified** when code is pushed to the AegisLab repo
2. **Schedule reminders** to check the Review Queue or run agents
3. **Trigger agent runs** via webhook when the Workflow API is exposed (ngrok or cloud)

---

## Workflow 1: GitHub Push → Slack (Recommended)

**Trigger:** New push to AegisLab repo  
**Action:** Send message to Slack channel

### Create this Zap

1. Go to [zapier.com](https://zapier.com) → **Create Zap**
2. **Trigger:** Search **GitHub** → **New Commit** (or **New Push** if available)
3. Connect your GitHub account
4. **Repository:** Select `CyberVet13/Aegislab-doctoral-cyber-analytics`
5. **Branch (optional):** Filter to `main` or `Baseline` only
6. **Action:** Search **Slack** → **Send Channel Message**
7. Connect Slack, choose channel
8. **Message Text:** `AegisLab: New push to {{branch}} by {{pusher}} — {{commit message}}`
9. **Test** → **Publish**

### Zapier template (quick start)

Use the pre-built template to get started:

**[Send new GitHub commits to Slack](https://zapier.com/webintent/create-zap?template=1608)**

Then customize: select your AegisLab repo and Slack channel.

---

## Workflow 2: GitHub Push → Gmail

**Trigger:** New push to AegisLab repo  
**Action:** Send email to PI

### Create this Zap

1. **Trigger:** GitHub → **New Commit**
2. Select repo `CyberVet13/Aegislab-doctoral-cyber-analytics`
3. **Action:** Gmail → **Send Email**
4. **To:** Your email
5. **Subject:** `AegisLab: New push to {{branch}}`
6. **Body:** `Commit by {{pusher}}: {{commit message}}`
7. **Test** → **Publish**

---

## Workflow 3: Schedule → Weekly Reminder

**Trigger:** Every Monday 9:00 AM  
**Action:** Send reminder to check Review Queue

### Create this Zap

1. **Trigger:** Schedule by Zapier → **Every Week**
2. **Day:** Monday
3. **Time:** 9:00 AM (your timezone)
4. **Action:** Slack → **Send Channel Message** (or Gmail → Send Email)
5. **Message:** `Weekly AegisLab reminder: Check Review Queue and run agents as needed.`
6. **Test** → **Publish**

---

## Workflow 4: Webhook → Trigger Agent Run (Advanced)

**Requirement:** Expose the Workflow API (e.g., ngrok or cloud deployment).

**Trigger:** Schedule or Webhooks catch  
**Action:** POST to Workflow API `/run-agent`

### Setup

1. Start Workflow API: `python 09_Operations/Workflow_API/app.py`
2. Expose with ngrok: `ngrok http 8002` → copy the HTTPS URL
3. In Zapier:
   - **Trigger:** Schedule by Zapier (e.g., daily) or Webhooks by Zapier (Catch Hook)
   - **Action:** Webhooks by Zapier → **POST**
   - **URL:** `https://YOUR-NGROK-URL/run-agent`
   - **Payload Type:** JSON
   - **Data:**
     ```json
     {
       "input_path": "10_Input/brief.md",
       "agent_num": 2,
       "template_type": "Daily Driver",
       "output_path": "11_Results/artifact.md"
     }
     ```

### Workflow API reference

| Endpoint   | Method | Body |
|------------|--------|------|
| `/run-agent` | POST | `input_path`, `agent_num`, `template_type`, `output_path`, optional `assumptions`, `constraints`, `model_override`, `override_rationale`, `confirm_defensive_scope` |
| `/health`    | GET  | — |

**Human-in-the-loop:** When input content may involve offensive security (e.g., exploit, red team), set `confirm_defensive_scope: true`. All outputs require Review Queue approval before committee-ready.

**Success:** `{ "success": true, "message": "Output written to ..." }`  
**Error:** `400` with `{ "detail": "error message" }`

---

## GitHub Actions (zapier-push)

AegisLab includes `.github/workflows/zapier-push.yml` that runs on push to `Baseline` or `main`. It uses the `zapier-push-action` and requires these GitHub secrets:

| Secret | Description |
|--------|-------------|
| `ZAPIER_DEPLOYMENT_KEY` | Zapier deployment key |
| `MAIN_ID` | Main ID (from Zapier app) |
| `MAIN_APP_KEY` | Main app key (from Zapier app) |
| `BASE_URL` | Base URL for Zapier deployment |

Add them in **GitHub repo → Settings → Secrets and variables → Actions**.

> **Note:** The `zapier-push-action` is for custom Zapier apps. For standard Zapier (zapier.com), use the built-in **GitHub** trigger as described in Workflows 1–2 above.

---

## Agents reference

| # | Agent |
|---|-------|
| 1 | PI/Orchestrator |
| 2 | Applied Research Methodologist |
| 3 | Engineering Praxis Architect |
| 4 | Cyber Threat & Adversary Analysis |
| 5 | Cybersecurity Architecture & Zero Trust |
| 6 | Applied Cryptography & Data Protection |
| 7 | Security Data Analytics |
| 8 | Visualization & Decision Support |
| 9 | Doctoral Writing & Argumentation |
| 10 | Committee & Defense Simulation |
| 11 | Ethics, Governance & Risk |

**Template types:** `Daily Driver` | `Deep Dive` | `Review/QA`

---

## Files in this folder

| File | Purpose |
|------|---------|
| `README.md` | This document |
| `ZAPIER_SETUP_CHECKLIST.md` | Quick setup checklist |
| `Launch_Zapier_GitHub_Slack.bat` | Double-click to open GitHub→Slack template in browser |

---

## Related documentation

- [BPNA_Workflow.md](../BPNA_Workflow.md) — BPMN-style process model (tasks, gateways, events)
- [Workflow_Visual.md](../Workflow_Visual.md) — 10_Input → Run Agent → Review Queue → 11_Results
- [Workflow_API/README.md](../Workflow_API/README.md) — HTTP API for Zapier
- [Streamlit_App/README.md](../Streamlit_App/README.md) — Run agents via Streamlit
