# Current session handoff

**Updated:** 13 November 2026

**Project:** Banking Fraud Intelligence

**Start with:** [Phase scorecard](PROJECT_STATUS_CURRENT.md) · [Documentation index](DOCUMENTATION_INDEX.md) · [Master continuation prompt](MASTER_CONTINUATION_PROMPT.md)

## Verified checkpoint

| Area | Evidence |
|---|---|
| Repository baseline | The preceding planning checkpoint was [`d7d2726`](https://github.com/Sonkhe-Shongwe/banking-fraud-intelligence/commit/d7d27267768123a30c25472b5d8730a73ab1e5e8). |
| Scope | Python for data preparation, modelling and evaluation. The owner approved Power BI Desktop as the single P5 dashboard platform. |
| Data | The pinned Handbook raw snapshot was profiled across 183 daily files. It contains 1,754,155 simulated transactions and 14,681 fraud labels. [Audit](data_sources.md) |
| Local CSV | Converted the uploaded pinned ZIP and verified one CSV with 1,754,155 transactions, nine source columns and 14,681 fraud labels. Use **Prepare Transactions.cmd** after pulling. The Python converter was exercised in Linux. The Windows launcher awaits a Windows run. [Conversion commit `aeb7816`](https://github.com/Sonkhe-Shongwe/banking-fraud-intelligence/commit/aeb7816000692455468330c8628312665ea11910) · [Instructions](../data/README.md#prepare-one-csv) |
| Exploratory notebook | Executed on the verified CSV in IPython. The owner also confirmed a successful Windows VS Code run using Python 3.12.7 and the extracted CSV. The notebook audits the input, compares illustrative review budgets and checks sensitivity to the amount rule. [Notebook](../notebooks/01_fraud_investigation_eda.ipynb) · [Run instructions](../data/README.md#run-the-exploratory-notebook) |
| P2 input validation | Ran the validator on the full CSV with pandas 2.2.3. It accepted all 1,754,155 rows, kept 42 zero-amount rows and left the CSV byte-identical. The regression suite checks malformed inputs and retention of valid same-time transactions. [Validation instructions](../data/README.md#validate-the-csv-for-the-pipeline) |
| P2 feature engineering | Executed the [feature notebook](../notebooks/02_fraud_feature_engineering.ipynb) on the full CSV in IPython. Verified one feature row per transaction and full coverage of the chronological split. Training-period features matched exactly when rebuilt from April–July alone. Eight regression tests passed. [Run instructions](../data/README.md#run-the-feature-engineering-notebook) |
| P3 baseline and model | Executed the [modelling notebook](../notebooks/03_fraud_model_validation.ipynb) in IPython. Fitted logistic regression with April–July only. Compared both August policies at both budgets in the full and restricted cohorts. Ten regression tests passed. [Frozen protocol](methodology.md#frozen-model-and-review-protocol) |
| Key risk | The simulator labels all amounts above 220 as fraud. The raw files lack label-confirmation timestamps. [Evaluation implications](data_sources.md#evaluation-implications) |
| Delivery state | P1 is at 80%, P2 and P3 are at 100%, and overall progress is 52%. Final September evaluation and the Power BI report are pending. |

## Owner working agreement

Work in small increments with a visible checkpoint. Show what changed, why it matters, what was verified, and what the owner can open or try after pulling. Power BI Desktop is approved as the platform. Data availability, analytical findings and publication scope determine the proposed dashboard content. Dashboard design and other major changes require separate owner approval. The implementation start date has yet to be revised from the earlier 2027 plan.

## Resume here

1. Confirm the intended public artefacts and the applicable reuse terms. The source repository does not supply a separate raw-data licence. Keep raw files, row-level extracts and scored transaction records local while their publication rights are unresolved. [Publication scope](data_sources.md#publication-scope)
2. Open the [modelling notebook](../notebooks/03_fraud_model_validation.ipynb) in the Python 3.12 kernel to reproduce August validation. For P4, reproduce the fixed April–July fit and run the [frozen protocol](methodology.md#frozen-model-and-review-protocol) on September. Reconcile review counts and fraud-labelled value to the selected rows.
3. As P2–P4 produce evidence, record which business questions the data supports and what the analysis shows. Use those outputs to propose the P5 dashboard scope for owner approval. [Evidence for the dashboard](methodology.md#evidence-for-the-dashboard)
4. Update this handoff and the scorecard as each gate is closed.

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
