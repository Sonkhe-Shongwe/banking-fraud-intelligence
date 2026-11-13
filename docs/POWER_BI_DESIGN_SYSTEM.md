# Power BI Design System | Banking Fraud Intelligence

**Status:** Design direction approved. Detailed tokens, page wireframes and visual treatments are proposals pending owner approval.  
**Owner-approved direction:** A — Premium Banking Intelligence.  
**Platform:** Power BI Desktop.  
**Last reviewed:** 13 November 2026.

This document is the working design contract for P5. It records what has been approved, what is proposed, what the available data can support, and the quality gates required before a report is accepted. It does not authorise implementation of unapproved layouts or design changes.

## 1. Decision register

| Decision | Status | Record |
|---|---|---|
| Power BI Desktop is the dashboard platform | Approved | Owner decision |
| Two-page report: Fraud Overview and Review Policy Comparison | Approved | Owner decision |
| Begin implementation with Review Policy Comparison | Approved in principle | Owner accepted the proposed sequence |
| Premium Banking Intelligence visual direction | Approved | Direction A |
| Light, restrained, executive-grade appearance | Approved as part of Direction A | Owner's stated preference |
| Exact palette and colour roles | Proposed | Requires review and approval |
| Font family and type scale | Proposed | Requires review and local rendering check |
| Canvas dimensions and grid | Proposed | Requires review in Power BI Desktop |
| Exact page wireframes and chart selection | Pending | Must be shown for approval |
| KPI card construction, iconography and navigation treatment | Proposed | Must be shown for approval |
| Transaction-level queue or drillthrough | Not approved | Optional follow-up only |
| Public release of dataset-derived artefacts | Open | Separate data-publication gate |

**Approval boundary:** Do not create or modify the report, import a final theme, change page scope, add a new page, expose transaction-level data, or make another material design decision until the owner has approved the relevant proposal. Small documentation corrections that preserve these decisions are authorised.

## 2. Product and analytical intent

The report is an analytical interface for a simulated fraud-investigation case study. Its central question is:

> When investigators can review only a fixed number of transactions per day, which ranking policy places more fraud-labelled transactions into the review queue?

The design must communicate evidence rather than imply a live banking operation. The data is simulated, the outcome label is retrospective, and the report does not represent an operational alert-management system.

### Approved page scope

| Page | Primary question | Evidence source |
|---|---|---|
| **Fraud Overview** | What does fraud prevalence and transaction activity look like across the available simulated period? | Validated full transaction CSV |
| **Review Policy Comparison** | At the same daily review capacity, how do amount ranking and logistic regression compare? | September held-out rank export |

The Review Policy Comparison is the planned first build. Exact layouts remain subject to owner approval.

## 3. Data contract and truthful metric language

The audited source contains 1,754,155 simulated transactions from 1 April to 30 September 2018, with 14,681 fraud labels (0.837% overall). The P4 September export contains 287,873 rows and one row per September transaction.

### Supported fields

The source contains transaction ID, event timestamp, customer ID, terminal ID, amount, two elapsed-time fields, fraud label and fraud scenario. The September rank export adds a model decision score and four daily rank columns: amount and model ranks for the full population, and amount and model ranks for the amount-at-or-below-220 cohort.

### Candidate measure definitions

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

## 4. Proposed visual identity

The approved direction is **Premium Banking Intelligence**: light, calm, precise, restrained, confident and executive-grade. It should feel like a considered internal banking analytics product, not a generic Power BI starter report.

### Initial colour-token proposal

These are starting tokens for review, not final approved values.

| Token | Candidate | Intended role |
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

The candidate navy, slate, teal and secondary-text colours have strong contrast against the proposed light canvas. Every final text/background and icon/background pairing must still be checked in the actual report. Target WCAG 2.1 AA contrast of at least 4.5:1 for normal text and ensure meaningful graphical elements remain distinguishable without colour alone.

### Typography proposal

- Primary family: Segoe UI as the dependable Windows/Power BI baseline.
- Optional alternative: Inter only if installed and verified on the owner's machine and in the exported report.
- Page title: approximately 28–32 px.
- Section heading: approximately 16–18 px.
- KPI value: approximately 28–32 px.
- KPI label: approximately 12–13 px.
- Body and chart labels: approximately 12–14 px.
- Footnotes and data definitions: approximately 10–11 px, never so small that they become unreadable.

These are design targets. Final Power BI formatting values must be checked at the intended display size. Use tabular number styling where available, consistent decimal precision, thousands separators and explicit units. Do not add a currency symbol until the dataset's monetary unit is verified.

### Layout and spacing proposal

- Desktop-first 16:9 canvas; confirm the exact page size after a Power BI Desktop preview.
- Use a consistent page header, clear page navigation and a compact filter area.
- Use a 12-column layout as a planning grid, with approximately 24–32 px outer margins and 16–24 px gutters.
- Use an 8 px spacing rhythm for consistent gaps and alignment.
- Align KPI cards and chart edges to the same grid. Avoid arbitrary floating elements.
- Keep the highest-priority message in the upper-left reading path, then move from summary to comparison and supporting detail.
- Prefer generous whitespace and subtle separators over heavy borders, stacked shadows or excessive rounded containers.

The grid and measurements are proposals. They are not final until reviewed in Power BI Desktop at the intended screen resolution.

## 5. Page design briefs

These briefs define the intended analytical story. They are not final wireframes.

### Page 1 — Fraud Overview

**Purpose:** Establish the scale, prevalence and temporal pattern of the simulated dataset.

Candidate components:
- Page title and a visible **Simulated dataset** context label.
- Date-range filter covering the audited period.
- Four candidate KPI cards: transaction count, fraud-labelled transaction count, fraud-labelled share and fraud-labelled transaction value.
- A time-series visual for fraud-labelled activity or share over time.
- A supporting transaction-amount distribution visual, only if it adds a clear and defensible insight.
- A compact source/methodology note that explains the retrospective label and selected period.

Do not add product, channel, geography, merchant or customer-segment visuals because those dimensions are unavailable.

### Page 2 — Review Policy Comparison

**Purpose:** Compare two ranking policies under the same review capacity and eligible population.

Candidate controls:
- Daily review capacity: 50 or 100.
- Cohort: all transactions or amounts at or below 220.
- Date selection restricted to the September 2018 holdout period.

Candidate components:
- Two clearly labelled policy identities: Amount baseline and Logistic regression.
- Paired comparisons for fraud-labelled transactions selected, legitimate reviews, queue precision, cohort recall and fraud-labelled value selected.
- A daily comparison trend to show whether the aggregate result is consistent across the selected dates.
- A compact definition or methodology note explaining the capacity and denominator.

For the restricted cohort, use the restricted rank columns. Do not apply the full-population rank columns after filtering the data to amounts at or below 220. The cohort-specific ranks are independently calculated.

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

Use one coherent outline-icon family, consistent stroke weight and a restrained size. Icons support labels; they never replace them. Do not use a bank logo or imply affiliation with a real bank. A simple text wordmark or small neutral mark may be explored later, but branding is not yet approved.

## 7. Interaction contract proposal

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
| D1 — Design tokens | Palette, typography, spacing, icon and component rules | Proposed; owner review required |
| D2 — Page wireframes | Exact layout and visual selection for both pages | Proposal v0.1 documented; owner approval pending |
| D3 — Theme implementation | Theme JSON imported and inspected in Power BI Desktop | Not started |
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


## 12. Research synthesis and wireframe proposal

The detailed non-binding layout proposal is recorded in [P5 Wireframe Proposal v0.1](P5_WIREFRAMES_PROPOSAL_v0.1.md). It includes the two page layouts, proposed hierarchy, icon roles, number treatment, native Power BI interactions, accessibility checks and a proposed aggregate overview table.

The external review compared corporate banking dashboard patterns on Dribbble with overview/detail navigation and period controls found in LinkedIn and TikTok analytics interfaces. The useful pattern is a stable page frame, concise KPI summary, readable trend and supporting detail. Social audience metrics, personal wallet components, decorative gauges and unsupported data dimensions are deliberately excluded.

Microsoft's current Power BI documentation confirms support for custom report themes, date and button slicers, 16:9 1280 x 720 canvas settings, grid alignment and accessibility features. These are implementation constraints, not permission to build the proposed design.

**Current gate:** The wireframes and detailed tokens are proposals. The owner must approve or revise them before theme or report implementation. P5 remains at 0%.
