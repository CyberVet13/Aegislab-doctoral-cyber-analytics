---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 05)
Prompt_Summary: Defense-in-depth layers for AegisLab Security Detection Pipeline.
PI_Review_Status: Draft
---

# Defense-in-Depth Map — AegisLab Security Detection Pipeline

**Source:** System_Architecture_v1, Threat_Model_v1, Zero_Trust_Design.  
**Alignment:** SEAS 8405.

---

## Layers (artifact scope)

| Layer | Control / measure | Rationale |
|-------|-------------------|-----------|
| **Perimeter / input** | Schema validation, source allowlist or authentication for ingest | Reduce T1565, T1070 (manipulation, log evasion) at entry |
| **Processing** | Least privilege for detection engine; no unnecessary network egress | Limit blast radius; assume breach |
| **Data** | Access control and encryption for output store (Agent 06) | Confidentiality and integrity of results |
| **Monitoring** | Logging of pipeline health and evaluation metrics (no sensitive data in logs) | Observability; align with Metrics_Definitions |

---

## Control placement (high level)

- **Ingest:** Validate input format and optional integrity; reject malformed or unauthorized source.
- **Detection engine:** Read-only to inputs; write only to designated output; versioned code and config.
- **Output/store:** Encrypt at rest; access only by evaluation harness and authorized users.
- **Evaluation harness:** Read from output/store; write results to `06_Analysis/`; documented in Analysis_Plan.

---

## Limitations

- Single-pipeline scope; enterprise DiD (e.g., network segmentation, EDR) out of scope unless PI extends artifact.
- Document lab vs. operational deployment; tighten controls for operational use.

---

**Last Updated:** 2025-02-06
