import unittest

import pandas as pd

from src.transaction_features import MODEL_FEATURES, build_features, split_features


def transactions_at(events):
    frame = pd.DataFrame(events, columns=["TX_DATETIME", "CUSTOMER_ID", "TERMINAL_ID", "TX_AMOUNT"])
    frame["TX_DATETIME"] = pd.to_datetime(frame["TX_DATETIME"], format="ISO8601")
    frame["TRANSACTION_ID"] = range(len(frame))
    frame["TX_FRAUD"] = 0
    frame["TX_FRAUD_SCENARIO"] = 0
    return frame


class TransactionFeatureTests(unittest.TestCase):
    def setUp(self):
        self.transactions = transactions_at([
            ("2018-04-01 10:00:00", 1, 10, 10.0),
            ("2018-04-07 10:00:00", 1, 20, 20.0),
            ("2018-04-08 09:00:00", 2, 10, 90.0),
            ("2018-04-08 10:00:00", 1, 10, 500.0),
            ("2018-04-08 10:00:00", 1, 10, 600.0),
            ("2018-04-08 10:00:01", 1, 10, 30.0),
            ("2018-04-20 10:00:01", 1, 10, 40.0),
        ])

    def test_features_match_explicit_history_filters(self):
        actual = build_features(self.transactions)
        for index, event in self.transactions.iterrows():
            past = self.transactions.loc[self.transactions["TX_DATETIME"] < event.TX_DATETIME]
            row = actual.loc[index]
            for entity, key in (("customer", "CUSTOMER_ID"), ("terminal", "TERMINAL_ID")):
                history = past.loc[past[key] == event[key]]
                for days, window in ((1, "24h"), (7, "7d")):
                    recent = history.loc[history["TX_DATETIME"] >= event.TX_DATETIME - pd.Timedelta(days=days)]
                    self.assertEqual(row[f"{entity}_tx_count_{window}"], len(recent))
                if entity == "customer":
                    if recent.empty:
                        self.assertTrue(pd.isna(row.customer_mean_amount_7d))
                    else:
                        self.assertAlmostEqual(row.customer_mean_amount_7d, recent["TX_AMOUNT"].mean())
                    if history.empty:
                        self.assertTrue(pd.isna(row.customer_seconds_since_previous))
                    else:
                        previous = history["TX_DATETIME"].max()
                        self.assertEqual(row.customer_seconds_since_previous, (event.TX_DATETIME - previous).total_seconds())

    def test_equal_time_and_future_rows_cannot_change_prior_features(self):
        before = build_features(self.transactions.iloc[:4])
        after = build_features(self.transactions)
        pd.testing.assert_frame_equal(before, after.iloc[:len(before)])

    def test_fraud_fields_cannot_change_model_features(self):
        original = build_features(self.transactions)
        changed = build_features(self.transactions.assign(TX_FRAUD=1, TX_FRAUD_SCENARIO=3))
        pd.testing.assert_frame_equal(original[list(MODEL_FEATURES)], changed[list(MODEL_FEATURES)])

    def test_partitions_use_exact_boundaries_and_keep_prior_history(self):
        transactions = transactions_at([
            ("2018-07-31 23:59:59", 1, 10, 10.0),
            ("2018-08-01 00:00:00", 1, 10, 20.0),
            ("2018-08-31 23:59:59", 1, 10, 30.0),
            ("2018-09-01 00:00:00", 1, 10, 40.0),
            ("2018-09-30 23:59:59", 1, 10, 50.0),
        ])
        features = build_features(transactions)
        parts = split_features(features)
        self.assertEqual([part["TRANSACTION_ID"].tolist() for part in parts.values()], [[0], [1, 2], [3, 4]])
        self.assertEqual(parts["validation"].iloc[0]["customer_seconds_since_previous"], 1)
        self.assertEqual(parts["test"].iloc[0]["customer_seconds_since_previous"], 1)

        outside = features.copy()
        outside.loc[4, "TX_DATETIME"] = pd.Timestamp("2018-10-01")
        with self.assertRaisesRegex(ValueError, "outside April"):
            split_features(outside)
        with self.assertRaisesRegex(ValueError, "each require transactions"):
            split_features(features.iloc[:3])
