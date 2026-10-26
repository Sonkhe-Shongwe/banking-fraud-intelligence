# Analytical model — proposed, not implemented

## Primary grain
Transaction-level record: one candidate decision at a known transaction time. Exact keys, event times and admissible features must be established from the selected dataset.

## Proposed layers
1. **Raw/landing data:** immutable source files outside Git unless legally and technically appropriate.
2. **SQL preparation:** validated transactions, quality flags, permitted prediction-time columns.
3. **Python modelling tables:** chronological training/validation/test partitions; engineered features computed without future information.
4. **Evaluation outputs:** transaction ID, held-out fraud label, predicted risk score, transaction amount, observation time and review-policy rank.
5. **Streamlit application:** precomputed/evaluated outputs for lightweight investigation-capacity simulations and explanatory charts.

## Mandatory checks
One row per scored transaction; no duplicate joins; consistent event ordering; no future label/chargeback columns used as predictors; reconciliation of queue counts and monetary exposure.

**A relational/star schema is not required unless the actual data and analysis justify it.**
