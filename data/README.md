# Data acquisition

The leading source for local feasibility work is the Fraud Detection Handbook's [raw-data revision `6e67dbd`](https://github.com/Fraud-Detection-Handbook/simulated-data-raw/tree/6e67dbd0a3bfe0d7ec33abc4bce5f37cd4ff0d6a). It provides 183 daily pickle files in its `data/` directory. Use the pinned revision and check the manifest against the [recorded audit](../docs/data_sources.md#source-and-audit-evidence).

Use a local `data/raw/` location for source files and `data/processed/` for generated tables. Both paths are excluded from Git. The source uses legacy pandas pickles. Only deserialize files from the verified source revision. The project loader is a P2 deliverable.

The source's reuse status and the boundary for publishing derived artefacts are recorded in the [feasibility audit](../docs/data_sources.md#publication-scope).
