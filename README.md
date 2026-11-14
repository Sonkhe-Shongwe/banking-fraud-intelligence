# Banking Fraud Intelligence

A portfolio case study on prioritising potentially fraudulent card transactions when investigators can review only a fixed number each day. The main question is whether a risk model helps investigators find more fraud than an amount-based baseline at the same review capacity.

**Current checkpoint (14 November 2026): P1 at 80% · P2 through P4 at 100% · 72% overall.** The Overview reconciliation passed on Windows, and Power BI Desktop imported the approved light theme. All four reporting tables are visible in Desktop Model view. The Review Policy Comparison model passed Desktop reconciliation. Its three KPI cards show the expected default values. The next step is to format and align the cards. [Phase scorecard](docs/PROJECT_STATUS_CURRENT.md) · [Resume here](docs/SESSION_HANDOFF_CURRENT.md#resume-here)

Use the existing validated data/processed/transactions.csv if you already have it. For a fresh checkout, follow the Windows setup in the [local data guide](data/README.md#prepare-one-csv).

## Start here

| What you need | Where to look |
|---|---|
| Resume the project in a new conversation | [Master continuation prompt](docs/MASTER_CONTINUATION_PROMPT.md) |
| Status, plans and evidence in one place | [Documentation index](docs/DOCUMENTATION_INDEX.md) |
| What each phase delivers and how progress is earned | [Current phase scorecard](docs/PROJECT_STATUS_CURRENT.md) |
| Latest checkpoint, decisions and next action | [Current session handoff](docs/SESSION_HANDOFF_CURRENT.md) |
| Current Power BI visual direction and design rules | [Power BI design system](docs/POWER_BI_DESIGN_SYSTEM.md) |
| Proposed P5 page layouts and detailed design review | [P5 wireframe proposal v0.1](docs/P5_WIREFRAMES_PROPOSAL_v0.1.md) |
| Repository, continuity and P5 readiness review | [Project audit, 13 November 2026](docs/PROJECT_AUDIT_2026-11-13.md) |
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

Power BI Desktop is the approved P5 platform. The two approved pages are **Fraud Overview** and **Review Policy Comparison**, with the latter planned as the first build. The approved visual direction is a light, premium banking-intelligence aesthetic. The detailed palette, typography, page layouts, chart selection and interactions are approved. The theme JSON and reporting-data notebook are prepared; the PBIX and DAX measure layer are not yet built. [Design system](docs/POWER_BI_DESIGN_SYSTEM.md)

The data source is the Fraud Detection Handbook's simulated transactions. The September evaluation and its limitations are documented in [Findings](docs/findings.md). Fraud-labelled transaction value is reported as exposure under review, not as loss prevented. Dataset-derived artefacts remain local until publication permissions are resolved.

## Repository guide

- data/ holds acquisition guidance. Raw and processed datasets are excluded from Git.
- notebooks/ is for exploration, charts and model interpretation in Jupyter. src/ is for repeatable Python preparation, training, evaluation and exports. tests/ is for verification.
- powerbi/ contains the approved theme and setup guide. The local report model is set up and the comparison measures reconcile. Visuals are the next P5 increment.
- docs/ holds project status, handoff, design system, audit, source audit, methodology and findings.
- reports/ and assets/ are reserved for approved shareable evidence and figures.
