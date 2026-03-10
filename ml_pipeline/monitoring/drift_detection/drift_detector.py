from __future__ import annotations

from ml_pipeline.services.monitoring_service import compute_drift_summary


class DriftDetector:
    def detect_drift(self):
        return compute_drift_summary()
