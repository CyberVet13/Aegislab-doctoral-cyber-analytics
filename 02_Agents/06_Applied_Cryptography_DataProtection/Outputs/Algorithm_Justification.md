---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 06)
Prompt_Summary: Algorithm justification for pipeline crypto (NIST references).
PI_Review_Status: Draft
---

# Algorithm Justification — Pipeline Cryptography

**Alignment:** SEAS 8415; committee-defensible; NIST references only.

---

- **AES-256-GCM:** NIST SP 800-38D (recommended for confidentiality and authentication); 256-bit key per SP 800-57.
- **TLS 1.2 / 1.3:** NIST SP 800-52; TLS 1.3 preferred where available.
- **SHA-256:** FIPS 180-4; integrity only (not for signatures; use HMAC-SHA256 or signature scheme if needed).
- **RSA-PSS / ECDSA P-256:** NIST SP 800-186 (ECDSA), FIPS 186-4; for config or artifact signing if required.

No custom or non-standard algorithms; no MD5, SHA-1 for signatures, or DES.

---

**Last Updated:** 2025-02-06
