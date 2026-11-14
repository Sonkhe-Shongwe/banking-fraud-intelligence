# Banking Fraud Intelligence

A portfolio case study on prioritising potentially fraudulent card transactions under a fixed daily review limit. It compares how many fraud-labelled transactions a risk model and an amount-based baseline select at the same review capacity.

**Current checkpoint (14 November 2026).** Overall progress is 72%. The comparison measures reconciled in Power BI Desktop. The dark Fraud Triage page builder passed fixture and schema checks and is ready to apply to the local project. [Phase scorecard](docs/PROJECT_STATUS_CURRENT.md) · [Resume here](docs/SESSION_HANDOFF_CURRENT.md#resume-here)

Use the existing validated `data/processed/transactions.csv` if you already have it. For a fresh checkout, follow the Windows setup in the [local data guide](data/README.md#prepare-one-csv).

## Start here

| What you need | Where to look |
|---|---|
| Resume the project in a new conversation | [Master continuation prompt](docs/MASTER_CONTINUATION_PROMPT.md) |
| Status, plans and evidence in one place | [Documentation index](docs/DOCUMENTATION_INDEX.md) |
| What each phase delivers and how progress is earned | [Current phase scorecard](docs/PROJECT_STATUS_CURRENT.md) |
| Latest checkpoint, decisions and next action | [Current session handoff](docs/SESSION_HANDOFF_CURRENT.md) |
| Current Power BI visual direction and design rules | [Power BI design system](docs/POWER_BI_DESIGN_SYSTEM.md) |
| Latest design preview and Desktop acceptance criteria | [Fraud Triage design proposal](docs/FRAUD_TRIAGE_DESIGN_PROPOSAL.md) |
| Latest documentation audit and findings | [Documentation audit, 14 November 2026](docs/PROJECT_AUDIT_2026-11-14.md) |
| Dataset revision, audit results and limitations | [Data source and feasibility audit](docs/data_sources.md) |
| Local data and notebook workflow | [Local data guide](data/README.md) |
| P5 page scope and verified inputs | [Current session handoff](docs/SESSION_HANDOFF_CURRENT.md#p5-scope-and-design-gate) |
| Exploratory analysis | [Exploratory notebook](notebooks/01_fraud_investigation_eda.ipynb) |
| Feature engineering | [Feature engineering notebook](notebooks/02_fraud_feature_engineering.ipynb) |
| Model validation | [Modelling notebook](notebooks/03_fraud_model_validation.ipynb) |
| Held-out evaluation | [Held-out evaluation notebook](notebooks/04_fraud_holdout_evaluation.ipynb) |
| Power BI data preparation and QA | [P5 reporting notebook](notebooks/05_power_bi_data_preparation.ipynb) |
| Power BI theme | [Premium Banking Intelligence theme](powerbi/themes/Premium_Banking_Intelligence.json) |
| Power BI setup and data model | [Power BI guide](powerbi/README.md) |
| Model evaluation and investigation policy | [Methodology](docs/methodology.md) |
| Actual evaluation results | [Findings](docs/findings.md) |

## Intended deliverable

A reproducible Python pipeline using pandas for ingestion, validation and feature preparation and scikit-learn for offline modelling. The evaluation compares a model with an amount-based baseline on chronological held-out data. Report fraud caught, legitimate transactions sent for review, and fraud-labelled transaction value captured under the same daily review limits.

Power BI Desktop is the approved P5 platform. The two approved pages are **Fraud Overview** and **Review Policy Comparison**. The comparison page has a local report build, reconciled measures and a repeatable page builder. Fraud Overview still needs its report visuals and Desktop verification. [Design system](docs/POWER_BI_DESIGN_SYSTEM.md) · [Power BI guide](powerbi/README.md)

The data source is the Fraud Detection Handbook's simulated transactions. The September evaluation and its limitations are documented in [Findings](docs/findings.md). Fraud-labelled transaction value is reported as exposure under review, not as loss prevented. Dataset-derived artefacts remain local until publication permissions are resolved.

## Repository guide

- data/ holds acquisition guidance. Raw and processed datasets are excluded from Git.
- notebooks/ is for exploration, charts and model interpretation in Jupyter. src/ is for repeatable Python preparation, training, evaluation and exports. tests/ is for verification.
- powerbi/ contains the approved theme, comparison measure script, DAX checks, page builder and Desktop guide.
- docs/ holds project status, handoff, design system, audit, source audit, methodology and findings.
- reports/ and assets/ are reserved for approved shareable evidence and figures.
