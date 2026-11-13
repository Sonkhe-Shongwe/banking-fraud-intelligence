# Banking Fraud Intelligence methodology

The decision is which transactions an investigator should review when daily review capacity is limited. The unit of analysis is one transaction at its scoring time. The source has been [profiled](data_sources.md). Model results are pending.

1. **Prepare in Python.** Validate transaction keys, timestamps and amounts. Build features from information available at scoring time. Define how equal timestamps and any simulated label delay affect the available history.
2. **Partition chronologically.** Use earlier data for training, later data for validation and the latest held-out period for final evaluation. Use validation for model selection and freeze the protocol before scoring the holdout.
3. **Establish the baseline.** Rank by transaction amount within each day and compare at least one scikit-learn model. Use a consistent tie-break and record it before evaluation.
4. **Evaluate at the same daily review capacity.** Rank each day's eligible transactions under both policies and compare the same top-N limit. Report fraud caught, legitimate transactions reviewed and the sum of amounts on reviewed fraud-labelled transactions. Use precision, recall and PR-AUC to support interpretation.
5. **Check the simulator effect.** Report a sensitivity comparison on transactions with amounts at or below 220. Document whether any lift persists when the deterministic high-amount group is excluded. Use the scenario field for retrospective breakdowns.
6. **Define the report from the evidence.** Use verified Python outputs to identify which questions, metrics and interactions the report can support. Present the proposed scope for owner approval before building. Reconcile each approved Power BI measure to Python for representative capacities and date selections.

Report the captured amount as fraud-labelled transaction value. Estimates of savings, prevented losses or production performance require separate evidence.

## Evidence for the dashboard

The business question guides exploration. For each candidate view, record the question it answers, the data fields and time period it requires, the metric definition and denominator, and the Python output that verifies it. Check what the intended audience can access before including transaction detail.

| Candidate question | Evidence required | What it could support |
|---|---|---|
| How do the two policies perform at the same review capacity? | Held-out fraud labels and daily ranks for both policies on the same transactions, reconciled at representative review limits. | A capacity control with a policy comparison. Report the measured difference even if lift is small, zero or negative. |
| Which transactions enter the queue for a given day and capacity? | Unique transaction IDs, event times and verified ranks. Transaction-level rows must be available for the intended audience. | A dated review queue and transaction drillthrough when the detail is available. |
| How quickly are alerts confirmed or resolved? | Alert, confirmation or resolution timestamps from an appropriate source. The current snapshot has none of these. | Reconsider this question only if those events become available. |

The initial audit confirms simulated transaction history and fraud labels. P2–P4 must still establish which comparisons are reliable, including how much the simulator's amount rule influences the results. A public report can show approved evidence and must label any illustrative data separately from measured results. [Source audit](data_sources.md)
