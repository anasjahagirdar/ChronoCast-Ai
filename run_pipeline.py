from __future__ import annotations

import os
import subprocess
import sys


def run_step(step_name: str, command: list[str]):
    print("\n==============================")
    print(f"Running Step: {step_name}")
    print("==============================\n")

    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise SystemExit(f"Step failed: {step_name}")

    print(f"\nStep completed: {step_name}")


def main():
    default_python = os.getenv("CHRONOCAST_PYTHON", sys.executable or "python")
    tensorflow_python = os.getenv("CHRONOCAST_TF_PYTHON", default_python)

    steps = [
        ("Data Ingestion", [default_python, "-m", "ml_pipeline.data_pipeline.ingest"]),
        ("Data Preprocessing", [default_python, "-m", "ml_pipeline.data_pipeline.preprocess"]),
        ("Feature Engineering", [default_python, "-m", "ml_pipeline.data_pipeline.feature_engineering"]),
        ("Model Training (Linear Regression)", [default_python, "-m", "ml_pipeline.training.train_linear"]),
        ("Model Training (ARIMA)", [default_python, "-m", "ml_pipeline.training.train_arima"]),
        ("Model Training (LSTM)", [tensorflow_python, "-m", "ml_pipeline.training.train_lstm"]),
        (
            "Drift Detection",
            [default_python, "-m", "ml_pipeline.monitoring.drift_detection.generate_report"],
        ),
    ]

    print("\nStarting ChronoCast ML pipeline\n")
    for step_name, command in steps:
        run_step(step_name, command)

    print("\nChronoCast pipeline completed successfully.")


if __name__ == "__main__":
    main()
