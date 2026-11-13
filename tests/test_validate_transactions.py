import csv
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pandas as pd

from src.convert_transactions import COLUMNS
from src.validate_transactions import load_transactions


class TransactionValidationTests(unittest.TestCase):
    def setUp(self):
        directory = self.enterContext(TemporaryDirectory())
        self.path = Path(directory) / "transactions.csv"
        self.rows = [
            [0, "2018-04-01 00:00:05", 3, 7, 0, 5, 0, 0, 0],
            [1, "2018-04-01 00:00:05", 3, 7, 225.5, 5, 0, 1, 1],
        ]

    def write_csv(self, header=COLUMNS):
        with self.path.open("w", newline="", encoding="utf-8") as output:
            writer = csv.writer(output)
            writer.writerow(header)
            writer.writerows(self.rows)

    def test_preserves_zero_amount_and_equal_timestamps(self):
        self.write_csv()
        before = self.path.read_bytes()
        transactions = load_transactions(self.path)
        self.assertEqual(transactions.TRANSACTION_ID.tolist(), [0, 1])
        self.assertEqual(transactions.TX_AMOUNT.tolist(), [0.0, 225.5])
        self.assertEqual(transactions.TX_DATETIME.tolist(), [pd.Timestamp("2018-04-01 00:00:05")] * 2)
        self.assertEqual(self.path.read_bytes(), before)

    def test_invalid_values_fail_with_a_diagnostic(self):
        cases = (
            (0, 0, "duplicate TRANSACTION_ID"),
            (1, "2018-02-30 00:00:05", "Invalid TX_DATETIME"),
            (1, "2018-04-01 00:00:01", "out of chronological order"),
            (2, "", "Missing values by column: CUSTOMER_ID"),
            (3, -1, "negative identifier"),
            (4, -1, "negative or non-finite TX_AMOUNT"),
            (4, "inf", "negative or non-finite TX_AMOUNT"),
            (5, 6, "TX_TIME_SECONDS mismatches"),
            (6, 1, "TX_TIME_DAYS mismatches"),
            (7, 2, "invalid TX_FRAUD values"),
            (8, 4, "invalid TX_FRAUD_SCENARIO"),
            (8, 0, "fraud label and scenario disagreements"),
        )
        original_row = self.rows[1].copy()
        for index, value, diagnostic in cases:
            with self.subTest(index=index, value=value):
                self.rows[1] = original_row.copy()
                self.rows[1][index] = value
                self.write_csv()
                with self.assertRaisesRegex(ValueError, diagnostic):
                    load_transactions(self.path)

    def test_rejects_missing_column(self):
        self.write_csv(COLUMNS[:-1])
        with self.assertRaisesRegex(ValueError, "Expected the nine source columns"):
            load_transactions(self.path)

    def test_rejects_extra_fields_in_rows(self):
        for row in self.rows:
            row.append("extra")
        self.write_csv()
        with self.assertRaisesRegex(ValueError, "more fields than the header"):
            load_transactions(self.path)
