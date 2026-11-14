# Current session handoff

**Updated:** 14 November 2026

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
| Delivery state | P1 is at 80%, P2 through P4 are at 100%, and overall progress is 72%. P5 detailed design is approved and implementation is authorised within scope. Notebook 05 generated the local outputs. The Windows Overview audit and Desktop theme import passed. All four reporting tables and both date relationships are visible in Desktop Model view. |

## Owner working agreement

Work in small increments with a visible checkpoint. Show what changed, what was verified, and what the owner can open after pulling. Keep executed notebooks in the [local notebook runs folder](../data/README.md#save-notebook-runs-locally) so the tracked sources can receive updates. The owner requires explicit approval before major design changes or unapproved implementation. Dashboard scope and publication scope are separate decisions.

## Owner-approved P5 decisions

1. Power BI Desktop is the report platform.
2. The first report has two pages: **Fraud Overview** and **Review Policy Comparison**.
3. Start the build with **Review Policy Comparison**.
4. The approved design direction is **A — Premium Banking Intelligence**: light, restrained, sophisticated, professional and executive-grade.
5. No drastic design or implementation change without the owner's approval.

## P5 scope and design gate

The page scope, visual identity, detailed tokens, both wireframes and interaction contract are approved. The owner authorised implementation by saying “lets continue” on 13 November 2026. Proceed only within the approved design and two-page scope.

| Page | Intended purpose | Verified input | Design status |
|---|---|---|---|
| Fraud Overview | Show simulated transaction activity, fraud-labelled count/share and trends over the available period | Validated full transaction CSV | **Detailed design approved; implementation foundation prepared** |
| Review Policy Comparison | Compare amount ranking and logistic regression at 50 or 100 reviews/day, across all transactions or amounts at or below 220 | Local September rank CSV | **Detailed design approved; first build after local data/theme checks** |

The approved metric contract, visual tokens and design gates are in the [Power BI design system](POWER_BI_DESIGN_SYSTEM.md).

**Important data-language restrictions:**
- Describe the data as simulated and the outcome as a retrospective fraud label.
- Use fraud-labelled transaction value, not fraud loss prevented or money saved.
- Do not display alerts reviewed, case resolution, turnaround time, geography, channel, product or customer-segment analysis; the source does not support those claims.
- The logistic-regression decision score is not a calibrated probability.
- For the at-or-below-220 cohort, use its independently recalculated rank columns, not the full-population ranks.
- The visual concept board is a moodboard only. Its sample KPI values and fraud-pattern categories are placeholders and must not be copied into the report.

### Current Power BI repository state

The [Power BI guide](../powerbi/README.md) records the import and relationship contract. The owner reported marking `DimDate` as the date table and saving locally. The Review Policy Comparison model script applied and the Desktop reconciliation passed. P5 remains at 0% pending accepted report evidence.

| Check | Status | Evidence |
|---|---|---|
| Notebook 05 on the owner's checkout | Passed | The owner reported the 14 November run and provided the manifest. The five CSVs contained 183 Overview rows, 183 date rows, 287,873 September rank rows, four scenario rows and eight QA rows. The owner's exact checkout SHA and kernel build were unrecorded. |
| Pinned-source reproduction | Passed after dependency fix | At [`017f90c`](https://github.com/Sonkhe-Shongwe/banking-fraud-intelligence/commit/017f90c5c6c760972e24619d5ac13fa5496534e5), `python src/convert_transactions.py` verified all 183 daily files from source revision `6e67dbd0a3bfe0d7ec33abc4bce5f37cd4ff0d6a`. Notebooks 04 and 05 ran via IPython on Linux with Python 3.12.14, pandas 2.2.3 and scikit-learn 1.8.0. Notebook 05 initially stopped at a styled table because Jinja2 was missing. With Jinja2 3.1.6 installed, the complete rerun produced all five CSVs and matched the eight September comparisons. |
| P5.2 daily Overview reconciliation | Passed in Linux and Windows | The earlier ad hoc audit flagged six metrics due to pandas index alignment. The corrected command `python -m src.reconcile_powerbi_overview` matched all seven metrics across 183 dates in the pinned-source Linux reproduction and in the owner's Windows run after pulling [`1cce1e1`](https://github.com/Sonkhe-Shongwe/banking-fraud-intelligence/commit/1cce1e1a481685f4ba3ec1cc02a9e006bd29619c). The owner supplied the terminal result on 14 November 2026. |
| Theme schema | Passed | The committed theme passed Microsoft's Power BI report theme JSON schema 2.159. |
| Power BI Desktop theme import | Passed | On 14 November 2026 the owner imported the approved theme into a blank report in Windows Power BI Desktop. The screenshot shows the app confirming the file was added successfully. Desktop build number and theme rendering on visuals are unverified. |
| Power BI base model | Observed in Desktop | The owner's 14 November screenshot shows four reporting tables, two active one-to-many relationships with single-direction indicators from `DimDate`, and `September_Scenario_Lift` disconnected. Loaded row counts and date-table marking still need verification. |
| Review Policy Comparison model and DAX reconciliation | Passed | In Windows Power BI Desktop on 14 November, the owner applied [`eb9be80`](https://github.com/Sonkhe-Shongwe/banking-fraud-intelligence/commit/eb9be801d26764aa72dc2214cd6fd045f697e8b3) and ran `powerbi/review_policy_checks.dax`. The query returned 183 calendar rows, 183 Overview rows, 287,873 ranks and four scenarios. All 48 metric values across eight full-September comparisons agreed with the pinned Python QA reference at report precision. The restricted 1 September check returned one day, 50 slots per policy, eight baseline, nine model and +1. |
| Power BI report visuals | Not tested | The TMDL editor displayed name-resolution diagnostics after Apply. The DAX query resolved and evaluated the new tables and measures. Report visuals, theme rendering and interactions still need Desktop evidence. |

The reported P5.1 audit passed five file-integrity and nine structural checks on the owner's exports. In the Linux reproduction, hashes, schemas and row counts matched the generated manifest for all five CSVs. The corrected P5.2 audit rejected a changed count and a changed value in disposable copies. The source and original Overview hashes remained identical, and all ten existing regression tests passed.

### Publication boundary

Keep raw files, processed extracts, transaction-level rank exports and reports containing row-level records local. The source snapshot does not include a separate raw-data licence, and permission to redistribute derived artefacts has not been established. Resolve publication scope separately before portfolio release. [Source publication scope](data_sources.md#publication-scope)

## Resume here

1. Save the verified model locally and [build the three Review Policy Comparison cards](../powerbi/README.md#8-build-the-review-policy-kpi-row).
2. Finish the comparison visuals and test slicers, navigation, theme rendering and accessibility in Desktop. Record the Desktop version when available.
3. Finish calendar label sorting before building and reconciling Fraud Overview.

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
| 13 November 2026 | Owner approved P5 wireframe proposal v0.1 as presented, including detailed design tokens and both page layouts. |
| 13 November 2026 | Owner authorised implementation within the approved P5 scope by instructing us to continue. Theme JSON and Notebook 05 prepared; Windows and Power BI Desktop checks remain pending. |
| 13 November 2026 | Audited remote main, corrected stale dark-theme handoff language, established the design system and recorded the P5 readiness audit. |
| 14 November 2026 | Recorded the owner's Notebook 05 outputs, reproduced the reporting export from the pinned source, fixed the P5.2 reconciliation and checked the light theme against Microsoft's schema. |
| 14 November 2026 | Owner screenshots confirmed P5.2 passed in Windows and the approved light theme imported in Power BI Desktop. |
| 14 November 2026 | Owner screenshot confirmed four Power BI reporting tables and two date relationships in Model view. |
| 14 November 2026 | Prepared one script for the Review Policy Comparison controls and measures. On Linux, pandas 2.2.3 reproduced all six QA metrics in all eight cases from the 287,873 local September ranks generated at `017f90c` from the pinned source `6e67dbd0a3bfe0d7ec33abc4bce5f37cd4ff0d6a`. A restricted 1 September test selected 50 reviews per policy, with 8 baseline and 9 model fraud labels. Desktop script execution and reconciliation remain pending. |
| 14 November 2026 | Windows Power BI Desktop applied the comparison model and passed all three DAX query result sets. |
