import unittest

import numpy as np
import pandas as pd

from src.fraud_model import compare_review_queues, fit_ranker, score_transactions
from src.review_export import build_rank_export
from src.transaction_features import MODEL_FEATURES


class FraudModelTests(unittest.TestCase):
    def test_ranker_preprocessing_uses_training_data(self):
        training = pd.DataFrame({feature: [1.0, 3.0, 8.0, 12.0] for feature in MODEL_FEATURES})
        training.loc[1, "customer_mean_amount_7d"] = np.nan
        training["TX_FRAUD"] = [0, 0, 1, 1]
        training["TRANSACTION_ID"] = [0, 1, 2, 3]
        training["TX_DATETIME"] = pd.Timestamp("2018-04-01")

        model = fit_ranker(training)
        validation = training.iloc[:2].assign(TX_AMOUNT=[1000.0, 1.0])
        scores = score_transactions(model, validation)
        self.assertEqual(model.named_steps["impute"].statistics_[0], 5.5)
        self.assertEqual(model.named_steps["impute"].statistics_[5], 8.0)
        self.assertTrue(np.isfinite(scores["model_score"]).all())
        pd.testing.assert_frame_equal(scores, score_transactions(model, validation.assign(TX_FRAUD=1)).assign(
            TX_FRAUD=validation["TX_FRAUD"],
        ))

    def test_daily_ranking_breaks_ties_by_id_and_reranks_filtered_cohort(self):
        scored = pd.DataFrame({
            "TRANSACTION_ID": range(105),
            "TX_DATETIME": [pd.Timestamp("2018-08-01")] * 103 + [pd.Timestamp("2018-08-02")] * 2,
            "TX_AMOUNT": [300.0] + [10.0] * 104,
            "TX_FRAUD": [1] + [0] * 49 + [1] + [0] * 54,
            "model_score": [0.0] * 50 + [1.0] + [0.0] * 54,
        })
        queues, precision = compare_review_queues(scored.iloc[::-1])
        lookup = queues.set_index(["Cohort", "Daily limit", "Policy"])
        full = lookup.loc[("All transactions", 50, "Amount baseline")]
        restricted = lookup.loc[("Amount at or below 220", 50, "Amount baseline")]
        model = lookup.loc[("All transactions", 50, "Logistic regression")]
        self.assertEqual(full["Reviews"], 52)
        self.assertEqual(full["Fraud caught"], 1)
        self.assertEqual(full["Fraud-labelled value caught"], 300.0)
        self.assertEqual(restricted["Fraud caught"], 1)
        self.assertEqual(restricted["Fraud-labelled value caught"], 10.0)
        self.assertEqual(restricted["Recall"], 1.0)
        self.assertEqual(model["Fraud caught"], 2)
        self.assertEqual(len(precision), 4)

        export = build_rank_export(scored.iloc[::-1]).set_index("TRANSACTION_ID")
        self.assertEqual(export.loc[50, "tx_amount_rank_all"], 51)
        self.assertEqual(export.loc[50, "tx_amount_rank_le_220"], 50)
        self.assertEqual(export.loc[50, "model_score_rank_all"], 1)
        self.assertEqual(export.loc[103, "tx_amount_rank_all"], 1)
        self.assertTrue(pd.isna(export.loc[0, "tx_amount_rank_le_220"]))
        self.assertTrue(pd.isna(export.loc[0, "model_score_rank_le_220"]))
