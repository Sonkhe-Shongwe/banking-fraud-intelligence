# Local data and notebook workflow

The leading source for local feasibility work is the Fraud Detection Handbook's [raw-data revision `6e67dbd`](https://github.com/Fraud-Detection-Handbook/simulated-data-raw/tree/6e67dbd0a3bfe0d7ec33abc4bce5f37cd4ff0d6a). It provides 183 daily pickle files in its `data/` directory. Use the pinned revision and check the manifest against the [recorded audit](../docs/data_sources.md#source-and-audit-evidence).

## Prepare one CSV

If `data/processed/transactions.csv` already exists and passed validation, use that copy for the notebooks. If you already have the combined `transactions.csv.zip`, extract its `transactions.csv` into `data/processed/`.

Pull the repository and double-click **Prepare Transactions.cmd** at the repo root. The first run needs an internet connection and Python 3.12 or a compatible Python 3.9–3.13 installation available on PATH. The launcher sets up pandas in the repo's `.venv`, downloads the pinned ZIP into `data/raw/`, and opens `data/processed/` when the CSV is ready.

The converter checks all 183 daily pickle files against the audited manifest before loading them. It writes one `data/processed/transactions.csv` containing 1,754,155 transactions, all nine source columns, and 14,681 fraud labels. If the pinned ZIP is already cached, the converter uses that copy. Raw and processed data are excluded from Git.

To use your own copy of the pinned ZIP, run the following in an environment with `requirements-conversion.txt` installed:

```powershell
python src/convert_transactions.py --archive "path\to\source.zip"
```

The full CSV exceeds Excel's worksheet row limit. Use pandas to inspect all rows. The [held-out notebook](#run-the-held-out-evaluation) generates the separate September rank export for Power BI.

The source's reuse status and the boundary for publishing derived artefacts are recorded in the [feasibility audit](../docs/data_sources.md#publication-scope).

## Run the exploratory notebook

Use the Python 3.12 kernel that already runs the project notebooks. For a fresh setup, generate the local CSV first. From the repository root, install the notebook dependencies in the virtual environment created by the Windows launcher.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-notebook.txt
```

Open [01_fraud_investigation_eda.ipynb](../notebooks/01_fraud_investigation_eda.ipynb) in VS Code with its Jupyter extension. Use your working Python 3.12 kernel or the `.venv` kernel from the fresh setup. Choose **Run All**. The notebook finds the CSV relative to the checkout and generates the tables and figures locally. [Keep a saved run without blocking pulls](#save-notebook-runs-locally).

## Validate the CSV for the pipeline

From the repository root, run this with the same Python environment you used for the notebook, or one with `requirements-conversion.txt` installed.

```powershell
python src/validate_transactions.py
```

Use `--input "path\to\transactions.csv"` to validate a different copy. The default is `data/processed/transactions.csv`. The report shows rows read, ready and dropped, date coverage, fraud labels and retained zero amounts. The verified CSV passed with 1,754,155 rows ready, zero rows dropped and 42 zero-amount rows retained.

The validator parses timestamps and numeric types, checks the schema, missing fields, ID integrity, amount validity, chronological order, elapsed-time fields and fraud label consistency. It exits with an error on invalid input and leaves the source file intact. The converter and source audit establish provenance and expected snapshot totals. [Source audit](../docs/data_sources.md#source-and-audit-evidence)

## Run the feature engineering notebook

Open [02_fraud_feature_engineering.ipynb](../notebooks/02_fraud_feature_engineering.ipynb) in VS Code, select the same Python 3.12 kernel that ran the exploratory notebook, and choose **Run All**. It validates the local CSV, builds the history features in memory, and displays a synthetic example, a missing-history summary and a chronological split table. [Feature definitions and split rules](../docs/data_model.md#scoring-time-features-and-partitions)

## Run the modelling notebook

Open [03_fraud_model_validation.ipynb](../notebooks/03_fraud_model_validation.ipynb) with the Python 3.12 kernel that ran the first two notebooks. If this kernel still needs scikit-learn 1.8.0, run the following in a temporary notebook cell and restart the kernel after installation.

```python
%pip install scikit-learn==1.8.0
```

Choose **Run All** to rebuild the feature inputs, fit the model and display the August tables and chart. A fresh environment can use `requirements-notebook.txt` for all dependencies. [Frozen protocol](../docs/methodology.md#frozen-model-and-review-protocol)

## Run the held-out evaluation

Open [04_fraud_holdout_evaluation.ipynb](../notebooks/04_fraud_holdout_evaluation.ipynb) with the same Python 3.12 kernel as the modelling notebook and choose **Run All**. It rebuilds the April–July fit, compares the September queues, and reconciles the aggregate metrics to the rows selected by each rank. It writes `data/processed/september_review_ranks.csv` after those checks pass. The export is local and ignored by Git. [Rank fields and grain](../docs/data_model.md#september-review-rank-export)

## Prepare the Power BI reporting data

Run this after Notebook 04 has generated the local september_review_ranks.csv export.

1. Pull the latest repository changes.
2. Open 05_power_bi_data_preparation.ipynb in VS Code.
3. Select the same Python 3.12 kernel used for the earlier notebooks.
4. Choose **Run All**.
5. Review the input audit, monthly summary, weekly trend, simulator-boundary chart and eight-row P4 reconciliation.
6. Confirm the output inventory and manifest at the end of the notebook.

The notebook writes these local files to data/processed/powerbi/:

- Overview_Daily.csv
- DimDate.csv
- September_Ranks.csv
- September_Scenario_Lift.csv
- September_Queue_Reconciliation_QA.csv (QA only; do not load into Power BI)
- PowerBI_Data_Manifest.json

The output folder is Git-ignored. Do not commit the generated CSVs or manifest. If the P4 rank export is missing, run 04_fraud_holdout_evaluation.ipynb first. See the Power BI setup guide at powerbi/README.md for the table contract and relationship plan.

## Save notebook runs locally

The files under `notebooks/` are tracked source files. Running a notebook can add outputs and execution counts. Saving those changes can block a pull when the same notebook has an incoming update. A white dot on a VS Code tab indicates unsaved editor changes. Git's `M` marks changes already saved to disk.

To keep tables and charts, pull first and copy the notebook you want to run to `data/processed/notebook-runs/`. For example, run these PowerShell commands from the repo root to copy P4. The timestamp gives each run its own file.

```powershell
$runDir = '.\data\processed\notebook-runs'
New-Item -ItemType Directory -Path $runDir -Force | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
Copy-Item -LiteralPath '.\notebooks\04_fraud_holdout_evaluation.ipynb' `
  -Destination (Join-Path $runDir "04_fraud_holdout_evaluation-$stamp.ipynb")
```

To preserve the P5 reporting charts and audit tables, use the same copy command with the Notebook 05 filename:

```powershell
Copy-Item -LiteralPath '.\notebooks\05_power_bi_data_preparation.ipynb' `
  -Destination (Join-Path $runDir "05_power_bi_data_preparation-$stamp.ipynb")
```

Open the copy in VS Code, select your working Python 3.12 kernel, then run and save it there. All five notebooks can locate the repo from that folder. For links to project docs embedded in notebook text, use the original notebook under `notebooks/`. For a new run after another pull, make a fresh copy from the updated source. If you only need the CSV from P4, you can run the tracked notebook and close it without saving the notebook outputs.

### Recover a pull blocked by a notebook

1. Close the affected tab in VS Code before pulling. If it has unsaved edits or outputs you want to keep, save them first so Git can preserve them. For unsaved outputs you do not need, choose **Don't Save**.
2. If Git still reports the notebook as modified and blocks the pull, stash only the named file. For P4, run the following from the repo root.

   ```powershell
   git stash push -m "Local P4 notebook run" -- notebooks/04_fraud_holdout_evaluation.ipynb
   ```

3. Click **Pull origin** and reopen the updated source from Explorer. Leave the old run in the stash to keep the updated notebook clean. Your local rank CSV is outside the stash. If other notebooks are marked `M`, they can stay in place until a pull touches those same files.
