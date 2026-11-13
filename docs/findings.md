# Findings

## September held-out evaluation

The [held-out evaluation notebook](../notebooks/04_fraud_holdout_evaluation.ipynb) rebuilds the April–July fit and evaluates the frozen logistic-regression challenger against the amount-based baseline across all 30 September days. The notebook reconciles the selected rows against the local rank export.

### Fraud-labelled transactions selected across September

| Cohort | Daily review limit | Amount baseline | Logistic regression | Model difference |
|---|---:|---:|---:|---:|
| All transactions | 50 | 589 | 592 | +3 |
| All transactions | 100 | 622 | 632 | +10 |
| Amounts at or below 220 | 50 | 74 | 77 | +3 |
| Amounts at or below 220 | 100 | 101 | 110 | +9 |

These are aggregate counts across the 30 September days, not single-day counts. The at-or-below-220 cohort is reranked independently within each day. The 220 boundary is specific to the simulator's deterministic high-amount rule and is a sensitivity cohort, not a proposed production rule.

### August validation context

| Cohort | Daily review limit | Amount baseline | Logistic regression | Model difference |
|---|---:|---:|---:|---:|
| All transactions | 50 | 616 | 610 | -6 |
| All transactions | 100 | 650 | 648 | -2 |
| Amounts at or below 220 | 50 | 66 | 61 | -5 |
| Amounts at or below 220 | 100 | 102 | 99 | -3 |

The direction changed between August validation and September holdout. The model selected fewer fraud-labelled transactions in August and more in September. Do not present the September result as proof that the model is universally superior. Report the measured result for the selected period and capacity, including negative or small lift.

### Metric interpretation

- **Fraud-labelled transactions selected** counts selected rows with the retrospective TX_FRAUD label.
- **Legitimate reviews** counts selected rows without that label.
- **Queue precision** is the share of selected reviews with a fraud label.
- **Cohort recall** uses all fraud-labelled transactions in the eligible cohort and selected date range as its denominator.
- **Fraud-labelled transaction value selected** is the sum of TX_AMOUNT for selected rows with a fraud label. It is not a loss, saving or prevented loss.
- **Average precision** is a supplementary ranking metric over the eligible population, not the same as precision at the selected daily capacity.

Run the [held-out evaluation notebook](../notebooks/04_fraud_holdout_evaluation.ipynb) on the pinned CSV to see the full metric tables and chart. The [methodology](methodology.md) records the frozen protocol. The [source audit](data_sources.md) records the simulation, deterministic amount rule and label-timing limits. Generated tables, figures and transaction-level records remain local pending agreement on [publication scope](data_sources.md#publication-scope).
