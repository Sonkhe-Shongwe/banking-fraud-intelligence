# Banking Fraud Intelligence methodology

The decision is which transactions an investigator should review when daily review capacity is limited. The unit of analysis is one transaction at its scoring time. The source has been [profiled](data_sources.md). Model results are pending.

1. **Prepare in Python.** Validate transaction keys, timestamps and amounts. Build features from information available at scoring time. Define how equal timestamps and any simulated label delay affect the available history.
2. **Partition chronologically.** Use earlier data for training, later data for validation and the latest held-out period for final evaluation. Use validation for model selection and freeze the protocol before scoring the holdout.
3. **Establish the baseline.** Rank by transaction amount within each day and compare at least one scikit-learn model. Use a consistent tie-break and record it before evaluation.
4. **Evaluate at the same daily review capacity.** Rank each day's eligible transactions under both policies and compare the same top-N limit. Report fraud caught, legitimate transactions reviewed and the sum of amounts on reviewed fraud-labelled transactions. Use precision, recall and PR-AUC to support interpretation.
5. **Check the simulator effect.** Report a sensitivity comparison on transactions with amounts at or below 220. Document whether any lift persists when the deterministic high-amount group is excluded. Use the scenario field for retrospective breakdowns.
6. **Demonstrate the investigation workflow.** After design approval, use precomputed scores in Streamlit. The reviewer can change capacity, inspect the resulting queue and open individual transaction detail.

Report the captured amount as fraud-labelled transaction value. Estimates of savings, prevented losses or production performance require separate evidence.
