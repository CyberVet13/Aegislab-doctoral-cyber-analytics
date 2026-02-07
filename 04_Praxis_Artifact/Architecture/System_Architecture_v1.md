---
Session_Date: 2025-02-06
Model_Used: Claude Sonnet 4.5 (Agent 03 Deep Dive)
Prompt_Summary: High-level system architecture for praxis artifact (detection pipeline / analytics); evaluation instrumentation.
PI_Review_Status: Draft
Modifications: [PI to set artifact name, tech stack, and environment]
---

# System Architecture v1 — Praxis Artifact

**Artifact name:** AegisLab Security Detection Pipeline (or substitute your title; e.g., "[Org] Detection Analytics Pipeline").  
**Scope:** Security analytics detection pipeline that ingests security-relevant logs/telemetry, applies detection logic, and produces outputs for detection-rate evaluation (pre/post). *Refine scope (e.g., network-only, endpoint-only) per PI.*

**Evaluation:** Primary metric = detection rate; see `04_Praxis_Artifact/Benchmarks/Performance_Criteria.md` and `02_Agents/07_Security_Data_Analytics/Outputs/Metrics_Definitions.md`.

---

## 1. Purpose and alignment to RQ1

- **Purpose:** Deliver an engineering artifact that (a) ingests security-relevant data, (b) applies detection/analytics logic, and (c) produces outputs that enable computation of detection rate (and optional secondary metrics) for pre/post comparison.
- **RQ1:** Does the praxis artifact improve detection rate compared to baseline? Architecture must support baseline (pre) and post measurement with same operational definition.

---

## 2. High-level architecture (C4 context level)

```
[Data sources: logs, telemetry] --> [Ingestion] --> [Processing / Detection] --> [Outputs / Alerts]
                                                                                    |
                                                                                    v
[Evaluation] <-- Detection rate (and optional metrics) computed from outputs + ground truth or labeled set
```

- **Data sources:** Security logs, telemetry, or labeled events (e.g., network flow, endpoint EDR, or SIEM exports); scope per PI.
- **Ingestion:** Log shipper or API (e.g., file tail, syslog, REST); schema normalization; no PII in evaluation pipeline without governance.
- **Processing / Detection:** Rule-based and/or lightweight ML detection (e.g., Python + pandas/scikit-learn or Sigma rules); versioned and documented for reproducibility.
- **Outputs:** Structured detections (event IDs, timestamps, confidence) to file store or DB for evaluation harness.
- **Evaluation:** Instrumentation point where detection rate is computed (pre and post windows); same definition and source in both periods.

---

## 3. Key components (placeholder)

| Component | Purpose | Technology (example) | Rationale |
|-----------|---------|----------------------|-----------|
| Ingest | Collect and normalize data | Python + file/syslog/API reader; schema (e.g., JSON/Parquet) | Single entry point; versioned schema; reproducible |
| Detection engine | Apply detection logic | Python (e.g., rules engine or scikit-learn); Sigma-compatible rules optional | Produces detections for evaluation; SEAS 8414 tool justification |
| Output / store | Persist results for analysis | SQLite or Parquet in `05_Data/Processed/` | Enables pre/post metric computation; no vendor lock-in |
| Evaluation harness | Compute detection rate | Scripts in `06_Analysis/Statistical/` (R or Python) | Same definition pre/post; Analysis_Plan |

*PI to confirm or replace technology choices; justify in Tool_Selection_Justification and methodology (SEAS 8405, 8414).*

---

## 4. Security and design patterns

- **Defense-in-depth:** Data ingestion and processing in bounded scope; least privilege for artifact components (per SEAS 8405). *Expand in Agent 05 handoff.*
- **Zero Trust:** No implicit trust of data sources; validate and log access (per SEAS 8405). *Expand when artifact is implemented.*
- **Monitoring:** Artifact health and evaluation metrics observable; no sensitive data in logs (per 00_Governance and Metrics_Definitions).

---

## 5. Evaluation metrics instrumentation

- **Detection rate:** Computed from (a) artifact outputs (detected events) and (b) ground truth or labeled set over the same window; proportion = true positives / (true positives + false negatives) or equivalent per Metrics_Definitions.
- **Pre period:** Baseline detection rate with same definition (e.g., same system without artifact or with baseline config).
- **Post period:** Detection rate with artifact deployed; same window length and population.
- **Data flow:** Outputs from artifact to `05_Data/Processed/` or equivalent; analysis scripts in `06_Analysis/Statistical/` (reproducibility per Analysis_Plan).

---

## 6. Handoffs to other agents

- **Agent 04 (Threat & Adversary):** Artifact boundary = data sources, ingest, detection, output; assumed adversary and detection requirements when threat model is built.
- **Agent 05 (Zero Trust / Architecture):** Control placement, Zero Trust and DiD details when stack is fixed.
- **Agent 06 (Cryptography):** If data at rest/transit or auth required; key management per compliance.
- **Agent 08 (Visualization):** Dashboard or figures for detection rate (pre/post) and decision pathway; see Visualization_Design and Decision_Pathway_Docs.

---

## 7. Implementation phases (placeholder)

- **Phase 1:** Requirements and design lock (this doc + Performance_Criteria).
- **Phase 2:** Ingest and detection component (minimal viable for baseline measurement).
- **Phase 3:** Baseline (pre) data collection; instrumentation stable.
- **Phase 4:** Full artifact deployment; post data collection; analysis per Analysis_Plan.

---

## 8. Committee defense preview

- **Why this architecture?** Supports RQ1 (detection rate pre/post) with clear instrumentation; reproducible and documentable.
- **Risks:** Scope creep; instrumentation drift between pre and post. Mitigations: fixed windows, same definitions, versioned code and config.

---

**Last Updated:** 2025-02-06  
**Next:** PI to set artifact name and tech stack; Agent 04 threat boundary; Agent 05 control mapping.
