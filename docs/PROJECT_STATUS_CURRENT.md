# Current project status

**Checkpoint:** 14 November 2026

**Overall progress:** 72% · **Latest completed phase:** P4 at 100% · **P1:** 80%

**Next checkpoint.** Apply and verify Fraud Triage in Power BI Desktop. P5 remains at 0% pending accepted report evidence. [Run evidence and next steps](SESSION_HANDOFF_CURRENT.md#resume-here)

| Phase | Weight | Complete | Points earned | Evidence required to close |
|---|---:|---:|---:|---|
| **P1 · Scope and dataset feasibility** | 15% | **80%** | **12** | Pin and profile the source, document leakage and label timing, record scope and audit in Git, and agree on publication scope. |
| **P2 · Python data pipeline** | 20% | **100%** | **20** | Repeatable load and validation, scoring-time feature preparation, chronological train/validation/test partitions, and checks for future information. |
| **P3 · Baseline and model** | 20% | **100%** | **20** | Amount-based baseline and at least one scikit-learn model, compared on validation data. Record and freeze the model and evaluation protocol before scoring the holdout. |
| **P4 · Investigation policy and held-out results** | 20% | **100%** | **20** | Compare model and baseline at the same daily review limits. Report fraud caught, legitimate reviews and fraud-labelled transaction value. Check results on amounts at or below 220. |
| **P5 · Power BI Investigation Dashboard** | 15% | 0% | 0 | Notebook 05 outputs, Windows Overview reconciliation and Desktop theme import passed. Verify the semantic model and theme rendering, build the two approved pages, reconcile all measures to Python, and verify filters, navigation, accessibility and report behaviour. [Design system](POWER_BI_DESIGN_SYSTEM.md) |
| **P6 · Portfolio release** | 10% | 0% | 0 | Verify from a fresh checkout and publish the approved README, reproduction instructions, results, limitations and walkthrough after publication scope is cleared. |
| **Overall** | **100%** | **72%** | **72** | |

Phase percentages track accepted evidence. Overall progress is the sum of each phase weight multiplied by its completion fraction. The current score is 15 × 0.80 + 3 × 20 = 72 points.

## P1 checks

Each check is worth 20% of P1.

| Check | Status | Evidence |
|---|---|---|
| Pin the source revision | Verified | [Raw dataset revision and manifest](data_sources.md#source-and-audit-evidence) |
| Profile all raw files | Verified | [183 batches and 1,754,155 transactions](data_sources.md#source-and-audit-evidence) |
| Identify leakage and label-timing risks | Verified | [Simulator limits and evaluation implications](data_sources.md#evaluation-implications) |
| Record revised scope and audit in GitHub | Verified | [Python scope](../README.md#intended-deliverable) · [Audit](data_sources.md) |
| Resolve which derived artefacts can be published | Open | [Publication scope](data_sources.md#publication-scope) |

## P2 checks

Each check is worth 25% of P2.

| Check | Status | Evidence |
|---|---|---|
| Repeatable input load and validation | Verified | [Full CSV run and validation rules](../data/README.md#validate-the-csv-for-the-pipeline) · [Regression tests](../tests/test_validate_transactions.py) |
| Scoring-time feature preparation | Verified | [Feature definitions](data_model.md#scoring-time-features-and-partitions) and [full CSV notebook run](../notebooks/02_fraud_feature_engineering.ipynb) |
| Chronological partitions | Verified | The notebook reconciles all transaction IDs to the ordered train, validation and test partitions. Boundary behaviour is covered by [regression tests](../tests/test_transaction_features.py) |
| Checks for future information | Verified | Equal-time and future-event tests passed. Training features matched exactly when rebuilt without August and September rows. [Regression tests](../tests/test_transaction_features.py) |

## P3 evidence

The [modelling notebook](../notebooks/03_fraud_model_validation.ipynb) ran on the pinned CSV. It fitted the baseline challenger on April–July, compared both August policies at equal daily capacities and verified both eligible cohorts. The [frozen protocol](methodology.md#frozen-model-and-review-protocol) defines the inputs and comparison for P4.

## P4 evidence

The [held-out notebook](../notebooks/04_fraud_holdout_evaluation.ipynb) reproduced the April–July fit and evaluated both policies across all 30 September days. It reconciled review counts, fraud caught, legitimate reviews and fraud-labelled value to the rows selected by rank for all eight policy, cohort and capacity combinations. All ten regression tests passed. The owner confirmed the [local reporting export](data_model.md#september-review-rank-export) was generated in Windows VS Code.

## P5 decision and implementation status

- **Approved:** Power BI Desktop; two pages (Fraud Overview and Review Policy Comparison); Premium Banking Intelligence light-theme direction; start with Review Policy Comparison.
- **Approved by owner (13 November 2026):** exact palette, typography, canvas/grid, both page wireframes, visual selection, KPI card treatment, icons and interactions, as recorded in P5 wireframe proposal v0.1.
- **Verified:** Notebook 05 generated the expected local files. The Linux reproduction matched all eight September comparisons, and the corrected Overview audit matched seven daily metrics across 183 dates. The theme passed Microsoft's schema check.
- **Verified in Windows:** All seven Overview metrics matched across 183 dates. Power BI Desktop confirmed the theme import.
- **Observed in Desktop:** Four reporting tables, two active single-direction relationships from `DimDate` and a disconnected scenario table.
- **Owner reported:** Date table marked and report saved locally.
- **Passed in Desktop:** Review Policy Comparison model application, four imported table row counts, all six metrics in each of the eight full-September comparisons and one restricted single-day check.
- **Awaiting local verification:** Calendar sorting, Desktop version, theme rendering, Fraud Overview measure reconciliation and report interactions.
- **Observed in Desktop:** The first light page build displayed 589, 592 and +3, both policy lines and the four fixed reference values. The layout polish and report interactions still need a Desktop check.
- **Prepared:** The owner-authorised Fraud Triage builder passed PBIR schema and fixture checks. [Desktop acceptance checks](../powerbi/README.md#10-apply-and-verify-fraud-triage)
- **Separate open gate:** dataset-derived publication permissions. See [source publication scope](data_sources.md#publication-scope).

P5 remains at 0% pending verified report implementation and acceptance.

For a new conversation, use the [master continuation prompt](MASTER_CONTINUATION_PROMPT.md) to retrieve this scorecard and the current handoff.
