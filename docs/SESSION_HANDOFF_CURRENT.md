# Current session handoff

**Updated:** 13 November 2026

**Project:** Banking Fraud Intelligence

**Start with:** [Phase scorecard](PROJECT_STATUS_CURRENT.md) · [Documentation index](DOCUMENTATION_INDEX.md)

## Verified checkpoint

| Area | Evidence |
|---|---|
| Repository baseline | The preceding planning checkpoint was [`d7d2726`](https://github.com/Sonkhe-Shongwe/banking-fraud-intelligence/commit/d7d27267768123a30c25472b5d8730a73ab1e5e8). |
| Scope | Python for data preparation, modelling and evaluation. The owner approved Power BI Desktop as the single P5 dashboard platform. |
| Data | The pinned Handbook raw snapshot was profiled across 183 daily files. It contains 1,754,155 simulated transactions and 14,681 fraud labels. [Audit](data_sources.md) |
| Key risk | The simulator labels all amounts above 220 as fraud. The raw files lack label-confirmation timestamps. [Evaluation implications](data_sources.md#evaluation-implications) |
| Delivery state | P1 is at 80%. The pipeline, model evaluation and Power BI report are pending. |

## Owner working agreement

Work in small increments with a visible checkpoint. Show what changed, why it matters, what was verified, and what the owner can open or try after pulling. The planned report lets the owner or reviewer change review capacity, compare policies and inspect transactions. The platform decision is approved. Dashboard design and other major changes require separate owner approval. The implementation start date has yet to be revised from the earlier 2027 plan.

## Resume here

1. Confirm the intended public artefacts and the applicable reuse terms. The source repository does not supply a separate raw-data licence. Keep raw files, row-level extracts and scored transaction records local while their publication rights are unresolved. [Publication scope](data_sources.md#publication-scope)
2. Bring the owner a concrete P2 first increment for approval, with inputs, outputs and acceptance checks. The first proposed increment is reproducible loading and validation of the pinned daily files.
3. Record approval and evidence in this handoff and the scorecard as each gate is closed. Dashboard design is a later approval in P5.

## Checkpoint history

| Date | Checkpoint |
|---|---|
| 26 October 2026 | Proposed data grain and model quality gates recorded in `d7d2726`. |
| 13 November 2026 | Profiled the pinned simulated source, recorded the Python-only scope, and added the documentation index, phase scorecard and session handoff. |
| 13 November 2026 | Owner approved Power BI Desktop for P5. Recorded the change and the Python-to-report handoff. |
