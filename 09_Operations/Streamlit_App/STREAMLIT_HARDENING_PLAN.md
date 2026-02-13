# Streamlit UI Hardening Plan — Doctoral Defense & Publication Readiness

**Purpose:** Bring the AegisLab Streamlit operational console to committee- and publication-ready standard with clear security, reproducibility, and disclosure controls.

**Scope:** `09_Operations/Streamlit_App/` and `aegislab_ui/`; integration with `00_Governance/`, `02_Agents/`, `09_Operations/Session_Logs/`, `09_Operations/Decision_Logs/`.

---

## 1. Security & Access Control

### 1.1 Authentication & Authorization

- [ ] **Define access model**
  - Single-PI only vs. lab members vs. committee view-only.
  - Document in `00_Governance/` or `09_Operations/Tool_Configurations/Streamlit_UI_Workflow.md`.
- [ ] **Implement authentication**
  - Option A: Streamlit’s built-in password protection (`streamlit run app.py --server.runOnSave false` + `.streamlit/secrets.toml` with hashed password).
  - Option B: OAuth/SSO (e.g., Azure AD, institutional IdP) via `streamlit-authenticator` or custom middleware.
  - Option C: Reverse proxy (IIS, nginx) with Windows/auth or SAML in front of Streamlit; app trusts `X-Forwarded-User` or similar (document trust boundary).
- [ ] **Authorization rules**
  - PI: full access (Run Agent, Review Queue, Approve/Archive, Settings, Audit).
  - Lab member (if any): Run Agent + view own sessions; no Approve, no Settings.
  - Committee/view-only: read-only Dashboard + Governance Audit (no Run, no Review Queue, no Settings).
  - Enforce in UI (hide/disable controls) and in backend (reject actions by role).
- [ ] **Secrets management**
  - No API keys in repo or in Streamlit `secrets.toml` committed to git.
  - Use environment variables or a secret store (e.g., Azure Key Vault, AWS Secrets Manager) and document in `.env.example` and README.
  - Rotate keys on schedule; document rotation in `09_Operations/`.

### 1.2 Input Validation & Injection

- [ ] **Validate all user inputs**
  - Agent number: allow only 1–11.
  - Template type: allow only Daily Driver, Deep Dive, Review/QA.
  - Output path: block `..`, absolute paths, and paths outside `AEGISLAB_ROOT`; allow only repo-relative paths matching `^[0-9A-Za-z_/.-]+$` or similar.
  - Research objective / assumptions / constraints: max length (e.g., 10k chars); strip or reject control characters.
- [ ] **Prevent prompt injection**
  - Treat user-filled fields as untrusted; do not allow them to override system instructions or template structure.
  - Consider a fixed “user context” block that is clearly delimited from the template (e.g., `## User context\n...\n## Template`) so model sees a single, structured prompt.
- [ ] **Logging**
  - Do not log raw API keys; log only model id, agent, template type, and path hashes (prompt_payload_sha256, model_output_sha256) in session logs.

### 1.3 Session & State

- [ ] **Session handling**
  - Rely on Streamlit’s session state for in-memory state (review queue, filters); document that no server-side session store is used unless added.
  - If adding server-side sessions (e.g., DB or Redis), ensure session IDs are unpredictable and tied to authenticated identity.
- [ ] **Sensitive data in UI**
  - Never display API keys or full secrets in the UI; show only “Configured” / “Not set” in Settings.
  - Sanitize file content preview (e.g., strip accidental secrets) before showing in Review Queue or Governance Audit.

### 1.4 Dependency & Supply Chain

- [ ] **Pin dependencies**
  - Use `requirements.txt` with exact versions (e.g., `streamlit==1.28.0`) or export from `pip freeze` for reproducibility.
  - Add `pip-audit` or `safety` to CI; document in `09_Operations/Tool_Configurations/` or GitHub_Workflows.
- [ ] **Vulnerability scanning**
  - Run `pip audit` (or equivalent) in CI; fail or warn on known vulnerabilities; document process in hardening doc.
  - Optional: SBOM generation (e.g., `cyclonedx-py`) for committee or sponsor review.

---

## 2. Reproducibility & Audit Trail

### 2.1 Determinism & Versioning

- [ ] **Model parameters**
  - Log in every session: model id, temperature, max_tokens, seed (if supported); store in session log and in prompt_payload JSON (or equivalent).
  - Prefer fixed seed where supported (e.g., OpenAI `seed`) for reproducibility runs; document in Model_Routing or Streamlit_UI_Workflow.
- [ ] **Code and config versioning**
  - Record in session log or in a single “run manifest”: git commit hash (or tag) of the repo at run time, and Streamlit app version (e.g., `aegislab_ui.__version__`).
  - Optional: record `requirements.txt` hash or lockfile hash for the environment used.
- [ ] **Template versioning**
  - Record path and, if feasible, file hash (or last-modified) of the loaded `Prompt_Templates.md` in session log so template changes are traceable.

### 2.2 Logging & Traceability

- [ ] **Session log completeness**
  - Every Run Agent execution must produce exactly one session log: `09_Operations/Session_Logs/YYYY-MM-DD_AgentXX_SessionID.md`.
  - Mandatory fields: date, agent, template type, model, output path, prompt_payload_sha256, model_output_sha256; optional: prompt_payload summary (truncated), tool config.
- [ ] **Decision log**
  - Every manual model override and every PI action (Approve / Request changes / Archive) must append to `09_Operations/Decision_Logs/` with date and topic.
- [ ] **Authorship log**
  - Every new artifact must append one row to `00_Governance/Authorship_Log.md` with artifact name, path, date, AI/PI contribution, validation method, status, approval date.
- [ ] **Immutability**
  - Do not overwrite or delete session logs or decision log entries; append-only. If a correction is needed, add a new “Correction” entry with reference to the original.

### 2.3 Integrity & Hashing

- [ ] **Hashes**
  - Compute and store SHA-256 of: (1) canonical JSON of prompt payload (model, messages, temperature, etc.), (2) raw model output text.
  - Use UTF-8 encoding and a defined canonicalization (e.g., sorted keys for JSON) and document in README or Streamlit_UI_Workflow.
- [ ] **Committee packet**
  - Governance Audit “committee packet” ZIP should include session logs and decision logs; optionally add a manifest file (list of files + hashes) inside the ZIP for verification.

---

## 3. AI Disclosure & Governance

### 3.1 Disclosure in Artifacts

- [ ] **Front-matter**
  - Every AI-assisted artifact must include YAML front-matter with: AI_Assisted, Session_Date, Model_Used, Prompt_Summary, PI_Review_Status, Output_Path (per `00_Governance/AI_Use_Disclosure.md`).
  - Enforce in app: inject on write; on Approve, update PI_Review_Status to Approved and record in Decision_Log.
- [ ] **Authorship log alignment**
  - Status and approval date in Authorship_Log must stay in sync with PI actions in Review Queue (e.g., on Approve, update row to Approved and set Approval Date).
- [ ] **Defensive-scope confirmation**
  - When topic triggers defensive-scope heuristic, require explicit checkbox and log the confirmation in session or decision log.

### 3.2 Human-in-the-Loop

- [ ] **No auto-approval**
  - No artifact is marked Approved without an explicit PI action in Review Queue.
  - If “auto-approve” is ever added for a specific workflow, document exception and rationale in governance.
- [ ] **Review Queue as gate**
  - All Run Agent outputs enter Review Queue; PI must Approve, Request changes, or Archive; document in Streamlit_UI_Workflow.
- [ ] **Change requests**
  - “Request changes” must create a decision log entry and, if desired, a placeholder or stub for “revision notes” (e.g., in Decision_Log or in artifact path) so the request is traceable.

### 3.3 Policy and Safety

- [ ] **Safety checks**
  - Retain and document pattern-based checks (e.g., no malware/exploit generation); log when a prompt is blocked and do not call the model.
- [ ] **Defensive scope**
  - Keep “Defensive Scope Confirmation” checkbox and warning text; reference `00_Governance/` or Academic_Integrity_Policy for full policy.
- [ ] **Block writes outside repo**
  - All output paths must resolve under `AEGISLAB_ROOT`; reject and log any attempt to write outside (path traversal, absolute path escape).

---

## 4. Deployment & Environment

### 4.1 Configuration

- [ ] **AEGISLAB_ROOT**
  - Support only environment variable (or equivalent); no hardcoded absolute paths in code.
  - Document in README and .env.example; validate at startup and show clear error if not set (or if fallback is used, log a warning).
- [ ] **API keys**
  - Load from environment (or secure secret store); fail fast at Run Agent if required key is missing, with message “Set OPENAI_API_KEY / ANTHROPIC_API_KEY”.
- [ ] **.env**
  - Do not commit `.env`; provide `.env.example` with placeholders; mention in README and .gitignore.

### 4.2 Running the App

- [ ] **Startup checks**
  - On app load: verify `AEGISLAB_ROOT` (or fallback) exists and is a directory; verify required dirs (`00_Governance`, `02_Agents`, `09_Operations/Session_Logs`, etc.) exist; show Dashboard warning if validation fails.
- [ ] **Port and binding**
  - Document how to run (e.g., `streamlit run app.py`); if deployed behind reverse proxy, document recommended bind (e.g., 127.0.0.1) and proxy headers (e.g., X-Forwarded-For, X-Forwarded-Proto).
- [ ] **HTTPS**
  - For any non-local deployment, require HTTPS at the proxy; document in Tool_Configurations or deployment doc.

### 4.3 Reproducibility of Environment

- [ ] **Python version**
  - Specify in README (e.g., Python 3.10 or 3.11); optional: use `pyproject.toml` with `requires-python`.
- [ ] **Lockfile**
  - Provide `requirements.txt` with pinned versions; optional: generate from `pip freeze` and document how to reproduce env.
- [ ] **Optional container**
  - If Docker is used, provide Dockerfile and document how to build/run; include AEGISLAB_ROOT mount and env vars.

---

## 5. Testing & Quality

### 5.1 Unit Tests

- [ ] **repo_validator**
  - Tests for path validation (allowed_output_path, is_under_root); reject `..`, absolute, and paths outside root.
- [ ] **metadata**
  - Tests for inject_frontmatter and parse_frontmatter; required fields present; round-trip.
- [ ] **router**
  - Tests for get_recommended_model and resolve_model_id for known agents/templates.
- [ ] **safety**
  - Tests for check_prompt (blocked vs allowed); defensive_scope_confirmation_required.
- [ ] **logging_audit**
  - Tests for sha256_text; write_session_log creates file with expected fields; append_decision_log and append_authorship_log append only (mock or temp dir).

### 5.2 Integration Tests

- [ ] **End-to-end flow (mocked LLM)**
  - Run Agent with mocked model_gateway (no real API call); assert session log created, artifact has front-matter, review queue updated, authorship log appended.
- [ ] **Review Queue**
  - Approve action updates artifact front-matter and decision log; Archive/Request changes create decision log entry.
- [ ] **Governance Audit**
  - Generate ZIP; assert expected log files present; optional: assert manifest or hash list.

### 5.3 Linting & Formatting

- [ ] **Lint**
  - Run ruff (or flake8/pylint) on `aegislab_ui/` and `pages/`; fix or document exceptions.
- [ ] **Format**
  - Black or ruff format; apply consistently and document in README or Tool_Configurations.

---

## 6. Documentation & Handoff

### 6.1 In-Repo Documentation

- [ ] **README (Streamlit_App)**
  - Quick start, prerequisites, env vars, how to run, link to Streamlit_UI_Workflow and Model_Routing.
- [ ] **Streamlit_UI_Workflow.md**
  - Workflow checklist, path rules, session/decision log naming, integration points (templates, governance, routing).
- [ ] **Model_Routing.md**
  - Keep aligned with router defaults (Daily Driver / Deep Dive / Review-QA → model); document overrides and rationale logging.
- [ ] **Hardening plan (this document)**
  - Place in `09_Operations/Streamlit_App/STREAMLIT_HARDENING_PLAN.md`; reference from README and Tool_Configurations.

### 6.2 Committee- and Publication-Ready

- [ ] **Disclosure statement**
  - All committee-facing docs reference `00_Governance/AI_Use_Disclosure.md`; Streamlit UI is listed as an AI-assisted tool with scope (operational console, logging, no autonomous decisions).
- [ ] **Reproducibility statement**
  - Short paragraph in README or governance: how to reproduce a run (commit, env, model params, hashes in session log); link to Session_Logs and Decision_Logs.
- [ ] **Security summary**
  - One-page summary: authentication (if any), how secrets are handled, input validation, no writes outside repo; link to this hardening plan.

### 6.3 Handoff Checklist

- [ ] **Runbook**
  - How to start/stop the app; where logs and config live; how to rotate API keys; how to add a new agent or template.
- [ ] **Known limitations**
  - Document: in-memory review queue (lost on restart unless persisted); optional future work (auth, persistence, container).
- [ ] **Contact / owner**
  - Principal Investigator and repo URL in README; last-updated date on key docs.

---

## 7. Implementation Order (Suggested)

1. **Security & path safety** — Input validation, path checks, no secrets in logs (Sections 1.2, 1.4, 3.3).
2. **Reproducibility & hashing** — Session log fields, git/version in logs, hashes (Sections 2.1–2.3).
3. **Governance alignment** — Front-matter, Authorship_Log sync, defensive-scope log (Sections 3.1–3.3).
4. **Auth (if required)** — Choose model; implement and document (Section 1.1).
5. **Tests** — Unit then integration (Section 5).
6. **Deployment & env** — Startup checks, HTTPS, lockfile (Sections 4.2–4.3).
7. **Documentation** — README, workflow, hardening refs, committee summary (Section 6).

---

**Document version:** 1.0  
**Last updated:** 2025-02-07  
**Owner:** Principal Investigator
