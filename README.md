# Banking Fraud Intelligence

> **Status (26 October 2026): Planning and dataset feasibility review. No model, deployed app, dataset audit, or findings are claimed.**

## Core business problem
How should a financial institution prioritise potentially fraudulent transactions under limited investigation capacity while balancing detection, unnecessary investigations and financial exposure?

## Intended end-to-end deliverable
A **reproducible SQL/Python machine-learning investigation** plus a **lightweight Streamlit decision-support application**. The app is a presentation and simulation layer, not a replacement for an independently testable analytical pipeline.

The proposed app would have an overview, prioritised investigation queue, transaction-level review and an investigation-capacity simulator using held-out labelled data. Train models offline, not during web sessions. A separate custom website and flagship Power BI report are **not planned**; Power BI is optional only if it adds clear analytical value.

## Proposed technology
- **Core:** Python, pandas, NumPy, scikit-learn, SQL, notebooks, Git/GitHub.
- **Evaluation:** chronological splits, leakage audits, precision/recall, PR-AUC, calibration and capacity-constrained ranking.
- **Delivery:** Streamlit, charts, documented assumptions, reproducibility and tests.

## Dataset position
**Leading provisional candidate:** [Fraud Detection Handbook](https://github.com/Fraud-Detection-Handbook/fraud-detection-handbook), a synthetic transaction simulation. IEEE-CIS and PaySim remain alternatives. Dataset access, license, schema, size, leakage columns and compute feasibility require a raw-data audit before selection.

Simulated outcomes must **not** be described as achieved savings or bank production performance. Fraud exposure and prevented losses are not equivalent.

## Delivery stages (planned for 2027)
1. Verify data, documentation, reuse terms, transaction timing and prediction-time feature availability.
2. Define decision policy and business success metrics; create baselines.
3. Implement and test SQL/Python preparation and temporal model evaluation.
4. Assess investigator-capacity scenarios on held-out data.
5. Build the lightweight Streamlit interface and document results, limitations and reproducibility.

## Repository guide
- `data/`: acquisition instructions and excluded raw datasets.
- `sql/`: transformations and analytical checks.
- `src/`, `notebooks/`, `tests/`: analytical pipeline and verification.
- `docs/`: sources, method, analytical design and findings.
- `reports/`, `assets/`: supporting report and figures.
- `powerbi/`: existing scaffold only; Power BI is **not a required deliverable**.

**Portfolio context:** [PilotODIN](https://github.com/Sonkhe-Shongwe/PilotODIN) · [Education research](https://github.com/Sonkhe-Shongwe/does-a-degree-still-matter) · [Financial consumer complaints BI](https://github.com/Sonkhe-Shongwe/financial-consumer-complaint-analysis)

**Planning documentation only. No analytical work has started.**
