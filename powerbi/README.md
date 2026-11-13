# Power BI implementation workspace

**Project:** Banking Fraud Intelligence  
**Approved design:** Premium Banking Intelligence, light theme  
**Platform:** Power BI Desktop  
**Current checkpoint:** Theme and reporting-data preparation foundation

## 1. First local setup

1. Pull the repository.
2. Run Notebook 05 — Power BI data preparation. It writes the approved import tables to the Git-ignored data/processed/powerbi/ folder.
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
- Cohort and daily-capacity selectors will be disconnected tables defined in the DAX increment.

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
- Pending local checks: run Notebook 05 in the owner's Windows Python environment and import/inspect the theme in Power BI Desktop.
- Not yet created: PBIX, semantic model, DAX measure set or finished visuals.
- Publication remains separate: generated reporting data stays local until dataset-derived publication permissions are resolved.
