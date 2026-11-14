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

The original light design and the two-page scope were approved on 13 November 2026. On 14 November the owner requested a darker preview and directed changes to its brand, title, methodology placement and slicer order. After the documentation audit, the owner authorised implementing [Fraud Triage](FRAUD_TRIAGE_DESIGN_PROPOSAL.md) as the comparison page. The builder is ready for Desktop verification.

| Page | Intended purpose | Verified input | Design status |
|---|---|---|---|
| Fraud Overview | Show simulated transaction activity, fraud-labelled count/share and trends over the available period | Validated full transaction CSV | **Detailed design approved; implementation foundation prepared** |
| Fraud Triage | Compare amount ranking and logistic regression at 50 or 100 reviews/day, across all transactions or amounts at or below 220 | Local September rank CSV | **Light comparison observed in Desktop. Dark Fraud Triage builder verified against fixtures and ready for Desktop checks.** |

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
| Power BI base model | Observed in Desktop | The owner's 14 November screenshot shows four reporting tables, two active one-to-many relationships from `DimDate` and a disconnected `September_Scenario_Lift`. The DAX check below verified the loaded row counts. The owner reported marking `DimDate` as the date table. |
| Review Policy Comparison model and DAX reconciliation | Passed | In Windows Power BI Desktop on 14 November, the owner applied [`eb9be80`](https://github.com/Sonkhe-Shongwe/banking-fraud-intelligence/commit/eb9be801d26764aa72dc2214cd6fd045f697e8b3) and ran `powerbi/review_policy_checks.dax`. The query returned 183 calendar rows, 183 Overview rows, 287,873 ranks and four scenarios. All 48 metric values across eight full-September comparisons agreed with the pinned Python QA reference at report precision. The restricted 1 September check returned one day, 50 slots per policy, eight baseline, nine model and +1. |
| TMDL editor diagnostics | Observed | The editor displayed name-resolution diagnostics after Apply. The Desktop DAX query resolved and evaluated the new tables and measures. |
| Review Policy Comparison cards | Default values passed | The owner's 14 November Desktop screenshot shows the three native cards with 589 for the amount baseline, 592 for logistic regression and +3 model difference. Two labels are clipped and the cards need alignment. Canvas dimensions, final styling and filter behaviour still need verification. |
| Comparison page build at `5fed1b8` | Opened in Desktop | The owner's Windows run applied the layout and saved a backup. Desktop showed the three correct default cards, both policy lines and four fixed reference values. The chart subtitle used generated measure names, the matrix columns were cramped and the second scorecard row clipped. The 100/day interaction is pending. |
| Light layout polish at `438bd22` | Desktop check open | The [builder](../powerbi/build_review_policy_page.py) supports updating its existing comparison page. The update targets chart labelling, matrix readability and both scorecard rows. |
| Fraud Triage design preview | Implementation authorised | The owner requested a standalone logo and slicers above the result cards, then approved continuing after the documentation audit. The preview used reconciled September aggregates. [Design specification](FRAUD_TRIAGE_DESIGN_PROPOSAL.md) |
| Fraud Triage builder | Passed in Linux fixtures | Python 3.12.14 verified the upgrade from the light and three-card layouts, no-write preview, filter preservation, layout bounds, logo registration, backups, rerun safety and rollback after an injected failure. Fourteen generated PBIR JSON files passed Microsoft schema validation, and all ten existing Python regression tests passed. Desktop rendering and interaction checks remain open. [Desktop instructions](../powerbi/README.md#10-apply-and-verify-fraud-triage) |

The reported P5.1 audit passed five file-integrity and nine structural checks on the owner's exports. In the Linux reproduction, hashes, schemas and row counts matched the generated manifest for all five CSVs. The corrected P5.2 audit rejected a changed count and a changed value in disposable copies. The source and original Overview hashes remained identical, and all ten existing regression tests passed.

### Publication boundary

Keep raw files, processed extracts, transaction-level rank exports and reports containing row-level records local. The source snapshot does not include a separate raw-data licence, and permission to redistribute derived artefacts has not been established. Resolve publication scope separately before portfolio release. [Source publication scope](data_sources.md#publication-scope)

## Resume here

1. Pull `main` and [apply Fraud Triage](../powerbi/README.md#10-apply-and-verify-fraud-triage) to the saved local Power BI Project.
2. Record the Desktop build number and verify visual rendering, the four monthly scenarios, the restricted single-day slice, keyboard access to the Help tooltip and the fixed reference values.
3. Complete calendar label sorting, then build and reconcile Fraud Overview. Verify navigation and reset controls on the two-page report.

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
| 14 November 2026 | Owner screenshot confirmed the three Review Policy Comparison cards display the expected default values. |
| 14 November 2026 | Prepared a local PBIR page builder. The Python fixture run on Linux verified preview, apply, original-page backup, repeat-run protection, binding preservation and layout bounds. The page and visual JSON passed Microsoft's PBIR schemas. The owner needs to run and inspect the result in Desktop. |
| 14 November 2026 | Recorded the first Desktop layout and the subsequent light polish. Captured the darker Fraud Triage preview and the owner-requested title, logo, methodology and slicer placement decisions in the design proposal. [Documentation audit](PROJECT_AUDIT_2026-11-14.md) |
