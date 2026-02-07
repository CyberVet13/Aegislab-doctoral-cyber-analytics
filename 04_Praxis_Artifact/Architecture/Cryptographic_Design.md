---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 06)
Prompt_Summary: Cryptographic design for pipeline data at rest/transit; from Zero_Trust_Design.
PI_Review_Status: Draft
Modifications: [PI to confirm compliance (FIPS/NIST) and key custody]
---

# Cryptographic Design — AegisLab Security Detection Pipeline

**Source:** Zero_Trust_Design (data at rest/transit), Threat_Model_v1 (confidentiality).  
**Scope:** Pipeline output store and optional inter-component communication. Lab deployment: software key storage acceptable; operational may require HSM/KMS (PI to set).

---

## 1. Algorithms selected

| Use case | Algorithm | Key size / parameters | Rationale (NIST) |
|----------|-----------|------------------------|------------------|
| Data at rest (output store) | AES-256-GCM | 256-bit key | NIST SP 800-38D; confidentiality and integrity |
| Data in transit (if sensitive) | TLS 1.3 or TLS 1.2 with AES-GCM | — | NIST; prefer TLS 1.3 |
| Integrity (optional: config, critical data) | SHA-256 | 256-bit output | NIST FIPS 180-4; do not use for signatures (use HMAC-SHA256 if needed) |
| Digital signature (if needed for provenance) | RSA-PSS or ECDSA P-256 | 2048-bit RSA or P-256 | NIST SP 800-186; for config or artifact signing if required |

*No custom crypto; no MD5, SHA-1 for signatures, or DES.*

---

## 2. Data at rest

- **Scope:** Output store (e.g., SQLite, Parquet) containing detection results and evaluation inputs.
- **Control:** Encrypt at rest using AES-256-GCM; key from Key_Management_Spec (software-stored for lab; KMS/HSM for operational if PI requires).
- **Classification:** Per 00_Governance and Metrics_Definitions; no PII in pipeline without IRB and data governance approval.

---

## 3. Data in transit

- **Scope:** Ingest → detection → store (if over network or untrusted host boundary).
- **Control:** TLS 1.2+ (prefer 1.3) for any network links; same host / localhost may rely on OS and document assumption.
- **Limitation:** Lab single-host deployment may treat internal traffic as trusted; document and upgrade for operational.

---

## 4. Key management (summary)

- **Lifecycle:** Generation, storage, rotation, revocation, destruction — see Key_Management_Spec.md.
- **Custody:** PI or designated owner; no key material in logs or code.
- **Compliance:** NIST SP 800-57; FIPS 140-2 if PI specifies (e.g., operational).

---

## 5. Zero Trust alignment

- Encryption supports Zero Trust data pillar (Zero_Trust_Design); least privilege and access control remain primary (Agent 05).

---

## 6. Limitations

- No side-channel or physical security analysis; no claim beyond algorithm and key-size standards.
- Lab: software key storage; operational: consider HSM/KMS per PI and compliance.

---

**Last Updated:** 2025-02-06  
**Next:** Key_Management_Spec, Data_Protection_Matrix; PI to confirm compliance and key custody.
