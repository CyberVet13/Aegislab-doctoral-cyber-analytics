---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 04)
Prompt_Summary: ATT&CK to D3FEND mapping for threat model v1 (defensive only).
PI_Review_Status: Draft
---

# ATT&CK – D3FEND Matrix (Threat Model v1)

**Source:** `04_Praxis_Artifact/Architecture/Threat_Model_v1.md`, `Adversary_Profiles.md`.  
**Use:** Defensive mapping only; supports SEAS 8400, 8405. Citations: MITRE ATT&CK, MITRE D3FEND (d3fend.mitre.org).

---

| Threat (ATT&CK) | Brief description | D3FEND defensive technique (example) | Artifact relevance |
|-----------------|-------------------|--------------------------------------|--------------------|
| T1565 Data Manipulation | Adversary manipulates data to evade or poison | D3-IA Ingest Analysis; D3-AVB Anomaly-based detection; input validation | Ingest validation; baseline/drift checks |
| T1070 Indicator Removal / log evasion | Clearing or altering logs | D3-SDL Secure data logging (at source); D3-IA validate continuity | Pipeline input validation; document source assumptions |
| T1027 Obfuscated Files or Information | Obfuscation to evade detection | D3-DR Detection rules; D3-MA Model-based detection | Detection engine (rules/ML); RQ1 detection rate |
| Data confidentiality (pipeline) | Unauthorized access to data | D3-AC Access control; D3-EA Encrypt data at rest/transit | Agent 05/06: Zero Trust, encryption |

---

**Limitations:** High-level mapping; implement controls per architecture and PI approval. No offensive use of techniques.

**Last Updated:** 2025-02-06
