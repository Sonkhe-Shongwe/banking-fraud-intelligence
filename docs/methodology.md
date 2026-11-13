# Banking Fraud Intelligence methodology

The decision is which transactions an investigator should review when daily review capacity is limited. The unit of analysis is one transaction at its scoring time. The source has been [profiled](data_sources.md). The [modelling notebook](../notebooks/03_fraud_model_validation.ipynb) reproduces August validation, and the [held-out evaluation notebook](../notebooks/04_fraud_holdout_evaluation.ipynb) reproduces September results.

1. **Prepare in Python.** Validate transaction keys, timestamps and amounts. Build features from information available at scoring time. Define how equal timestamps and any simulated label delay affect the available history.
2. **Partition chronologically.** Use earlier data for training, later data for validation and the latest held-out period for final evaluation. Use validation for model selection and freeze the protocol before scoring the holdout.
3. **Establish the baseline.** Rank by transaction amount within each day and compare at least one scikit-learn model. Use a consistent tie-break and record it before evaluation.
4. **Evaluate at the same daily review capacity.** Rank each day's eligible transactions under both policies and compare the same top-N limit. Report fraud caught, legitimate transactions reviewed and the sum of amounts on reviewed fraud-labelled transactions. Use queue precision, recall and average precision to support interpretation.
5. **Check the simulator effect.** Report a sensitivity comparison on transactions with amounts at or below 220. Document whether any lift persists when the deterministic high-amount group is excluded. Use the scenario field for retrospective breakdowns.
6. **Define the report from the evidence.** Use verified Python outputs to identify which questions, metrics and interactions the report can support. Present the proposed scope for owner approval before building. Reconcile each approved Power BI measure to Python for representative capacities and date selections.

Report the captured amount as fraud-labelled transaction value. Estimates of savings, prevented losses or production performance require separate evidence.

## Frozen model and review protocol

The amount baseline remains the reference policy. The first logistic regression model is frozen as the challenger for the September comparison. August was used to assess this fixed configuration. The [model module](../src/fraud_model.py) defines the following settings.

| Decision | Frozen setting |
|---|---|
| Fit period | 1 April through 31 July 2018. Use historical transaction events and retrospective training outcomes from this period. Confirmation times are unavailable. |
| Validation and final evaluation | August 2018 for validation and September 2018 for final evaluation. Reproduce the fit from the same April–July data and settings. September was examined in aggregate in P1, and its model scores and queue results are reserved for P4. |
| Predictors and preprocessing | The seven P2 predictors. Fit median imputation with missing indicators and standardisation on training rows only. The features use strictly earlier events plus the current amount. |
| Estimator and rank score | scikit-learn 1.8.0 logistic regression with `lbfgs`, balanced class weights, `C=1.0` and `max_iter=1000`. Use its decision score for ranking. |
| Daily selection | Rank eligible rows separately each day by amount or decision score, descending. Break ties by ascending transaction ID. Take up to 50 and up to 100 per day. |
| Sensitivity | In addition to the full cohort, filter to amounts at or below 220 and rank again inside each day. Reuse the same fitted model. |
| Metrics | Sum reviews, fraud caught, legitimate reviews and fraud-labelled value across days. Calculate pooled queue precision and cohort recall. Report average precision over all eligible transactions as a supplementary ranking metric. |

## Evidence for the dashboard

The business question guides exploration. For each candidate view, record the question it answers, the data fields and time period it requires, the metric definition and denominator, and the Python output that verifies it. Check what the intended audience can access before including transaction detail.

| Candidate question | Evidence required | What it could support |
|---|---|---|
| How do the two policies perform at the same review capacity? | Held-out fraud labels and daily ranks for both policies on the same transactions, reconciled at representative review limits. | A capacity control with a policy comparison. Report the measured difference even if lift is small, zero or negative. |
| Which transactions enter the queue for a given day and capacity? | Unique transaction IDs, event times and verified ranks. Transaction-level rows must be available for the intended audience. | A dated review queue and transaction drillthrough when the detail is available. |
| How quickly are alerts confirmed or resolved? | Alert, confirmation or resolution timestamps from an appropriate source. The current snapshot has none of these. | Reconsider this question only if those events become available. |

The September evaluation verifies the capacity comparisons in both eligible cohorts and reconciles the local transaction ranks. The source is simulated and lacks alert and resolution timestamps. A public report can show approved evidence and must label any illustrative data separately from measured results. [Source audit](data_sources.md) · [Findings](findings.md)
