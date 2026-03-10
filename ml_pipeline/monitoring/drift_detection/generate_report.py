from __future__ import annotations

import json

from ml_pipeline.services.monitoring_service import compute_drift_summary, persist_drift_summary


def generate_drift_report():
    summary = compute_drift_summary()
    persist_drift_summary(summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    generate_drift_report()
