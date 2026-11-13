# P5 Wireframe Proposal v0.1
**Project:** Banking Fraud Intelligence  
**Prepared:** 13 November 2026  
**Status:** Non-binding design proposal for owner review  
**Authority:** Research and wireframe proposal only. This document does not authorise Power BI implementation, final theme import, a change in page scope, or publication.

## 1. Design objective

Create a premium, executive-grade fraud intelligence report that feels like a carefully designed banking analytics product rather than a default Power BI canvas. The interface should be visually rich through hierarchy, spacing, typography, meaningful icons, aligned components and deliberate interactions, not through decorative clutter.

The report must tell the truth about a simulated retrospective evaluation. It must not imply a live fraud-monitoring operation, confirmed alert workflow, recovered money, prevented loss or production model performance.

### Product principles

1. **Decision before decoration.** Each visual must answer a defined question.
2. **One reading path.** Page title, context, key measures, trend and supporting evidence should be encountered in a predictable order.
3. **Visible context.** Every headline value carries a label, period, cohort and unit where applicable.
4. **Comparison is controlled.** Both ranking policies use the same eligible transactions and the same daily review capacity.
5. **Interactivity is deliberate.** Controls are visible, their current state is obvious, and their effects are predictable.
6. **Premium restraint.** Use a small colour system, precise alignment, quiet surfaces and consistent icons. Avoid visual noise.
7. **Evidence over implication.** No unsupported metric, invented comparison, or decorative chart.

## 2. External design research

The research was used to extract reusable interface patterns, not to copy another product.

| Reference | Observed design pattern | What we should adopt | What we should reject |
|---|---|---|---|
| Dribbble, Dashboard of Corporate Banking by Will | A multi-zone corporate banking canvas with a compact context panel, central trend visual and transaction table; restrained cool neutrals and green accents | Strong panel alignment, clear separation of context and analysis, compact data tables, consistent card edges | The news column and circular gauge are not useful for our data story |
| Dribbble banking dashboard gallery | Modular KPI cards, repeated component styles, compact navigation and clear section groupings | Reusable cards, consistent component sizing, clear active navigation state | Personal wallet, card-management and spending-category content that our dataset does not contain |
| TikTok Studio analytics | Overview/content navigation, period controls, headline metrics and a time-series trend | Visible date context, concise KPI summary, clear transition from overview to detail | Audience, content thumbnails, traffic-source breakdowns and mobile-first density that do not fit this dataset |
| LinkedIn analytics | Overview tabs, metric highlights, date selection, trend panels and detailed performance views | Clear page-level navigation, period comparison only when valid, overview-to-detail hierarchy | Demographics, post previews, engagement metrics and competitor comparisons not present in our data |
| Microsoft Power BI guidance | Theme-level defaults, grid and snap-to-grid, on-canvas slicers, report navigation and accessibility configuration | Use a custom report theme, aligned canvas grid, visible slicers, accessible labels and predictable visual interactions | Excessive visuals, custom visuals without a clear need, and visual styling that cannot be maintained consistently |

### Research interpretation

The strongest pattern across the professional examples is not the number of widgets. It is the consistency of the system: a clear header, a controlled set of headline measures, a readable trend, supporting detail, and navigation or filters that remain in stable positions.

Social analytics products also separate overview from detailed analysis. We can use that structural idea, but our pages must follow the fraud-investigation questions and available transaction data.

Dribbble is an inspiration source, not an authority for analytical correctness. Microsoft documentation governs Power BI capabilities and accessibility constraints.

## 3. Proposed visual identity

The owner-approved direction remains **A - Premium Banking Intelligence**, with a light, restrained and executive-grade appearance. The current proposed palette is retained for review; this proposal does not make it final.

### 3.1 Colour roles

| Role | Candidate | Usage |
|---|---|---|
| Main canvas | #F8FAFC | Cool, very light report background |
| Card surface | #FFFFFF | KPI cards, charts and tables |
| Primary text | #0F172A | Page titles, KPI values and strongest labels |
| Secondary text | #475569 | Supporting labels, axis labels and explanatory text |
| Amount baseline | #1E3A5F | Consistent identity for the amount-ranking policy |
| Logistic regression | #0F766E | Consistent identity for the model policy |
| Muted surface | #EEF2F7 | Filter groups and secondary information panels |
| Divider / border | #CBD5E1 | Quiet separators and card boundaries |
| Attention | #F59E0B | Simulator caveat and methodology warnings only |
| Critical | #DC2626 | Only where a genuinely critical state must be communicated |

Policy colours identify the method, not whether its result is good or bad. Use a neutral signed difference and explicit labels to show which method selected more or fewer fraud-labelled transactions. Never use red and green as the only comparison signal.

### 3.2 Typography

**Preferred family:** Segoe UI, for reliable Windows and Power BI rendering.

| Element | Proposed size | Weight |
|---|---:|---|
| Page title | 24-26 pt | Semibold |
| Page subtitle | 10-11 pt | Regular |
| KPI value | 26-30 pt | Semibold |
| KPI label | 10-11 pt | Semibold |
| Section title | 12-14 pt | Semibold |
| Chart labels and table text | 9-11 pt | Regular |
| Methodology note | 9-10 pt | Regular |

Use consistent number formats, thousands separators and restrained decimal precision. Do not add a currency symbol because the audited source does not establish a real currency unit.

### 3.3 Component styling

- White surfaces on the light canvas, with a fine border and a restrained 6-8 px corner radius.
- Avoid stacked shadows, thick outlines, gradients and large decorative illustrations.
- Use one consistent outline icon family. Icons should be small, approximately 16-20 px, and support a written label rather than replace it.
- Put icons in small muted containers where they improve recognition. Do not put an icon on every chart or every data point.
- Use a slim teal active-state underline or pale teal fill for selected navigation and slicer options.
- Keep baseline and model colours consistent across both pages.
- Use a compact top navigation rather than a permanent wide sidebar, preserving canvas space for analysis.
- Use no bank logo, brand affiliation, stock photography or invented product identity.

## 4. Canvas and layout system

**Proposed page size:** 16:9, 1280 x 720 (HD). Microsoft lists this as a standard widescreen canvas size. The final layout must be inspected in Power BI Desktop at the owner's normal display scaling.

**Planning grid:** 12 columns, 24 px outer margins, 16 px gutters and an 8 px spacing rhythm. Use Power BI gridlines and snap-to-grid while arranging visuals.

**Page frame:**
- Stable header and navigation at the top.
- Stable filter strip immediately below the header.
- Headline measures below the filters.
- Main analysis in the centre of the page.
- Supporting scorecard or methodology context below or beside the main visual.
- No scrollbars at the target desktop size.

The same title, navigation, filter and footer positions should be retained on both pages. Date slicers will occupy the same location but will have different valid ranges: April-September on Fraud Overview and September only on Review Policy Comparison. They should not be synced because the two pages have different analytical scopes.

## 5. Page 2 wireframe - Review Policy Comparison

**Build order:** First report page to implement after detailed design approval.

**Question:** At the same daily review capacity, which ranking policy places more fraud-labelled transactions in the selected review queue?

**Default state proposed:** All transactions, 50 reviews per day, full September 2018 holdout period.

### 5.1 Layout sketch

    1280 x 720 REPORT CANVAS
    ┌──────────────────────────────────────────────────────────────────────────┐
    │ BANKING FRAUD INTELLIGENCE       [Fraud Overview] [Policy Comparison]    │
    │ REVIEW POLICY COMPARISON                     SIMULATED DATA               │
    │ Which ranking policy performs better at the same daily review capacity? │
    ├──────────────────────────────────────────────────────────────────────────┤
    │ COHORT [All transactions] [Amounts <= 220]                               │
    │ DAILY CAPACITY [50 / day] [100 / day]       PERIOD [01 Sep - 30 Sep]      │
    │ 30 days selected  |  1,500 review slots per policy                       │
    ├───────────────────────┬───────────────────────┬──────────────────────────┤
    │ AMOUNT BASELINE       │ LOGISTIC REGRESSION   │ MODEL DIFFERENCE         │
    │ 589                   │ 592                   │ +3                       │
    │ Fraud-labelled rows   │ Fraud-labelled rows   │ More selected rows       │
    ├───────────────────────────────────────────────┬──────────────────────────┤
    │ DAILY QUEUE YIELD                             │ SEPTEMBER SCENARIO LIFT  │
    │ Two-series line chart                         │                          │
    │ Amount baseline vs Logistic regression       │  All transactions        │
    │ One point per selected day                    │  50/day       +3         │
    │                                               │  100/day      +10        │
    │                                               │                          │
    │                                               │  Amounts <= 220           │
    │                                               │  50/day       +3         │
    │                                               │  100/day      +9         │
    ├──────────────────────────────────────────────────────────────────────────┤
    │ POLICY SCORECARD: two rows, same review capacity                         │
    │ Policy | Reviews | Fraud-labelled selected | Legitimate reviews         │
    │        | Queue precision | Cohort recall | Fraud-labelled value selected│
    ├──────────────────────────────────────────────────────────────────────────┤
    │ September simulated holdout. Labels are retrospective. Selected value  │
    │ is transaction amount, not loss prevented or money saved.               │
    └──────────────────────────────────────────────────────────────────────────┘

The sketch is a layout proposal, not a screenshot or final pixel specification.

### 5.2 Component specification

| Component | Proposed treatment | Purpose |
|---|---|---|
| Page header | Title, short decision question, simulated-data badge, two-page navigation | Establish identity and context immediately |
| Cohort selector | Two-button slicer: All transactions / Amounts at or below 220 | Selects the eligible ranking population |
| Daily capacity selector | Two-button slicer: 50 / 100 reviews per day | Keeps the policy comparison at equal capacity |
| Date range | Between-style date slicer restricted to September 2018 | Allows examination of the full holdout or a subset of days |
| Review-slot context | Dynamic text such as 30 days selected and 1,500 review slots per policy | Prevents confusion between daily capacity and total selected rows |
| Three KPI cards | Amount baseline, Logistic regression, Model difference | Makes the main comparison immediately legible |
| Daily queue-yield chart | Two-series line chart with visible markers and stable policy colours | Shows whether the aggregate result is consistent across days |
| Scenario-lift matrix | Compact 2 x 2 matrix of full-September model-minus-baseline differences | Keeps all four approved cohort/capacity results visible |
| Policy scorecard | Two-row table with comparable denominators and exact metrics | Provides auditability beyond the headline count |
| Methodology footer | Visible qualification about simulated data, retrospective labels and value interpretation | Prevents misleading operational or financial claims |

### 5.3 Verified September values for the scenario-lift matrix

The values below are taken from the recorded September held-out findings. Differences are Logistic regression minus Amount baseline, across all 30 September days.

| Eligible cohort | 50 reviews/day | 100 reviews/day |
|---|---:|---:|
| All transactions | +3 | +10 |
| Amounts at or below 220 | +3 | +9 |

The default KPI state, All transactions at 50 reviews/day, should therefore show 589 for the amount baseline, 592 for logistic regression and a difference of +3.

For context, each policy fills 1,500 review slots at 50/day across 30 days, or 3,000 at 100/day. Queue precision can be calculated as fraud-labelled selected rows divided by selected review rows. These derived values are useful cross-checks, but the final Power BI measures must be reconciled to the local P4 export.

### 5.4 Scorecard metric contract

| Display metric | Calculation | Required label or note |
|---|---|---|
| Reviews selected | Count of rows with the relevant daily rank at or below the selected capacity | Total depends on selected days and daily capacity |
| Fraud-labelled transactions selected | Selected rows where TX_FRAUD = 1 | Retrospective outcome |
| Legitimate reviews | Reviews selected minus fraud-labelled transactions selected | Do not imply a confirmed operational false-positive rate |
| Queue precision | Fraud-labelled selected / reviews selected | Pooled over the selected date range |
| Cohort recall | Fraud-labelled selected / all fraud-labelled transactions in the selected cohort and date range | Denominator changes with cohort and date selection |
| Fraud-labelled value selected | Sum of TX_AMOUNT for selected fraud-labelled rows | Amount units are not established; not loss or savings |

The model decision score must not be presented as a calibrated fraud probability.

### 5.5 Interaction proposal

1. Cohort and daily capacity button slicers update the KPI cards, daily trend and scorecard.
2. Date range selection updates the selected-day count, total review slots, KPI cards, trend and scorecard.
3. Selecting a day in the trend may cross-filter the scorecard to that day, provided the resulting denominator is made explicit.
4. The four-cell scenario matrix remains a fixed full-September reference and is clearly labelled as such. It should not silently change when the date range is narrowed.
5. A reset button returns the page to All transactions, 50/day and the full September period.
6. Dynamic titles and context text always reflect the active cohort, capacity and date range.
7. Important metric definitions remain visible in the scorecard or methodology area; tooltips provide supplementary detail only.

For the amount-at-or-below-220 cohort, use the independently recalculated restricted rank columns. Never filter the full-population rank columns and treat the result as the restricted queue.

## 6. Page 1 wireframe - Fraud Overview

**Question:** What does the simulated transaction population and retrospective fraud-label pattern look like across the available six months?

### 6.1 Layout sketch

    1280 x 720 REPORT CANVAS
    ┌──────────────────────────────────────────────────────────────────────────┐
    │ BANKING FRAUD INTELLIGENCE       [Fraud Overview] [Policy Comparison]    │
    │ FRAUD OVERVIEW                                  SIMULATED DATA            │
    │ Transaction activity and retrospective fraud-label prevalence           │
    ├──────────────────────────────────────────────────────────────────────────┤
    │ PERIOD [01 Apr 2018 - 30 Sep 2018]                  [Reset filters]      │
    ├────────────────────┬────────────────────┬────────────────────┬───────────┤
    │ TRANSACTIONS       │ FRAUD-LABELLED     │ LABELLED SHARE     │ COVERAGE  │
    │ 1,754,155          │ 14,681             │ 0.837%             │ 183 days  │
    ├─────────────────────────────────────────────────┬────────────────────────┤
    │ FRAUD-LABELLED SHARE OVER TIME                  │ SIMULATOR RULE CONTEXT  │
    │ Weekly line chart, with markers                 │                        │
    │                                                 │ 3,258 labels above 220  │
    │                                                 │ 22.2% of all labels     │
    │                                                 │                        │
    │                                                 │ 11,423 at/below 220     │
    │                                                 │ 77.8% of all labels     │
    ├──────────────────────────────────────────────────────────────────────────┤
    │ MONTHLY SUMMARY: transaction volume | fraud labels | labelled share     │
    ├──────────────────────────────────────────────────────────────────────────┤
    │ All transactions are simulated. Every transaction above 220 is labelled │
    │ fraud by the simulator. The 220 boundary is not a production threshold. │
    └──────────────────────────────────────────────────────────────────────────┘

### 6.2 Component specification

| Component | Proposed treatment | Purpose |
|---|---|---|
| Header and page navigation | Same system as Page 2 | Keeps the two-page report coherent |
| Date range | Date slicer covering 1 April to 30 September 2018 | Sets the reporting period |
| Transactions | 1,754,155 at full-period default | Shows source scale |
| Fraud-labelled transactions | 14,681 at full-period default | Shows retrospective outcome count |
| Fraud-labelled share | 0.837% at full-period default | Normalises fraud labels against transaction volume |
| Coverage | 183 days at full-period default | Makes the observation window explicit |
| Weekly fraud-labelled share | Line chart with markers | Shows prevalence over time without implying an operational alert stream |
| Simulator rule context | Two labelled figures and a caution note | Explains why the <=220 sensitivity cohort matters |
| Monthly summary | Six-row table calculated from the validated transaction input | Allows exact month-by-month comparison |
| Methodology footer | Simulated source and deterministic amount-rule caveat | Keeps interpretation honest |

The monthly table and weekly trend must be populated from the validated full transaction CSV. Their values should not be invented or copied from the design moodboard. If the weekly rate is too volatile or visually noisy, test monthly aggregation before choosing the final chart.

### 6.3 Amount-rule context

The source audit records:
- 3,258 transactions above 220, all labelled fraud by the simulator.
- 11,423 fraud-labelled transactions at or below 220.
- 3,258 represents 22.2% of all 14,681 fraud labels.
- The restricted cohort is a sensitivity analysis that removes the deterministic high-amount group. It is not a production threshold recommendation.

Use a horizontal split bar or two aligned metric rows. Do not use a decorative donut or a gauge for this information.

## 7. Iconography, number treatment and micro-UI

### Proposed icon roles

| Area | Candidate icon meaning |
|---|---|
| Report identity | Neutral shield / analytics mark, not a bank logo |
| Transactions KPI | Transaction or receipt |
| Fraud-labelled KPI | Shield alert |
| Labelled share KPI | Percentage |
| Coverage KPI | Calendar |
| Amount baseline | Scale / ranking |
| Logistic regression | Model / chart-line |
| Difference | Compare / arrow-left-right |
| Date control | Calendar |
| Reset | Refresh / undo |

Use one outline family and one consistent stroke weight. Icons are secondary to the text and values. Do not use emoji or unrelated illustrations.

### Number formatting

- Counts: comma-separated integers, no unnecessary decimal places.
- Percentages: one decimal place for queue precision; three decimals for the overall 0.837% share where precision is meaningful.
- Differences: explicit plus or minus sign, with the unit named nearby.
- Review capacity: always expressed as reviews per day.
- Selected totals: always pair with selected day count.
- Monetary values: no currency symbol until a real unit is established; use the label fraud-labelled transaction value selected.

## 8. Power BI implementation feasibility

The proposal intentionally favours native Power BI visuals and interactions:
- Custom report theme JSON for report-wide colour, typography and visual defaults.
- Native card visuals for headline values.
- Native line chart with markers for the daily queue comparison and weekly overview.
- Native table or matrix for exact metric reconciliation.
- Button slicers for cohort and capacity, where the selected state is clearly visible.
- Date-range slicers for the distinct date windows.
- Native page navigation and a reset bookmark/button.

Power BI supports report themes, custom JSON themes, button slicers with images and labels, date-range slicers, gridlines and snap-to-grid. The final component choice must be verified in the installed Power BI Desktop version.

### Proposed data model for P5

This is a design recommendation, not an implementation decision.

| Table | Grain | Purpose |
|---|---|---|
| Overview_Daily | One row per date, optionally split by the simulator amount-rule group | Small, aggregated input for Page 1 trends and monthly summaries |
| September_Ranks | One row per September transaction | Supports daily ranks, policy comparison and selected-queue measures on Page 2 |
| DimDate | One row per calendar date | Shared date context across the report |
| Capacity selector | One row per supported capacity | 50 or 100 reviews per day |
| Cohort selector | One row per supported cohort | Full population or amount at/below 220 |

Python should create and validate the small overview aggregate. The September rank export remains the source for the P4 policy comparison. Keep row-level data local. No transaction-level drillthrough or public export is proposed for this first report.

The report should not load redundant transaction-level copies into the semantic model unless a measured requirement justifies them.

## 9. Accessibility and quality gates

- Normal text/background contrast must meet WCAG 2.1 AA at 4.5:1.
- Use markers and labels as well as colour to distinguish policy series.
- Add meaningful alternative text to informative visuals.
- Set keyboard tab order to follow the visible reading order.
- Keep slicer positions and styles consistent across pages.
- Ensure important conclusions are visible without hover or tooltip interaction.
- Check titles, axis labels, units, number formats and sort order.
- Test high-contrast mode and a squint test at the target canvas size.
- Use Power BI gridlines and snap-to-grid for alignment.
- No visual should be present merely to fill space.

## 10. Approval checklist

The following decisions remain with the owner. Nothing in this proposal is final until accepted.

| Decision | Current proposal | Owner status |
|---|---|---|
| Light premium banking palette | Navy, slate blue, teal, white and cool neutrals | Pending |
| Segoe UI type system | Proposed type hierarchy | Pending |
| 16:9 1280 x 720 canvas | HD widescreen | Pending |
| Compact top navigation | Two-page horizontal navigation | Pending |
| Review Policy Comparison layout | Header, filters, three KPIs, daily trend, scenario matrix, scorecard and methodology footer | Pending |
| Fraud Overview layout | Four KPIs, weekly trend, simulator-rule context, monthly summary and methodology footer | Pending |
| Native Power BI slicers and visuals | Prefer native components over custom visuals | Pending |
| Proposed aggregated Overview_Daily table | Generate from validated source in Python | Pending |
| No transaction-level drillthrough | Keep first report focused on aggregate analysis | Pending |

### What approval will authorise

Approval of the detailed design will authorise the next scoped P5 increment: create the theme JSON and the approved data-preparation outputs, then build the Review Policy Comparison page first. It will not authorise public publication or sharing of row-level data. Publication clearance remains separate.

## 11. Research references

### Design inspiration
- [Dribbble - Dashboard of Corporate Banking by Will](https://dribbble.com/shots/15659393-Dashboard-of-Corporate-Banking)
- [Dribbble - Banking Dashboard Design](https://dribbble.com/tags/banking-dashboard-design)
- [Dribbble - Financial Analytics Dashboard](https://dribbble.com/search/financial-analytics-dashboard)
- [Dribbble - Modern Financial Analytics Dashboard](https://dribbble.com/shots/27640184-Modern-Financial-Analytics-Dashboard)

### Product-interface patterns
- [Buffer - TikTok Analytics guide and dashboard examples](https://buffer.com/resources/tiktok-analytics/)
- [University of Michigan - LinkedIn best practices and analytics example](https://socialmedia.umich.edu/wp-content/uploads/sites/30/2023/11/LinkedIn-Best-Practices-Nov-2023.pdf)

### Power BI platform and accessibility
- [Microsoft - Power BI reports overview and interactions](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-reports-overview)
- [Microsoft - Use report themes in Power BI](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-report-themes)
- [Microsoft - Power BI accessibility](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports)
- [Microsoft - Slicer visual](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-slicer-visual)
- [Microsoft - Button slicer](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-button-slicer)
- [Microsoft - Page size and canvas settings](https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-report-display-settings)
- [Microsoft - Tips for creating reports](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-tips-and-tricks-for-creating-reports)

---

**Design gate:** P5 remains at 0%. This is a documented proposal for owner review, not a built report, final theme or implementation acceptance.
