# Current session handoff

**Updated:** 13 November 2026

**Project:** Banking Fraud Intelligence

**Start with:** [Phase scorecard](PROJECT_STATUS_CURRENT.md) · [Documentation index](DOCUMENTATION_INDEX.md) · [Power BI design system](POWER_BI_DESIGN_SYSTEM.md) · [Master continuation prompt](MASTER_CONTINUATION_PROMPT.md)

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
| Delivery state | P1 is at 80%, P2 through P4 are at 100%, and overall progress is 72%. P5 is approved in scope and design direction but has not started implementation. |

## Owner working agreement

Work in small increments with a visible checkpoint. Show what changed, what was verified, and what the owner can open after pulling. Keep executed notebooks in the [local notebook runs folder](../data/README.md#save-notebook-runs-locally) so the tracked sources can receive updates. The owner requires explicit approval before major design changes or unapproved implementation. Dashboard scope and publication scope are separate decisions.

## Owner-approved P5 decisions

1. Power BI Desktop is the report platform.
2. The first report has two pages: **Fraud Overview** and **Review Policy Comparison**.
3. Start the build with **Review Policy Comparison**.
4. The approved design direction is **A — Premium Banking Intelligence**: light, restrained, sophisticated, professional and executive-grade.
5. No drastic design or implementation change without the owner's approval.

## P5 scope and design gate

The page scope and overall visual direction are approved. Detailed design is not yet approved. The following remain proposals for review: palette, typography, canvas size, spacing/grid, exact page wireframes, chart types, KPI card treatment, iconography and interactions.

| Page | Intended purpose | Verified input | Design status |
|---|---|---|---|
| Fraud Overview | Show simulated transaction activity, fraud-labelled count/share and trends over the available period | Validated full transaction CSV | Page approved; exact layout pending |
| Review Policy Comparison | Compare amount ranking and logistic regression at 50 or 100 reviews/day, across all transactions or amounts at or below 220 | Local September rank CSV | Page approved; first build; exact layout pending |

The proposed metric contract, visual tokens and design gates are in the [Power BI design system](POWER_BI_DESIGN_SYSTEM.md).

**Important data-language restrictions:**
- Describe the data as simulated and the outcome as a retrospective fraud label.
- Use fraud-labelled transaction value, not fraud loss prevented or money saved.
- Do not display alerts reviewed, case resolution, turnaround time, geography, channel, product or customer-segment analysis; the source does not support those claims.
- The logistic-regression decision score is not a calibrated probability.
- For the at-or-below-220 cohort, use its independently recalculated rank columns, not the full-population ranks.
- The visual concept board is a moodboard only. Its sample KPI values and fraud-pattern categories are placeholders and must not be copied into the report.

### Current Power BI repository state

At audited remote HEAD 6326968, the powerbi directory contains only .gitkeep. No PBIX, final theme JSON, DAX measure set or Power BI Desktop validation evidence exists. This is consistent with P5 at 0%.

### Publication boundary

Keep raw files, processed extracts, transaction-level rank exports and reports containing row-level records local. The source snapshot does not include a separate raw-data licence, and permission to redistribute derived artefacts has not been established. Resolve publication scope separately before portfolio release. [Source publication scope](data_sources.md#publication-scope)

## Resume here

1. Review [P5 Wireframe Proposal v0.1](P5_WIREFRAMES_PROPOSAL_v0.1.md), including the two page layouts, metric hierarchy, controls, visual language and proposed data model.
2. Owner to approve or revise the palette, typography, canvas, page layouts, chart choices and interaction contract. The proposal is non-binding; no theme or report has been implemented.
3. After detailed design approval, create the approved theme and data-preparation outputs, then build Review Policy Comparison first and Fraud Overview second.
4. Reconcile all eight September policy/cohort/capacity comparisons and representative date selections against Python. Test Power BI Desktop refresh, filters, navigation, accessibility and rendering.
5. Keep P5 at 0% until the approved report has been built and verified in Power BI Desktop. Resolve publication permissions separately.

## Checkpoint history

| Date | Checkpoint |
|---|---|
| 26 October 2026 | Proposed data grain and model quality gates recorded in d7d2726. |
| 13 November 2026 | Profiled the pinned simulated source, recorded the Python-only scope, and added the documentation index, phase scorecard and session handoff. |
| 13 November 2026 | Owner approved Power BI Desktop for P5. |
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
| 13 November 2026 | Recorded Windows confirmation for P4 and documented the local notebook-run workflow. |
| 13 November 2026 | Owner approved the two P5 report pages and the Premium Banking Intelligence light-theme direction. Detailed design tokens and wireframes remain subject to owner approval. |
| 13 November 2026 | Researched corporate banking, Dribbble, LinkedIn and TikTok analytics interfaces; documented P5 wireframe proposal v0.1. No Power BI files or implementation artefacts were changed. |
| 13 November 2026 | Audited remote main, corrected stale dark-theme handoff language, established the design system and recorded the P5 readiness audit. |
