from __future__ import annotations

from unittest.mock import patch

from django.test import Client, SimpleTestCase


class ChronoCastApiSmokeTests(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    @patch(
        "predictions.views.predict_next_price",
        return_value={
            "latest_price": 67421.0,
            "predicted_price": 67850.0,
            "model_version": 3,
            "mae": 425.0,
            "rmse": 520.0,
            "drift_status": "No Drift",
        },
    )
    def test_predictions_endpoint(self, _mock_prediction):
        response = self.client.get("/api/predictions/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["predicted_price"], 67850.0)

    @patch(
        "experiments.views.get_experiments_snapshot",
        return_value={"summary": {"total_runs": 2}, "runs": []},
    )
    def test_experiments_endpoint(self, _mock_experiments):
        response = self.client.get("/api/experiments/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["summary"]["total_runs"], 2)

    @patch(
        "monitoring.views.get_drift_summary",
        return_value={"status": "No Drift", "features": []},
    )
    def test_monitoring_endpoint(self, _mock_monitoring):
        response = self.client.get("/api/monitoring/drift/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "No Drift")

    @patch(
        "monitoring.views.get_drift_summary",
        return_value={"status": "No Drift", "features": []},
    )
    def test_monitoring_root_endpoint(self, _mock_monitoring):
        response = self.client.get("/api/monitoring/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "No Drift")

    @patch(
        "model_registry_api.views.get_models_snapshot",
        return_value={"leaderboard": [], "versions": []},
    )
    def test_models_endpoint(self, _mock_models):
        response = self.client.get("/api/models/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("leaderboard", response.json())

    @patch(
        "roi.views.simulate_roi",
        return_value={"signal": "Bullish", "scenarios": []},
    )
    def test_roi_endpoint(self, _mock_roi):
        response = self.client.get("/api/roi/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["signal"], "Bullish")

    @patch(
        "ab_testing.views.get_ab_test_summary",
        return_value={"winner": "ChronoCast_Linear_Model", "variants": []},
    )
    def test_ab_testing_endpoint(self, _mock_ab):
        response = self.client.get("/api/ab-testing/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["winner"], "ChronoCast_Linear_Model")
