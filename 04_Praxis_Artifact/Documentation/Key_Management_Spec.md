---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 06)
Prompt_Summary: Key management lifecycle for pipeline crypto.
PI_Review_Status: Draft
---

# Key Management Spec — AegisLab Security Detection Pipeline

**Source:** Cryptographic_Design.md.  
**Scope:** Keys used for data-at-rest encryption (and optional signing) of pipeline output/store.

---

## 1. Lifecycle

| Phase | Practice |
|-------|----------|
| **Generation** | Use OS or library CSPRNG (e.g., OpenSSL, Python secrets); no hardcoded keys. |
| **Storage** | Lab: encrypted key store (e.g., env or secret file with restricted permissions); Operational: KMS/HSM per PI. |
| **Rotation** | Rotate data-encryption keys on schedule (e.g., annual) or on compromise; re-encrypt data or use key hierarchy. |
| **Revocation** | Revoke and destroy keys on compromise or decommission; document in Change_Log. |
| **Destruction** | Secure wipe; no key material in logs, backups, or code. |

---

## 2. Access control

- Only pipeline components and authorized evaluation harness need read access to decrypted output; key access restricted to minimal set of identities (Zero Trust).

---

## 3. Audit

- Log key use (e.g., encrypt/decrypt events) without logging key material; retain per 00_Governance and data retention policy.

---

## 4. Lab vs. operational

- **Lab:** Software key storage acceptable; document assumption; rotate and restrict access.
- **Operational:** Prefer KMS/HSM and formal key policy; PI to set.

---

**Last Updated:** 2025-02-06
