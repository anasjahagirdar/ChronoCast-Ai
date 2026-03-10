from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

import joblib
import mlflow
import mlflow.pyfunc
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler

from ml_pipeline.config import (
    LSTM_WINDOW_SIZE,
    MODEL_ARTIFACT_NAMES,
    MODEL_REGISTRY_NAMES,
    MODELS_DIR,
    PROCESSED_DATA_PATH,
    TARGET_COLUMN,
)
from ml_pipeline.mlflow_pyfunc import LstmForecastModel
from mlops.mlflow.mlflow_config import setup_mlflow
from mlops.mlflow.model_registry import ModelRegistryManager


def _run_version_check(command: list[str]) -> bool:
    try:
        result = subprocess.run(
            command + ["--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return False
    return "3.10" in (result.stdout + result.stderr)


def resolve_python_3_10() -> list[str] | None:
    env_python = os.getenv("CHRONOCAST_TF_PYTHON")
    candidates = []
    if env_python:
        candidates.append([env_python])

    repo_root = Path(__file__).resolve().parents[2]
    if os.name == "nt":
        candidates.append([str(repo_root / "venv310" / "Scripts" / "python.exe")])
        candidates.append(["py", "-3.10"])
    else:
        candidates.append([str(repo_root / "venv310" / "bin" / "python")])
        candidates.append(["python3.10"])

    for command in candidates:
        if _run_version_check(command):
            return command
    return None


def ensure_tensorflow_runtime(args: argparse.Namespace):
    if args.tf310_child or sys.version_info[:2] == (3, 10):
        return

    target_python = resolve_python_3_10()
    if target_python is None:
        raise RuntimeError(
            "TensorFlow training requires Python 3.10. "
            "Set CHRONOCAST_TF_PYTHON to a Python 3.10 interpreter or create ./venv310."
        )

    command = target_python + [__file__, "--tf310-child"]
    if args.epochs is not None:
        command += ["--epochs", str(args.epochs)]
    if args.batch_size is not None:
        command += ["--batch-size", str(args.batch_size)]
    if args.window_size is not None:
        command += ["--window-size", str(args.window_size)]

    raise SystemExit(subprocess.call(command))


def import_tensorflow_modules():
    os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
    from tensorflow.keras import Sequential
    from tensorflow.keras.callbacks import EarlyStopping
    from tensorflow.keras.layers import Dense, Dropout, LSTM

    return Sequential, LSTM, Dense, Dropout, EarlyStopping


def parse_args():
    parser = argparse.ArgumentParser(description="Train the ChronoCast LSTM forecaster.")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--window-size", type=int, default=LSTM_WINDOW_SIZE)
    parser.add_argument("--tf310-child", action="store_true")
    return parser.parse_args()


def load_dataset() -> pd.DataFrame:
    return pd.read_csv(PROCESSED_DATA_PATH)


def create_sliding_window_dataset(series: np.ndarray, window_size: int):
    X, y = [], []
    for index in range(window_size, len(series)):
        X.append(series[index - window_size : index, 0])
        y.append(series[index, 0])

    X_array = np.asarray(X, dtype=np.float32).reshape(-1, window_size, 1)
    y_array = np.asarray(y, dtype=np.float32)
    return X_array, y_array


def build_model(window_size: int):
    Sequential, LSTM, Dense, Dropout, _ = import_tensorflow_modules()
    model = Sequential(
        [
            LSTM(64, return_sequences=True, input_shape=(window_size, 1)),
            Dropout(0.15),
            LSTM(32),
            Dense(16, activation="relu"),
            Dense(1),
        ]
    )
    model.compile(optimizer="adam", loss="mse")
    return model


def train_lstm_model(epochs: int = 20, batch_size: int = 32, window_size: int = LSTM_WINDOW_SIZE):
    setup_mlflow()
    _, _, _, _, EarlyStopping = import_tensorflow_modules()

    frame = load_dataset()
    scaler = MinMaxScaler()
    scaled_close = scaler.fit_transform(frame[[TARGET_COLUMN]].astype(float))
    X, y = create_sliding_window_dataset(scaled_close, window_size)

    split_index = int(len(X) * 0.8)
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    model = build_model(window_size)
    callbacks = [
        EarlyStopping(
            monitor="val_loss",
            patience=6,
            restore_best_weights=True,
        )
    ]

    with mlflow.start_run(run_name="LSTM_Model"):
        history = model.fit(
            X_train,
            y_train,
            validation_split=0.15,
            epochs=epochs,
            batch_size=batch_size,
            verbose=1,
            callbacks=callbacks,
            shuffle=False,
        )

        predictions_scaled = model.predict(X_test, verbose=0)
        predictions = scaler.inverse_transform(predictions_scaled.reshape(-1, 1)).ravel()
        y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1)).ravel()

        mae = mean_absolute_error(y_test_actual, predictions)
        rmse = mean_squared_error(y_test_actual, predictions, squared=False)

        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        model_path = MODELS_DIR / "lstm_model.keras"
        scaler_path = MODELS_DIR / "lstm_scaler.pkl"
        model.save(model_path)
        joblib.dump({"scaler": scaler, "window_size": window_size}, scaler_path)

        mlflow.log_params(
            {
                "model_type": "lstm",
                "epochs": epochs,
                "batch_size": batch_size,
                "window_size": window_size,
                "train_rows": len(X_train),
                "test_rows": len(X_test),
            }
        )
        mlflow.log_metrics(
            {
                "mae": mae,
                "rmse": rmse,
                "best_val_loss": min(history.history["val_loss"]),
            }
        )
        mlflow.pyfunc.log_model(
            artifact_path=MODEL_ARTIFACT_NAMES["lstm"],
            python_model=LstmForecastModel(window_size=window_size),
            artifacts={
                "model_path": str(model_path),
                "scaler_path": str(scaler_path),
            },
        )

        run_id = mlflow.active_run().info.run_id
        model_uri = f"runs:/{run_id}/{MODEL_ARTIFACT_NAMES['lstm']}"
        registry = ModelRegistryManager()
        version = registry.register_model(
            model_uri=model_uri,
            model_name=MODEL_REGISTRY_NAMES["lstm"],
            tags={"model_type": "lstm"},
        )
        registry.promote_to_production(
            model_name=MODEL_REGISTRY_NAMES["lstm"],
            version=version,
        )

        return {"mae": float(mae), "rmse": float(rmse), "version": version}


def main():
    args = parse_args()
    ensure_tensorflow_runtime(args)
    results = train_lstm_model(
        epochs=args.epochs,
        batch_size=args.batch_size,
        window_size=args.window_size,
    )
    print(results)


if __name__ == "__main__":
    main()
