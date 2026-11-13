# Banking Fraud Intelligence

A portfolio case study on prioritising potentially fraudulent card transactions when investigators can review only a fixed number each day. The main question is whether a risk model helps investigators find more fraud than an amount-based baseline at the same review capacity.

**Current checkpoint (13 November 2026): P1 at 80% · P2 and P3 at 100% · 52% overall.** The modelling notebook compares the August review queues, and the September evaluation protocol is frozen. The publication scope for dataset-derived artefacts is open. [Phase scorecard](docs/PROJECT_STATUS_CURRENT.md) · [Resume here](docs/SESSION_HANDOFF_CURRENT.md)

**Open the data locally:** Pull this repository and double-click **Prepare Transactions.cmd** on Windows. It downloads the pinned source if needed and produces one CSV. [Instructions](data/README.md)

## Start here

| What you need | Where to look |
|---|---|
| Resume the project in a new conversation | [Master continuation prompt](docs/MASTER_CONTINUATION_PROMPT.md) |
| Status, plans and evidence in one place | [Documentation index](docs/DOCUMENTATION_INDEX.md) |
| What each phase delivers and how progress is earned | [Current phase scorecard](docs/PROJECT_STATUS_CURRENT.md) |
| Latest checkpoint, decisions and next action | [Current session handoff](docs/SESSION_HANDOFF_CURRENT.md) |
| Dataset revision, audit results and limitations | [Data source and feasibility audit](docs/data_sources.md) |
| Run the first fraud investigation | [Exploratory notebook](notebooks/01_fraud_investigation_eda.ipynb) · [Local setup](data/README.md#run-the-exploratory-notebook) |
| Check the CSV before feature preparation | [Pipeline validation](data/README.md#validate-the-csv-for-the-pipeline) |
| Build and inspect the model inputs | [Feature engineering notebook](notebooks/02_fraud_feature_engineering.ipynb) · [Local setup](data/README.md#run-the-feature-engineering-notebook) |
| Fit the first model and compare August review queues | [Modelling notebook](notebooks/03_fraud_model_validation.ipynb) · [Local setup](data/README.md#run-the-modelling-notebook) |
| Model evaluation and investigation policy | [Methodology](docs/methodology.md) |

## Intended deliverable

A reproducible Python pipeline using pandas for ingestion, validation and feature preparation and scikit-learn for offline modelling. The evaluation compares a model with an amount-based baseline on chronological held-out data. Report fraud caught, legitimate transactions sent for review, and fraud-labelled transaction value captured under the same daily review limits.

The approved P5 platform is Power BI Desktop. The validated data and held-out results will determine which questions the report can answer and which views the owner reviews for approval. Candidate interactions include changing daily review capacity, comparing policies, inspecting the queue and drilling through to a transaction. Each needs a verified Python output and a data source suitable for the intended audience. [Evidence for the dashboard](docs/methodology.md#evidence-for-the-dashboard)

The leading data source is the Fraud Detection Handbook's simulated transactions. The audit supports a simulated study. Final September results are pending. Fraud-labelled transaction value is reported as exposure under review.

## Repository guide

- `data/` holds acquisition guidance. Raw and processed datasets are excluded from Git.
- `notebooks/` is for exploration, charts and model interpretation in Jupyter. `src/` is for repeatable Python preparation, training, evaluation and exports. `tests/` is for verification.
- `powerbi/` is reserved for the P5 report and its setup instructions.
- `docs/` holds the project status, handoff, source audit, methodology and findings.
- `reports/` and `assets/` are reserved for shareable evidence and figures.
