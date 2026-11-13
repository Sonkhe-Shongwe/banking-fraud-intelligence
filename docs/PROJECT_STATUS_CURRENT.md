# Current project status

**Checkpoint:** 13 November 2026

**Overall progress:** 12% · **Active phase:** P1 at 80%

**Next decision:** Confirm the scope of public dataset-derived artefacts. [Current handoff](SESSION_HANDOFF_CURRENT.md)

| Phase | Weight | Complete | Points earned | Evidence required to close |
|---|---:|---:|---:|---|
| **P1 · Scope and dataset feasibility** | 15% | **80%** | **12** | Pin and profile the source, document leakage and label timing, record scope and audit in Git, and agree on publication scope. |
| **P2 · Python data pipeline** | 20% | 0% | 0 | Repeatable load and validation, scoring-time feature preparation, chronological train/validation/test partitions, and checks for future information. |
| **P3 · Baseline and model** | 20% | 0% | 0 | Amount-based baseline and at least one scikit-learn model, compared on validation data. Record and freeze the model and evaluation protocol before scoring the holdout. |
| **P4 · Investigation policy and held-out results** | 20% | 0% | 0 | Compare model and baseline at the same daily review limits. Report fraud caught, legitimate reviews and fraud-labelled transaction value. Check results on amounts at or below 220. |
| **P5 · Power BI Investigation Dashboard** | 15% | 0% | 0 | Owner-approved design and a report verified in Power BI Desktop. Changing daily review capacity updates the investigation queue and both policies' metrics from precomputed ranks. Transaction drillthrough and totals are checked against the Python export. |
| **P6 · Portfolio release** | 10% | 0% | 0 | Verify from a fresh checkout and publish the approved README, reproduction instructions, results, limitations and walkthrough. |
| **Overall** | **100%** | **12%** | **12** | |

Phase percentages track accepted evidence. Overall progress is the sum of each phase weight multiplied by its completion fraction. The current score is `15 × 0.80 = 12` points.

## P1 checks

Each check is worth 20% of P1.

| Check | Status | Evidence |
|---|---|---|
| Pin the source revision | Verified | [Raw dataset revision and manifest](data_sources.md#source-and-audit-evidence) |
| Profile all raw files | Verified | [183 batches and 1,754,155 transactions](data_sources.md#source-and-audit-evidence) |
| Identify leakage and label-timing risks | Verified | [Simulator limits and evaluation implications](data_sources.md#evaluation-implications) |
| Record revised scope and audit in GitHub | Verified | [Python scope](../README.md#intended-deliverable) · [Audit](data_sources.md) |
| Resolve which derived artefacts can be published | Open | [Publication scope](data_sources.md#publication-scope) |

Update this scorecard and the handoff together when evidence changes. P4 is complete when its evaluation is reproducible and reported, even if the model shows little or no lift.
