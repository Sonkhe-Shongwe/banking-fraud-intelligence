# Power BI implementation workspace

**Project:** Banking Fraud Intelligence  
**Approved design:** Premium Banking Intelligence, light theme  
**Platform:** Power BI Desktop  
**Current checkpoint:** Four reporting tables and two date relationships visible in Power BI Desktop

## 1. First local setup

1. Pull the repository.
2. Use the existing Notebook 05 outputs in `data/processed/powerbi/`. If they are missing, follow the [Notebook 05 run guide](../data/README.md#prepare-the-power-bi-reporting-data). From the repository root, run `python -m src.reconcile_powerbi_overview` with the working Python environment. This read-only check compares all seven daily Overview metrics against the validated source and should report 183 matching dates.
3. In Power BI Desktop, create a blank report.
4. On the **Design** ribbon, choose **Import theme** and select the Premium Banking Intelligence JSON in themes/.
5. Confirm that Power BI reports a successful import. Record the installed Power BI Desktop version and inspect the default text and series colours.

The theme sets documented report-wide colour and text defaults. It does not set page dimensions, position visuals, create measures, or apply every per-visual border/radius treatment. Those are applied deliberately during report construction.

Set both report pages to the approved **16:9, 1280 × 720** canvas. Use the approved 12-column planning grid, 24 px outer margins, 16 px gutters and 8 px spacing rhythm.

## 2. Tables to load

Load these four CSV files from data/processed/powerbi/:

| Power BI table | File | Grain | Expected rows |
|---|---|---|---:|
| DimDate | DimDate.csv | One row per date | 183 |
| Overview_Daily | Overview_Daily.csv | One row per date | 183 |
| September_Ranks | September_Ranks.csv | One row per September transaction | 287,873 |
| September_Scenario_Lift | September_Scenario_Lift.csv | One row per cohort/capacity combination | 4 |

Do **not** load September_Queue_Reconciliation_QA.csv. It is a local QA artifact. PowerBI_Data_Manifest.json is a file-integrity record, not a model table.

## 3. Relationship contract

Create the following relationships:

| One side | Many side | Cardinality | Cross-filter direction |
|---|---|---|---|
| DimDate[Date] | Overview_Daily[Date] | One-to-many | Single, from DimDate |
| DimDate[Date] | September_Ranks[Date] | One-to-many | Single, from DimDate |

Additional rules:

- Mark DimDate as the report's date table, using DimDate[Date].
- Keep September_Scenario_Lift disconnected. It is a fixed full-September reference and must not change when the report date range or cohort selector changes.
- Do not create a relationship between Overview_Daily and September_Ranks.
- The review cohort, capacity and policy tables in the measure script stay disconnected.

## 4. Field handling

### Overview_Daily

- Date: Date.
- Transaction and fraud counts: Whole number.
- FraudLabelledTransactionValue: Decimal number; do not assign a currency symbol.
- Simulator-boundary counts: Whole number.

### DimDate

- Date, MonthStartDate, WeekStartDate: Date.
- Year, MonthNumber, DayOfWeekNumber: Whole number.
- MonthName, MonthYear, DayName: Text.
- IsWeekend: True/False.

Sort MonthName by MonthNumber, MonthYear by MonthStartDate, and DayName by DayOfWeekNumber.

### September_Ranks

- Date: Date.
- TX_AMOUNT: Decimal number, without a currency symbol.
- TX_FRAUD: Whole number, used as a retrospective outcome label.
- Four rank columns: Whole number; restricted-cohort ranks are blank for transactions above 220.
- TRANSACTION_ID: retain for uniqueness and reconciliation, but hide from report view.
- Hide the four technical rank columns from report view after measures are created. No transaction-level drillthrough is part of the approved first release.

### September_Scenario_Lift

- Cohort: Text.
- DailyCapacity: Whole number.
- Baseline/model selected fraud-label counts and ModelDifference: Whole number.
- Label it as the full-September reference matrix.

## 5. Approved report scope

**Page 1 — Fraud Overview**
- April–September 2018 date range.
- Four KPI cards: transactions, fraud-labelled transactions, fraud-labelled share and coverage days.
- Weekly fraud-labelled-share trend.
- Simulator amount-boundary context.
- Monthly summary table.
- Visible simulated-data and methodology qualification.

**Page 2 — Review Policy Comparison**
- September 2018 date range.
- Cohort selector: all transactions / amounts at or below 220.
- Daily capacity selector: 50 / 100 reviews per day.
- Amount baseline, logistic regression and model-difference KPI cards.
- Daily queue-yield line chart.
- Fixed four-scenario September lift matrix.
- Two-row policy scorecard and methodology footer.

Build Review Policy Comparison first. Do not add pages, transaction-level drillthrough, unsupported dimensions or unapproved features.

## 6. Current implementation boundary

- Prepared: approved theme JSON, Notebook 05 and this setup guide.
- Verified: Notebook 05 outputs, the corrected Overview check on the owner's Windows checkout and the approved theme import in Power BI Desktop. Model view shows all four reporting tables and both date relationships. Mark `DimDate` as the date table, then check the loaded row counts and calendar sort order.
- Prepared: [Review Policy Comparison measures](review_policy_model.tmdl) and [Desktop reconciliation query](review_policy_checks.dax). Desktop application and reconciliation are pending.

## 7. Apply and check the review policy measures

1. Open the saved local report. In **TMDL view**, paste the contents of [review_policy_model.tmdl](review_policy_model.tmdl) into a new script tab and click **Preview**.
2. Check that the preview adds three disconnected tables (Review Cohort, Review Capacity and Review Policy) and measures under September_Ranks. The four existing table definitions and their relationships should remain intact. Click **Apply** once the preview matches.
3. In **DAX query view**, paste [review_policy_checks.dax](review_policy_checks.dax) and click **Run**. If the new selector tables are unprocessed, use **Home → Refresh** before rerunning the checks.
4. The three result sets should show row counts of **183, 183, 287,873 and 4** in the query's column order, the eight full-September comparisons, and a one-day check for 1 September with the restricted cohort at 50/day. The one-day check should show **1 day, 50 slots per policy, 8 baseline, 9 model and +1**. Compare all six metrics for the eight full-September rows to the local `September_Queue_Reconciliation_QA.csv` at display precision. The full-month default is **589 baseline, 592 model and +3**.

The script uses the existing four daily rank fields, including the independently recalculated restricted ranks. The policy scorecard uses Review Policy[Policy] as its row field. For the report slicers, use single select for cohort and capacity and set the default to All transactions and 50 reviews per day.
- Publication remains separate: generated reporting data stays local until dataset-derived publication permissions are resolved.
