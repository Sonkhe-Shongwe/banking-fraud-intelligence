# Findings

## September held-out evaluation

Run the [held-out evaluation notebook](../notebooks/04_fraud_holdout_evaluation.ipynb) on the pinned CSV to see the September tables and chart. The notebook reports fraud caught, legitimate reviews, queue precision, cohort recall, fraud-labelled transaction value and average precision for the full and restricted populations. It also checks that each selected queue can be reconstructed from the local rank export.

Interpret differences at the same daily review limit first. Use August validation to assess whether the direction holds across periods. The restricted comparison reranks amounts at or below 220 so it can assess performance after removing the simulator's deterministic high-amount group. The [source audit](data_sources.md) records the simulation and label-timing limits. Generated tables, figures and transaction-level records are local pending agreement on [publication scope](data_sources.md#publication-scope).
