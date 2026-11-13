"""Verify the pinned Handbook archive and combine its daily tables into one CSV."""

import argparse
import hashlib
import os
from pathlib import Path, PurePosixPath
import shutil
import tempfile
from urllib.request import urlopen
from zipfile import BadZipFile, ZipFile

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REVISION = "6e67dbd0a3bfe0d7ec33abc4bce5f37cd4ff0d6a"
SOURCE = f"https://codeload.github.com/Fraud-Detection-Handbook/simulated-data-raw/zip/{REVISION}"
ARCHIVE = ROOT / "data" / "raw" / f"simulated-data-raw-{REVISION}.zip"
OUTPUT = ROOT / "data" / "processed" / "transactions.csv"
MANIFEST = "0b324e9e800a8fc69b388d5f646c2afa71ee87de973ea2fe839b36d2acc2120d"
COLUMNS = (
    "TRANSACTION_ID", "TX_DATETIME", "CUSTOMER_ID", "TERMINAL_ID", "TX_AMOUNT",
    "TX_TIME_SECONDS", "TX_TIME_DAYS", "TX_FRAUD", "TX_FRAUD_SCENARIO",
)


def verified_batches(archive):
    batches = sorted(
        (entry for entry in archive.infolist()
         if not entry.is_dir() and PurePosixPath(entry.filename).parent.name == "data"
         and entry.filename.endswith(".pkl")),
        key=lambda entry: PurePosixPath(entry.filename).name,
    )
    if len(batches) != 183:
        raise ValueError(f"Expected 183 daily pickle files, found {len(batches)}.")
    manifest = hashlib.sha256()
    for entry in batches:
        digest = hashlib.sha256(archive.read(entry)).hexdigest()
        manifest.update(f"{digest}  {PurePosixPath(entry.filename).name}\n".encode("utf-8"))
    if manifest.hexdigest() != MANIFEST:
        raise ValueError("The archive contents do not match the audited source revision.")
    return batches


def download_archive(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    print("Downloading the pinned dataset from GitHub...", flush=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, suffix=".part", delete=False) as temp:
        partial = Path(temp.name)
    try:
        with urlopen(SOURCE, timeout=60) as response, partial.open("wb") as target:
            shutil.copyfileobj(response, target)
        with ZipFile(partial) as archive:
            verified_batches(archive)
        os.replace(partial, path)
    finally:
        partial.unlink(missing_ok=True)


def convert(archive_path, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive_path) as archive:
        batches = verified_batches(archive)
        print(f"Verified {len(batches)} daily files. Combining them into one CSV...", flush=True)
        with tempfile.NamedTemporaryFile(dir=output_path.parent, suffix=".part", delete=False) as temp:
            partial = Path(temp.name)
        try:
            rows = 0
            fraud_labels = 0
            with partial.open("w", encoding="utf-8", newline="") as csv:
                for index, entry in enumerate(batches):
                    with archive.open(entry) as source:
                        frame = pd.read_pickle(source)
                    if tuple(frame.columns) != COLUMNS:
                        raise ValueError(f"Unexpected columns in {entry.filename}.")
                    frame.to_csv(csv, index=False, header=index == 0)
                    rows += len(frame)
                    fraud_labels += int(frame["TX_FRAUD"].sum())
            if (rows, fraud_labels) != (1_754_155, 14_681):
                raise ValueError(f"Unexpected totals: {rows:,} transactions, {fraud_labels:,} fraud labels.")
            os.replace(partial, output_path)
        finally:
            partial.unlink(missing_ok=True)
    print(f"Saved {rows:,} transactions and {fraud_labels:,} fraud labels to {output_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, help="Use an existing copy of the pinned ZIP.")
    parser.add_argument("--output", type=Path, default=OUTPUT, help="CSV destination.")
    options = parser.parse_args()
    archive_path = options.archive or ARCHIVE
    if archive_path.resolve() == options.output.resolve():
        parser.error("The CSV destination must differ from the source archive.")
    try:
        if options.archive is None and not archive_path.is_file():
            download_archive(archive_path)
        convert(archive_path, options.output)
    except (OSError, ValueError, EOFError, BadZipFile) as error:
        parser.exit(1, f"Conversion failed: {error}\n")


if __name__ == "__main__":
    main()
