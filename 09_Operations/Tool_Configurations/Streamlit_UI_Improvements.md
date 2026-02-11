# Streamlit Console — UI Improvement Ideas

**Purpose:** Actionable ideas to make the AegisLab operational console clearer, faster to use, and more committee-ready. Implement incrementally; prioritize by PI need.

---

## Done (this pass)

- **Dashboard:** Metric cards for session count and review-queue count; clearer empty states.
- **Run Agent:** Grouped sections (Context, Output, Model, RAG); output path placeholder; recommended model shown inline; spinner and success message retained.
- **Review Queue:** Agent names (not just numbers); clearer action labels; optional confirm-for-archive note.
- **Review Queue persistence:** Queue is persisted to `09_Operations/Gradio_App/review_queue.json` and shared with Gradio and CLI (Streamlit loads on startup, saves on add/approve/request/archive). **Refresh from disk** button on Review Queue page to pick up items added by Gradio or CLI.
- **Theme:** Slightly refined colors and spacing for readability.
- **Sidebar:** Short tips expander; AEGISLAB_ROOT remains.

---

## Short-term (high impact)

| Area | Suggestion | Effort |
|------|------------|--------|
| **Run Agent** | "Use last output path" button to copy previous run’s path into the field | Low |
| **Run Agent** | Collapsible "Template preview" closed by default to reduce scroll | Low |
| **Review Queue** | Optional two-step Archive (e.g. "Archive?" → "Confirm archive") to avoid misclicks | Low |
| **Governance Audit** | Date picker instead of free-text YYYY-MM-DD; filter chips for agent | Low |
| **Dashboard** | Link/button "Open Run Agent" for quick start | Low |
| **All pages** | Consistent page subtitle and "What this page does" in one line under title | Low |

---

## Medium-term (workflow)

| Area | Suggestion | Effort |
|------|------------|--------|
| **Run Agent** | Save "favorite" output paths per agent (session state or small JSON in Operations) | Medium |
| **Review Queue** | ~~Persist queue to disk~~ ✅ Done — shared file `09_Operations/Gradio_App/review_queue.json` (Streamlit + Gradio + CLI) | — |
| **Governance Audit** | Clickable log rows that expand inline or open in a new tab (file path as `file://` link) | Medium |
| **Settings** | Editable routing table (e.g. override defaults in a config file from the UI) | Medium |
| **Dashboard** | "Last run" summary: agent, model, output path, timestamp | Medium |

---

## Longer-term (polish & committee)

| Area | Suggestion | Effort |
|------|------------|--------|
| **Theme** | Optional "high contrast" or "committee" theme (e.g. larger font, more contrast) | Medium |
| **Export** | One-click "Evidence pack" ZIP: last N session logs + decision logs + Authorship_Log snapshot | Medium |
| **Onboarding** | First-time checklist in sidebar: "API keys set?", "RAG built?", "First run done?" | Medium |
| **Accessibility** | Labels and ARIA where Streamlit allows; keyboard nav notes in README | Low–Medium |
| **Tests** | UI smoke tests (e.g. Playwright) for "Run Agent → success" and "Review Queue → Approve" | High |

---

## Usage tips (for sidebar or README)

- Use **Auto-route** unless you have a documented reason to override (override is logged).
- Build **RAG** once per repo change that affects governance/agents/methodology; then use "Augment this run" when helpful.
- **Review Queue** is persisted (shared file with Gradio and CLI); survives app restart.
- **Committee packet** (Governance Audit) ZIP includes all session + decision logs for a given run.

---

**Last updated:** 2025-02-07
