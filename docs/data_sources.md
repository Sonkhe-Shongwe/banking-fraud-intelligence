# Data source feasibility and audit

**13 November 2026 verdict:** Go for a simulated portfolio case study. Public reuse of dataset-derived artefacts remains an open P1 decision.

## Source and audit evidence

The audit used the Fraud Detection Handbook's [raw-data revision `6e67dbd`](https://github.com/Fraud-Detection-Handbook/simulated-data-raw/tree/6e67dbd0a3bfe0d7ec33abc4bce5f37cd4ff0d6a). The handbook documents how its simulator writes one pickle file per day. [Simulator chapter](https://fraud-detection-handbook.github.io/fraud-detection-handbook/Chapter_3_GettingStarted/SimulatedDataset.html)

| Check | Observed |
|---|---|
| Files and date coverage | 183 daily batches, 1 April to 30 September 2018 inclusive. Every batch matched its filename date. |
| Shape | 1,754,155 transactions, nine fields, 107,121,710 raw file bytes. |
| Fraud labels | 14,681 fraud-labelled transactions (0.837%). Every day contained fraud labels. |
| Integrity | Zero missing field values, duplicate transaction IDs or duplicate full rows. |
| Amounts | 42 zero amounts and zero negative amounts. The zero-amount rows all had a non-fraud label. |
| Amount rule | All 3,258 transactions above 220 were labelled fraud, accounting for 22.2% of all fraud labels. There were 11,423 fraud-labelled transactions at or below 220. |
| Ordering | Timestamps were nondecreasing. 231,973 rows shared a timestamp with at least one other row, so feature computation needs an explicit rule for ties. |
| Manifest SHA-256 | `0b324e9e800a8fc69b388d5f646c2afa71ee87de973ea2fe839b36d2acc2120d` |

The manifest hash is the SHA-256 of the UTF-8 manifest with one line per daily file, in ascending filename order. Each line contains the lowercase SHA-256 of the raw file, two spaces, the basename, and a newline. The audit read all batches in pandas 2.2.3 using its compatibility loader for the legacy pickle format. See [acquisition notes](../data/README.md) for the local file boundary.

## Evaluation implications

- Use `TX_FRAUD` as the outcome and `TX_FRAUD_SCENARIO` only for retrospective diagnostics. The amount rule intersects other simulator scenarios, so use the actual `TX_AMOUNT > 220` boundary for the sensitivity check.
- Treat customer and terminal IDs as history keys and transaction ID as a record key. Define how to handle equal timestamps before building historical features.
- The two elapsed-time columns match values derived from the event timestamps. The source lacks a confirmed-at timestamp for fraud outcomes. Any use of historical labels requires a stated feedback-delay assumption. [Handbook evaluation example](https://fraud-detection-handbook.github.io/fraud-detection-handbook/Chapter_3_GettingStarted/BaselineModeling.html)
- Describe results as simulated. Use a simple amount-based ranking as the primary baseline at identical daily review limits.

## Publication scope

The raw-data revision contains daily files and a short README, without a separate dataset licence. The handbook separately states GPL v3 for notebook code and CC BY-SA 4.0 for its prose and pictures. Raw-data redistribution permission was not verified. Keep source files, extracts and scored records local. Before the portfolio release, confirm which aggregate results, derived files or demo fixtures can be shared. The current repository records source links, audit methodology and summary counts. [Raw repository](https://github.com/Fraud-Detection-Handbook/simulated-data-raw) · [Handbook licence statement](https://fraud-detection-handbook.github.io/fraud-detection-handbook/README.html#license)

## Alternative sources

[IEEE-CIS Fraud Detection](https://www.kaggle.com/competitions/ieee-fraud-detection) and [PaySim](https://www.kaggle.com/datasets/ealaxi/paysim1) remain alternatives if the Handbook source cannot support the agreed release. Each would require its own access, reuse, timing and leakage review.
