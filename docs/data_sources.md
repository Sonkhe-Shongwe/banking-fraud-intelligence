# Data source feasibility register — 26 October 2026

**Status:** source-level candidate identification only. No files have been downloaded, profiled, trained on or formally approved.

| Candidate | Intended use | Known caveat | Gate |
|---|---|---|---|
| [Fraud Detection Handbook](https://github.com/Fraud-Detection-Handbook/fraud-detection-handbook) | Leading candidate: timestamped simulated transaction and fraud labels | **Synthetic**; scenario-generating fields can leak labels; model performance may not generalise | Check exact release, feature timing, sizes, licence and known fraud scenarios |
| [IEEE-CIS Fraud Detection](https://www.kaggle.com/competitions/ieee-fraud-detection) | Alternative for anonymised e-commerce patterns | Anonymised fields and access/competition terms complicate explanation and temporal design | Verify download access, terms, labels, dates and permitted repository material |
| [PaySim](https://www.kaggle.com/datasets/ealaxi/paysim1) | Alternative simulated mobile-money activity | Simulated; some labels/features may make classification artificially easy | Inspect schema, baseline difficulty, synthetic-generation assumptions and terms |

## Minimum dataset requirements
Transaction identifier, appropriate order/time field, binary historical fraud label, transaction amount, usable prediction-time features and enough examples for a chronological holdout and review-capacity simulation.

## Failure conditions
Do not proceed with a dataset if a credible temporal evaluation cannot be constructed, legitimate prediction-time features cannot be distinguished from leaked fields, or required access/usage permissions are unavailable.

## Reproducibility
Record authoritative URL, version, file hashes, extraction procedure, licence, row counts, exclusions and data dictionary when actual data is acquired. Do not commit restricted or unwieldy raw datasets.

**Simulation caveat:** detected fraudulent value is not equivalent to realised or prevented loss.
