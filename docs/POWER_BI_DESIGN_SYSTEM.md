# Power BI Design System | Banking Fraud Intelligence

**Status:** Detailed design approved; P5 implementation authorised within the approved scope on 13 November 2026. Current increment: theme and reporting-data preparation.  
**Owner-approved direction:** A — Premium Banking Intelligence.  
**Platform:** Power BI Desktop.  
**Last reviewed:** 13 November 2026.

This document is the working design contract for P5. It records the approved visual identity, page designs, data contract and quality gates. Implementation may proceed within this approved scope; any scope expansion or material design change still requires owner approval.

## 1. Decision register

| Decision | Status | Record |
|---|---|---|
| Power BI Desktop is the dashboard platform | Approved | Owner decision |
| Two-page report: Fraud Overview and Review Policy Comparison | Approved | Owner decision |
| Begin implementation with Review Policy Comparison | Approved in principle | Owner accepted the proposed sequence |
| Premium Banking Intelligence visual direction | Approved | Direction A |
| Light, restrained, executive-grade appearance | Approved as part of Direction A | Owner's stated preference |
| Exact palette and colour roles | Approved | Accepted as presented in P5 wireframe proposal v0.1 |
| Font family and type scale | Approved | Segoe UI approved; local rendering validation remains an implementation test |
| Canvas dimensions and grid | Approved | 16:9 1280 x 720 planning canvas and grid accepted; final rendering check remains an implementation test |
| Exact page wireframes and chart selection | Approved | P5 wireframe proposal v0.1 accepted as presented |
| KPI card construction, iconography and navigation treatment | Approved | Accepted as presented in P5 wireframe proposal v0.1 |
| Transaction-level queue or drillthrough | Not approved | Optional follow-up only |
| Public release of dataset-derived artefacts | Open | Separate data-publication gate |

**Approval boundary:** The owner has authorised implementation within the approved two-page design. Do not add pages, alter the approved visual identity, introduce transaction-level drillthrough or publish dataset-derived artefacts without separate owner approval. Publication and row-level data exposure remain separately gated.

## 2. Product and analytical intent

The report is an analytical interface for a simulated fraud-investigation case study. Its central question is:

> When investigators can review only a fixed number of transactions per day, which ranking policy places more fraud-labelled transactions into the review queue?

The design must communicate evidence rather than imply a live banking operation. The data is simulated, the outcome label is retrospective, and the report does not represent an operational alert-management system.

### Approved page scope

| Page | Primary question | Evidence source |
|---|---|---|
| **Fraud Overview** | What does fraud prevalence and transaction activity look like across the available simulated period? | Validated full transaction CSV |
| **Review Policy Comparison** | At the same daily review capacity, how do amount ranking and logistic regression compare? | September held-out rank export |

The Review Policy Comparison is the approved first build. Both page layouts are approved in [P5 wireframe proposal v0.1](P5_WIREFRAMES_PROPOSAL_v0.1.md). Implementation proceeds within that specification.

## 3. Data contract and truthful metric language

The audited source contains 1,754,155 simulated transactions from 1 April to 30 September 2018, with 14,681 fraud labels (0.837% overall). The P4 September export contains 287,873 rows and one row per September transaction.

### Supported fields

The source contains transaction ID, event timestamp, customer ID, terminal ID, amount, two elapsed-time fields, fraud label and fraud scenario. The September rank export adds a model decision score and four daily rank columns: amount and model ranks for the full population, and amount and model ranks for the amount-at-or-below-220 cohort.

### Approved metric definitions

| Display label | Definition | Required qualification |
|---|---|---|
| Transactions | Count of transaction rows | State selected period |
| Fraud-labelled transactions | Sum of the retrospective TX_FRAUD label | Simulated dataset; not live confirmed alerts |
| Fraud-labelled share | Fraud-labelled transactions divided by all eligible transactions | Prefer this label to an unqualified bank-wide fraud rate |
| Fraud-labelled transaction value | Sum of TX_AMOUNT where TX_FRAUD = 1 | Amount units are not established as a real currency; not loss |
| Reviews selected | Count of rows selected by the policy rank at or below the chosen daily limit | The selected date range determines the number of review days |
| Fraud-labelled transactions selected | Selected rows whose retrospective TX_FRAUD label is 1 | A retrospective evaluation outcome |
| Legitimate reviews | Selected rows minus fraud-labelled transactions selected | Do not call this an operational false-positive rate without qualification |
| Queue precision | Fraud-labelled transactions selected divided by reviews selected | Pooled across the selected days |
| Cohort recall | Fraud-labelled transactions selected divided by all fraud-labelled transactions in the eligible cohort and selected date range | Denominator changes with date range and cohort |
| Fraud-labelled value selected | Sum of amount for selected rows whose retrospective fraud label is 1 | Exposure represented by selected transactions, not money saved |

### Claims and visuals the data does not support

Do not display or imply:

- Fraud loss prevented, money saved, recoveries, chargebacks or financial impact.
- Alerts reviewed, investigation turnaround, case resolution or investigator productivity.
- Confirmed alert, fraud-confirmation or resolution timelines.
- Merchant, channel, product, geography or customer-segment breakdowns. Those fields are not present in the audited source.
- A calibrated fraud probability. The model score is a logistic-regression decision function used for ranking, not a calibrated probability.
- A real-world bank fraud rate or production model effectiveness.

The source has no label-confirmation timestamp. Historical label use therefore depends on the documented feedback-delay assumption. The simulator labels every transaction above 220 as fraud; the at-or-below-220 comparison is a simulator-sensitivity cohort, not a proposed operational threshold. Keep TX_FRAUD_SCENARIO out of predictive inputs and out of the default executive view; it is a retrospective diagnostic field.

## 4. Approved visual identity

The approved direction is **Premium Banking Intelligence**: light, calm, precise, restrained, confident and executive-grade. It should feel like a considered internal banking analytics product, not a generic Power BI starter report.

### Approved colour tokens

These values were approved as presented in P5 wireframe proposal v0.1 and are the source of truth for theme implementation.

| Token | Approved value | Intended role |
|---|---|---|
| Primary navy | #0F172A | Page titles, key labels and strongest text |
| Slate blue | #1E3A5F | Amount-baseline series and structural emphasis |
| Teal | #0F766E | Logistic-regression series and selected actions |
| Secondary text | #475569 | Supporting labels and explanatory text |
| Canvas | #F8FAFC | Main report background |
| Surface | #FFFFFF | Cards and primary visual containers |
| Muted surface | #EEF2F7 | Filter strips and secondary grouping |
| Border | #CBD5E1 | Quiet dividers and control boundaries |
| Amber | #F59E0B | Watchlist or attention marker only |
| Critical red | #DC2626 | Genuine fraud or critical-risk marker only |

Use slate blue consistently for the amount baseline and teal for logistic regression. These colours identify policies; they must not imply that one policy is always better. Use explicit signed differences and labels to show performance. Reserve amber and red for semantically meaningful attention and risk states, not decoration. Do not use amber as small text on a light surface; pair it with a sufficiently dark foreground.

The approved navy, slate, teal and secondary-text colours have strong contrast against the approved light canvas. Every final text/background and icon/background pairing must still be checked in the actual report. Target WCAG 2.1 AA contrast of at least 4.5:1 for normal text and ensure meaningful graphical elements remain distinguishable without colour alone.

### Approved typography hierarchy

**Primary family:** Segoe UI, for reliable Windows and Power BI rendering.

| Element | Approved size | Weight |
|---|---:|---|
| Page title | 24–26 pt | Semibold |
| Page subtitle | 10–11 pt | Regular |
| KPI value | 26–30 pt | Semibold |
| KPI label | 10–11 pt | Semibold |
| Section title | 12–14 pt | Semibold |
| Chart labels and table text | 9–11 pt | Regular |
| Methodology note | 9–10 pt | Regular |

Use consistent number formats, thousands separators and restrained decimal precision. Do not add a currency symbol because the audited source does not establish a real currency unit. The Power BI theme sets report-wide text defaults; page titles, KPI values and individual components will be formatted to the approved hierarchy in Desktop.

### Approved layout and spacing

- **Canvas:** 16:9, 1280 × 720 (HD).
- **Planning grid:** 12 columns, 24 px outer margins, 16 px gutters and an 8 px spacing rhythm.
- Keep a stable header and page navigation at the top, with the filter strip directly below.
- Place headline measures below the filters, followed by the main analytical visual and supporting scorecard/context.
- Align KPI cards, charts and table edges to the same grid. Avoid arbitrary floating elements.
- Keep the highest-priority message in the upper-left reading path, then move from summary to comparison and supporting detail.
- Prefer generous whitespace and subtle separators over heavy borders, stacked shadows or excessive rounded containers.
- Retain the same title, navigation, filter and footer positions across both pages.

The canvas and grid are approved. Final visual positioning, text wrapping and fit must still be inspected in Power BI Desktop at the owner's normal display scaling. The theme JSON does not set canvas dimensions or position visuals.

## 5. Approved page designs

The exact page layouts, hierarchy, components and default states are recorded in the [owner-approved P5 wireframe specification](P5_WIREFRAMES_PROPOSAL_v0.1.md).

### Page 1 — Fraud Overview

**Purpose:** Establish the scale, prevalence and temporal pattern of the simulated dataset.

Approved components:
- Stable report header, two-page navigation and visible **Simulated data** context.
- Date-range control covering 1 April to 30 September 2018.
- Four KPI cards: transaction count, fraud-labelled transaction count, fraud-labelled share and coverage days.
- Weekly fraud-labelled-share line chart with markers.
- Simulator-rule context showing the fraud-label split above and at/below 220.
- Six-month summary table with transaction volume, fraud labels and labelled share.
- Visible methodology footer qualifying the retrospective labels and simulator rule.

### Page 2 — Review Policy Comparison

**Purpose:** Compare amount ranking and logistic regression under the same review capacity and eligible population.

Approved controls:
- Cohort: all transactions or amounts at or below 220.
- Daily review capacity: 50 or 100 reviews per day.
- Date range restricted to September 2018.

Approved components:
- Three headline KPI cards: amount baseline, logistic regression and model difference.
- Daily queue-yield line chart with both policy series.
- Fixed four-scenario September lift matrix.
- Two-row policy scorecard with reviews selected, fraud-labelled transactions selected, legitimate reviews, queue precision, cohort recall and fraud-labelled value selected.
- Visible simulated-data/methodology footer.

The restricted cohort must use its independently recalculated rank columns. Do not filter the full-population ranks and treat them as restricted-cohort ranks.

## 6. Chart and component language

### Prefer

- Line charts for ordered time trends.
- Horizontal bars or a paired dot plot for two-policy comparisons.
- Small, carefully labelled tables for exact metric reconciliation.
- Histograms or binned distributions only when the amount distribution answers a useful question.
- KPI cards that show one number, a clear label, unit/period context and a comparison only when the comparison is valid.
- Restrained line icons as secondary cues where they improve recognition.

### Avoid

- Gauges, 3D charts, decorative donut charts and chart variety without analytical purpose.
- Red/green as the only encoding of good/bad or baseline/model.
- Multiple competing accent colours, gradients, heavy borders and shadows.
- Oversized icons, emoji, generic stock photography or decorative banking imagery.
- Tiny labels, truncated numbers, unexplained percentages and ambiguous axes.
- Trend arrows or prior-period deltas when a valid comparison period has not been defined.

### Iconography

Use one coherent outline-icon family, consistent stroke weight and a restrained size. Icons support labels; they never replace them. Do not use a bank logo or imply affiliation with a real bank. A neutral report title is sufficient; no real-bank logo, external brand affiliation or separate product branding is approved.

## 7. Approved interaction contract

| Interaction | Intended behaviour |
|---|---|
| Page navigation | Consistent, visible navigation between the two approved pages |
| Overview date filter | Filters all supported overview measures and visuals |
| Review-capacity selector | Switches between 50 and 100 reviews per day |
| Cohort selector | Switches between full population and amount-at-or-below-220 ranks |
| September date filter | Changes the selected days while retaining daily capacity semantics |
| Tooltips | Explain metric definitions, denominators, selected period and policy |
| Reset filters | Returns the page to a documented default state |

Cross-filtering must be predictable. Any interaction that changes a denominator must be visible and explained. A transaction-level queue, drillthrough or export of row-level data is not part of the approved first version.

## 8. Accessibility and usability acceptance

- Meet WCAG 2.1 AA contrast for normal text (at least 4.5:1); test all final combinations.
- Never rely on colour alone to distinguish the two policies or communicate risk.
- Provide meaningful titles, labels, units and alternative text for informative visuals.
- Set and test keyboard tab order; verify keyboard navigation.
- Use readable font sizes, clear focus states and consistent filter behaviour.
- Test the report in high-contrast mode where practical.
- Ensure charts can be understood without relying on decorative data labels.

Microsoft's Power BI accessibility guidance covers alternative text, tab order, titles, labels, markers, themes and contrast.

## 9. Design acceptance gates

| Gate | Evidence required | Status |
|---|---|---|
| D0 — Direction | Premium Banking Intelligence, light-theme direction | Approved |
| D1 — Design tokens | Palette, typography, spacing, icon and component rules | **Approved by owner, 13 November 2026** |
| D2 — Page wireframes | Exact layout and visual selection for both pages | **P5 wireframe proposal v0.1 approved by owner, 13 November 2026** |
| D3 — Theme implementation | Approved theme JSON prepared in the repository; import and visual inspection in Power BI Desktop | Prepared; local Desktop verification pending |
| D4 — Report implementation | Approved pages built with supported data only | Not started |
| D5 — Analytical reconciliation | Power BI measures match Python for all eight September policy/cohort/capacity cases and representative date selections | Not started |
| D6 — Interaction and accessibility | Filters, navigation, tooltips, keyboard order, contrast and labels tested | Not started |
| D7 — Owner acceptance | Owner reviews the actual report and approves the result | Not started |
| D8 — Publication clearance | Source reuse and artefact-sharing scope confirmed | Open; separate P1/P6 gate |

P5 remains at 0% until implementation evidence is produced and accepted. Design decisions alone do not earn implementation progress.

## 10. Concept-board warning

The visual identity board generated during the 13 November 2026 design discussion is a **moodboard only**. It illustrates the intended premium, light banking aesthetic and component vocabulary. Its displayed sample values (including transaction totals, rates, monetary amounts, alert counts and fraud-pattern shares) are illustrative placeholders, not results from this project. Do not copy those numbers, labels or unsupported dimensions into Power BI.

## 11. Research references

- [Microsoft — Design Power BI reports for accessibility](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-accessibility-creating-reports)
- [Microsoft — Use report themes in Power BI](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-report-themes)
- [Microsoft — Create custom report themes in Power BI Desktop](https://learn.microsoft.com/en-us/power-bi/create-reports/report-themes-create-custom)
- [Microsoft — Tips for designing a great Power BI dashboard](https://learn.microsoft.com/en-us/power-bi/create-reports/service-dashboards-design-tips)
- [Dribbble — Financial dashboard inspiration](https://dribbble.com/tags/financial-dashboard)
- [Dribbble — Banking dashboard design inspiration](https://dribbble.com/tags/banking-dashboard-design)

Dribbble is an inspiration source, not an authority for analytical correctness or Power BI capability. Microsoft documentation governs platform behaviour and accessibility constraints.


## 12. Research synthesis and approved wireframe specification

The owner-approved detailed layout specification is recorded in [P5 Wireframe Proposal v0.1](P5_WIREFRAMES_PROPOSAL_v0.1.md). It includes both page layouts, hierarchy, icon roles, number treatment, native Power BI interactions, accessibility checks and the approved aggregate overview table.

The external review compared corporate banking dashboard patterns on Dribbble with overview/detail navigation and period controls found in LinkedIn and TikTok analytics interfaces. The useful pattern is a stable page frame, concise KPI summary, readable trend and supporting detail. Social audience metrics, personal wallet components, decorative gauges and unsupported data dimensions are deliberately excluded.

Microsoft's current Power BI documentation confirms support for custom report themes, date and button slicers, 16:9 1280 x 720 canvas settings, grid alignment and accessibility features. These are implementation constraints for the approved design.

**Current gate:** D1 and D2 are approved. The first implementation increment now includes the theme JSON and Notebook 05. D3 remains pending until the owner imports the theme in Power BI Desktop; P5 remains at 0% until report implementation and acceptance evidence are verified.


## 13. Current implementation checkpoint

- **Theme:** [Premium Banking Intelligence theme JSON](../powerbi/themes/Premium_Banking_Intelligence.json) created using documented Power BI theme properties for data colours, structural colours and text classes. JSON syntax is checked; import and rendering still require Power BI Desktop.
- **Reporting preparation:** [Notebook 05](../notebooks/05_power_bi_data_preparation.ipynb) created to validate the full input and P4 rank export, build the daily Overview table and date dimension, inspect the temporal pattern, and reconcile all eight September comparisons.
- **Local outputs:** Generated tables are written to data/processed/powerbi/, which is Git-ignored. Do not commit row-level or derived data.
- **Current limitation:** No PBIX has been created or verified. The owner's Windows run of Notebook 05 and theme import remain the next acceptance checks.
