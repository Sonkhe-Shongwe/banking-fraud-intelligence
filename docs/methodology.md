# Planned methodology — Banking Fraud Intelligence

**Stage:** Research design only. No empirical measurements or working app are asserted.

## Decision problem
Prioritise transactions for an analyst review queue given a fixed investigation budget. Explore the trade-offs between fraud captured, false investigations and exposure represented by flagged transactions.

## Unit of analysis
**One transaction at the time a detection decision would be made.** Confirm event timestamps, feature availability and label delay in the selected data before implementation.

## Research plan
1. **Data profiling:** fraud prevalence, amounts, missingness, duplication, timestamps and potential label leakage.
2. **Training design:** chronological train/validation/test with holdout never used for model selection. Preserve customers/terminal effects when required.
3. **Baselines:** simple score/rules and relevant classification baselines; avoid adding models without a hypothesis.
4. **Model quality:** PR-AUC, precision, recall, calibration and uncertainty where supportable. Accuracy alone is not the primary criterion.
5. **Operational decisions:** compare fixed top-N or fixed percentage review policies; report false positives, discovered fraud counts and *fraud-labelled transaction amounts under review*. Any financial-loss model must clearly state its assumptions.
6. **App layer:** offline-trained artefacts feed a lightweight Streamlit dashboard showing risk distributions, investigator queues and review-capacity scenarios; no exposed personal banking records.
7. **Checks:** leakage tests, temporal splits, deterministic reproduction, metric reconciliation and limitations.

## Non-claims
A simulated improvement is not a bank-tested fraud-prevention system. Flagged amount is neither recovered nor prevented loss; synthetic dataset evaluation cannot demonstrate real-world effectiveness.

**Final output:** reproducible analytical pipeline, validation report and Streamlit demonstration.
