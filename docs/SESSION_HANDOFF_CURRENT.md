# Current session handoff

**Updated:** 13 November 2026

**Project:** Banking Fraud Intelligence

**Start with:** [Phase scorecard](PROJECT_STATUS_CURRENT.md) · [Documentation index](DOCUMENTATION_INDEX.md) · [Master continuation prompt](MASTER_CONTINUATION_PROMPT.md)

## Verified checkpoint

| Area | Evidence |
|---|---|
| Scope | Python for data preparation, modelling and evaluation. The owner approved Power BI Desktop as the single P5 dashboard platform. |
| Data | The pinned Handbook raw snapshot was profiled across 183 daily files. It contains 1,754,155 simulated transactions and 14,681 fraud labels. [Audit](data_sources.md) |
| Local CSV | The pinned archive was converted in Linux and the extracted CSV passed validation in Windows with Anaconda Python 3.12.7. Use the existing validated CSV or follow the fresh setup instructions. The Windows launcher still awaits a Windows run. [Instructions](../data/README.md#prepare-one-csv) |
| Exploratory notebook | Executed on the verified CSV in IPython. The owner also confirmed a successful Windows VS Code run using Python 3.12.7 and the extracted CSV. The notebook audits the input, compares illustrative review budgets and checks sensitivity to the amount rule. [Notebook](../notebooks/01_fraud_investigation_eda.ipynb) · [Run instructions](../data/README.md#run-the-exploratory-notebook) |
| P2 input validation | Ran the validator on the full CSV with pandas 2.2.3. It accepted all 1,754,155 rows, kept 42 zero-amount rows and left the CSV byte-identical. The regression suite checks malformed inputs and retention of valid same-time transactions. [Validation instructions](../data/README.md#validate-the-csv-for-the-pipeline) |
| P2 feature engineering | Executed the [feature notebook](../notebooks/02_fraud_feature_engineering.ipynb) on the full CSV in IPython. Verified one feature row per transaction and full coverage of the chronological split. Training-period features matched exactly when rebuilt from April–July alone. Eight regression tests passed. [Run instructions](../data/README.md#run-the-feature-engineering-notebook) |
| P3 baseline and model | Executed the [modelling notebook](../notebooks/03_fraud_model_validation.ipynb) in IPython. Fitted logistic regression with April–July only. Compared both August policies at both budgets in the full and restricted cohorts. Ten regression tests passed. [Frozen protocol](methodology.md#frozen-model-and-review-protocol) |
| P4 held-out evaluation | The [held-out notebook](../notebooks/04_fraud_holdout_evaluation.ipynb) reconciled all eight September comparisons. Ten regression tests passed. The owner confirmed the notebook saved 287,873 rows in Windows. The [export path fix](https://github.com/Sonkhe-Shongwe/banking-fraud-intelligence/commit/1a56a16a383f6d0b4181082b778ca1d12287c5a3) reproduced the same CSV byte for byte. |
| Key risk | The simulator labels all amounts above 220 as fraud. The raw files lack label-confirmation timestamps. [Evaluation implications](data_sources.md#evaluation-implications) |
| Delivery state | P1 is at 80%, P2 through P4 are at 100%, and overall progress is 72%. The P5 report scope awaits owner approval. |

## Owner working agreement

Work in small increments with a visible checkpoint. Show what changed, what was verified, and what the owner can open after pulling. Keep executed notebooks in the [local notebook runs folder](../data/README.md#save-notebook-runs-locally) so the tracked sources can receive updates. Dashboard scope, publication scope and other major changes require owner approval.

## Resume here

1. Use the existing `data/processed/september_review_ranks.csv` for the September comparison. To regenerate it, [run the held-out notebook](../data/README.md#run-the-held-out-evaluation) in the working Python 3.12 kernel.
2. Review the [proposed P5 scope](#p5-scope-for-review). After scope approval, build the local Power BI report and reconcile its measures and filters against Python.
3. Confirm which artefacts can be shared before publishing portfolio outputs. Keep raw data, transaction-level ranks, and reports that embed those rows local while publication terms are unresolved. [Publication scope](data_sources.md#publication-scope)

## P5 scope for review

The proposed first version has two dark-theme report pages. Power BI Desktop is approved. The page scope is a proposal, and the dark concept is a preview.

| Page | Proposed content | Verified input |
|---|---|---|
| Fraud overview | Simulated transaction volume, fraud count and rate, date trend, and fraud-labelled value. Label the selected period and amount units. | Validated source CSV |
| Review policy comparison | September holdout, 50 or 100 reviews per day, full or at-or-below-220 cohort, and side-by-side fraud caught, legitimate reviews, precision, recall and fraud-labelled value selected. | Local September rank CSV |

Transaction-level queue and drillthrough are optional follow-up views. An August comparison would require a matching August reporting export and separate validation labeling. For the September page, reconcile all eight policy, cohort and capacity combinations and a representative date selection against Python. [Rank contract](data_model.md#september-review-rank-export) · [Evidence for the dashboard](methodology.md#evidence-for-the-dashboard)

## Checkpoint history

| Date | Checkpoint |
|---|---|
| 26 October 2026 | Proposed data grain and model quality gates recorded in `d7d2726`. |
| 13 November 2026 | Profiled the pinned simulated source, recorded the Python-only scope, and added the documentation index, phase scorecard and session handoff. |
| 13 November 2026 | Owner approved Power BI Desktop for P5. Recorded the change and the Python-to-report handoff. |
| 13 November 2026 | Owner directed that data availability and analysis determine the project outline and proposed Power BI views. |
| 13 November 2026 | Converted and checked the uploaded archive. Added a pull-and-run launcher for local CSV generation. |
| 13 November 2026 | Added a reusable continuation prompt linked from the README, project instructions, documentation index and current status records. |
| 13 November 2026 | Ran the first exploratory notebook on the verified CSV and recorded the exact local reproduction steps. |
| 13 November 2026 | Owner confirmed the notebook ran in Windows. Verified the first P2 checkpoint by running the input validator on the full CSV and testing invalid inputs. |
| 13 November 2026 | Addressed pandas type diagnostics reported in VS Code. Rechecked the validator and notebook cells with Pyright and reran both on the full CSV. |
| 13 November 2026 | Owner confirmed the validator passed on Windows in Anaconda Python 3.12.7. Matched the CSV dtype mapping annotation to the pandas type signature flagged by Pylance. |
| 13 November 2026 | Completed P2 with a notebook walkthrough, reusable feature code, verified chronological partitions and timestamp leakage checks on the pinned data. |
| 13 November 2026 | Completed P3 with the amount baseline, logistic regression challenger, August validation notebook and frozen September evaluation protocol. |
| 13 November 2026 | Completed P4 with the frozen September evaluation, eight reconciled queue comparisons and a local rank export for the proposed Power BI report. |
| 13 November 2026 | Recorded Windows confirmation for P4, documented the local notebook-run workflow, and captured the proposed P5 scope for review. |
