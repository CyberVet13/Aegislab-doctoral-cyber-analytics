# Data - AegisLab Doctoral Research

## Purpose
Store raw, processed, and synthetic data with **documented provenance**. All analysis inputs must trace to this directory or an approved external source. No PII or sensitive data without access controls and governance approval.

## Structure
- **Raw/** – Unmodified source data; document origin, date, and access conditions.
- **Processed/** – Cleaned, transformed, or aggregated data; document pipeline and version.
- **Synthetic/** – AI-generated or synthetic datasets; clearly label and document methodology per `00_Governance/AI_Use_Disclosure.md`.

## Provenance Requirements
For each dataset, maintain:
- Source (e.g., public dataset, authorized internal, synthetic).
- Date obtained or generated.
- Processing steps (if processed).
- Classification (public, internal, sensitive) and handling requirements.
- Reference in analysis scripts and results (reproducibility).

**Last Updated:** [YYYY-MM-DD]
