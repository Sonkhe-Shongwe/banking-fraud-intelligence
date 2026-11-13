# Data acquisition

The leading source for local feasibility work is the Fraud Detection Handbook's [raw-data revision `6e67dbd`](https://github.com/Fraud-Detection-Handbook/simulated-data-raw/tree/6e67dbd0a3bfe0d7ec33abc4bce5f37cd4ff0d6a). It provides 183 daily pickle files in its `data/` directory. Use the pinned revision and check the manifest against the [recorded audit](../docs/data_sources.md#source-and-audit-evidence).

## Prepare one CSV

Pull the repository and double-click **Prepare Transactions.cmd** at the repo root. The first run needs an internet connection and Python 3.12 or a compatible Python 3.9–3.13 installation available on PATH. The launcher sets up pandas in the repo's `.venv`, downloads the pinned ZIP into `data/raw/`, and opens `data/processed/` when the CSV is ready.

The converter checks all 183 daily pickle files against the audited manifest before loading them. It writes one `data/processed/transactions.csv` containing 1,754,155 transactions, all nine source columns, and 14,681 fraud labels. If the pinned ZIP is already cached, the converter uses that copy. Raw and processed data are excluded from Git.

To use your own copy of the pinned ZIP, run the following in an environment with `requirements-conversion.txt` installed:

```powershell
python src/convert_transactions.py --archive "path\to\source.zip"
```

The full CSV exceeds Excel's worksheet row limit. Use pandas to inspect all rows. This is the combined source table. The Power BI reporting export comes from the later analysis and evaluation phases.

The source's reuse status and the boundary for publishing derived artefacts are recorded in the [feasibility audit](../docs/data_sources.md#publication-scope).

## Run the exploratory notebook

Generate the local CSV first. Use Python 3.12 for the notebook environment. From the repository root, install the notebook dependencies in the virtual environment created by the Windows launcher.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-notebook.txt
```

Open [01_fraud_investigation_eda.ipynb](../notebooks/01_fraud_investigation_eda.ipynb) in VS Code with its Jupyter extension, select the `.venv` Python kernel and choose **Run All**. The notebook finds the CSV relative to the checkout and generates the tables and figures locally. The committed notebook has empty outputs while publication scope is open.
