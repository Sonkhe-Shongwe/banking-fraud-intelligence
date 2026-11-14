# Fraud Triage design proposal

**Recorded 14 November 2026.** This is the current design preview for the existing Review Policy Comparison page. The owner requested the changes below during review. The consolidated design still awaits approval for Power BI implementation and validation in Desktop. The [approved light design](POWER_BI_DESIGN_SYSTEM.md) is the current implementation baseline.

## Page design

| Component | Current preview |
|---|---|
| Brand | **Banking Fraud Intelligence**, with a standalone mint symbol on its left. Three transaction lines converge on a diamond representing an item selected for review. The transparent mark was checked at 36 px against the dark header. |
| Title | **Fraud Triage** with the subtitle “Prioritising transactions under a fixed daily review limit.” |
| Controls | Place the eligible cohort, 50/100 reviews per day and September 2018 date slicers directly below the title and above the result cards. Keep labels visible alongside icons. Default to all transactions, 50/day and the full month. |
| Results | Lead with the signed model-minus-baseline difference. Show the comparison at the same daily capacity and put the amount-baseline and logistic-regression counts beside it. Use neutral treatment for a tie and baseline blue when the baseline is ahead. |
| Daily chart | Use a diverging column chart for daily model-minus-baseline selections with a visible zero line. Show the daily counts for both policies and the difference in the tooltip. |
| Capacity reference | Keep the four full-September comparisons visible beside the chart. The values stay fixed as slicers change. Highlight the selected cohort and capacity for orientation. |
| Scorecard | **Review trade-offs** presents both policy rows with selected reviews, fraud-labelled selections, legitimate reviews, precision, recall and fraud-labelled value. Keep both rows visible without scrolling at the target canvas size. |
| Methodology | Remove the standalone “Simulated data” badge and the bottom label from the comparison page. Use the scorecard's accessible information control for metric definitions, simulated-data provenance and retrospective use of fraud labels. Add the simulation provenance and the absence of confirmation timestamps to that information control during implementation. [Source audit](data_sources.md#evaluation-implications) · [Metric definitions](findings.md#metric-interpretation) |

The [transparent logo asset](../assets/fraud-triage-preview-mark.png) is the exact mark used in the preview.

## Visual treatment

- Use deep navy `#0C1422` for the canvas, `#131E30` for panels, `#2B3B51` for dividers, `#F0F5FA` for primary text and `#AABACD` for secondary text.
- Use mint `#62DDBD` for logistic regression and soft blue `#9EB8E4` for the amount baseline. Pair colour with the signed values, policy labels and chart position. The preview's primary text and accent pairings passed a calculated contrast check. Desktop contrast and rendering remain open.
- The preview uses Bricolage Grotesque for headings and labels and IBM Plex Mono for key figures and table values. Confirm font availability and rendering in Desktop before adopting the pair. Agree on a supported fallback if necessary.
- Align the title, slicers, cards, chart and scorecard on common edges. Give the daily chart more width than the capacity reference. Carry the approved 1280 × 720 canvas into the Desktop fit check.

## Evidence and implementation handoff

The preview uses the verified September aggregates. Its default values are 589 baseline and 592 model, a difference of +3 at 50 reviews/day. At 100/day, the figures are 622 and 632, a difference of +10. The restricted cohort returns +3 and +9. The preview's data reconciliation and filter logic were checked outside Desktop. See the [findings](findings.md#fraud-labelled-transactions-selected-across-september) and [Desktop evidence](SESSION_HANDOFF_CURRENT.md#current-power-bi-repository-state).

For the portfolio, frame the page as a comparison of review policies under constrained capacity. Present September as a held-out result and retain the [August validation context](findings.md#august-validation-context) when discussing model performance.

Once the owner approves the consolidated design for Desktop, map it onto the existing comparison page and its verified measures. Check the logo and type rendering, the default and 100/day results, both restricted scenarios, a single-day date slice, the fixed reference values, keyboard access to controls and definitions, and the visibility of both scorecard rows. Record the results in the [handoff](SESSION_HANDOFF_CURRENT.md). Fraud Overview remains the second page in the [approved scope](POWER_BI_DESIGN_SYSTEM.md#approved-page-scope). [Publication scope](data_sources.md#publication-scope) stays separate.
