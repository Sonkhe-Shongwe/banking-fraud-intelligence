# Banking Fraud Intelligence

A portfolio case study on prioritising potentially fraudulent card transactions when investigators can review only a fixed number each day. The main question is whether a risk model helps investigators find more fraud than an amount-based baseline at the same review capacity.

**Current checkpoint (13 November 2026): P1 at 80% · 12% overall.** The source is pinned, the raw data was profiled, and the Python-only scope is recorded. The publication scope for dataset-derived artefacts is open. [Phase scorecard](docs/PROJECT_STATUS_CURRENT.md) · [Resume here](docs/SESSION_HANDOFF_CURRENT.md)

## Start here

| What you need | Where to look |
|---|---|
| Status, plans and evidence in one place | [Documentation index](docs/DOCUMENTATION_INDEX.md) |
| What each phase delivers and how progress is earned | [Current phase scorecard](docs/PROJECT_STATUS_CURRENT.md) |
| Latest checkpoint, decisions and next action | [Current session handoff](docs/SESSION_HANDOFF_CURRENT.md) |
| Dataset revision, audit results and limitations | [Data source and feasibility audit](docs/data_sources.md) |
| Model evaluation and investigation policy | [Methodology](docs/methodology.md) |

## Intended deliverable

A reproducible Python pipeline using pandas for ingestion, validation and feature preparation and scikit-learn for offline modelling. The evaluation compares a model with an amount-based baseline on chronological held-out data. Report fraud caught, legitimate transactions sent for review, and fraud-labelled transaction value captured under the same daily review limits.

The planned Streamlit demo uses precomputed scores. A reviewer can change daily review capacity, see the queue and trade-offs update, and open a transaction for more detail. The owner approves the dashboard design before it is built.

The leading data source is the Fraud Detection Handbook's simulated transactions. The audit supports a simulated study. Model results, a working app and production performance evidence are future deliverables. Fraud-labelled transaction value is reported as exposure under review.

## Repository guide

- `data/` holds acquisition guidance. Raw and processed datasets are excluded from Git.
- `src/`, `notebooks/` and `tests/` are reserved for the Python pipeline and verification.
- `docs/` holds the project status, handoff, source audit, methodology and findings.
- `reports/` and `assets/` are reserved for shareable evidence and figures.
