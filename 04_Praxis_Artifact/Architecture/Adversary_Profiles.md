---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 04)
Prompt_Summary: Adversary profiles for threat model; defensive research scope only.
PI_Review_Status: Draft
---

# Adversary Profiles — Threat Model v1

**Context:** AegisLab Security Detection Pipeline; defensive understanding only (SEAS 8400). No offensive or unauthorized activity.

---

## Profile A — Evasion-focused adversary

- **Objective:** Reduce effective detection rate (evade detection or poison inputs so that the artifact underperforms).
- **Capabilities:** Can influence or craft input data (e.g., log injection, obfuscation); cannot assume full control of pipeline or data sources.
- **Relevance to RQ1:** Artifact evaluation (detection rate pre/post) measures resilience to evasion to the extent that test data or baseline includes evasion attempts; otherwise baseline vs. improved detection logic is the comparison.
- **In-scope techniques (defensive view):** Data manipulation (T1565), indicator removal / log evasion (T1070), obfuscation (T1027).

---

## Profile B — Integrity / confidentiality adversary

- **Objective:** Tamper with pipeline data or exfiltrate detection results / config.
- **Capabilities:** Network or local access to pipeline components; moderate sophistication.
- **Relevance:** Informs Zero Trust and control placement (Agent 05), encryption and access control (Agent 06); not primary driver of detection-rate metric.
- **In-scope concerns:** Unauthorized access to ingest or output; data at rest/transit (mitigate via controls and crypto).

---

## Use in threat model

- **Threat_Model_v1.md** references these profiles; top threats prioritize evasion (Profile A) and pipeline integrity/confidentiality (Profile B).
- **PI approval:** Confirm adversary assumptions and scope before committee or publication; document in Change_Log if updated.

---

**Last Updated:** 2025-02-06
