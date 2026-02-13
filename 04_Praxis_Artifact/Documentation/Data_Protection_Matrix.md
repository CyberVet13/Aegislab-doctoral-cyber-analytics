---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 06)
Prompt_Summary: Data protection matrix for pipeline (what, where, how).
PI_Review_Status: Draft
---

# Data Protection Matrix — AegisLab Security Detection Pipeline

**Source:** Cryptographic_Design, Key_Management_Spec, System_Architecture_v1.

---

| Data / asset | Location | Protection | Notes |
|--------------|----------|------------|-------|
| Ingest input (logs/telemetry) | Ingest interface | Schema validation; optional integrity (hash); no PII without approval | Per Metrics_Definitions |
| Detection outputs | Output store (SQLite/Parquet) | AES-256-GCM at rest; access control; no PII in evaluation path without approval | Key per Key_Management_Spec |
| Inter-component (if over network) | In-transit | TLS 1.2+ (prefer 1.3) | Lab: localhost may be documented as trusted |
| Config / detection rules | Versioned repo or secure store | Integrity (e.g., SHA-256); optional signing if required | No secrets in repo |
| Keys | Key store (software or KMS) | Access control; never in logs or code | Per Key_Management_Spec |

---

**Classification:** Pipeline data is internal/research unless PI classifies otherwise; PII requires IRB and 00_Governance.

---

**Last Updated:** 2025-02-06
