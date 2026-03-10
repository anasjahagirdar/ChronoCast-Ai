from __future__ import annotations

from datetime import timedelta

import joblib
import mlflow.pyfunc
import numpy as np
import pandas as pd

from ml_pipeline.config import FEATURE_COLUMNS, FORECAST_HORIZON_DAYS, MODELS_DIR, MODEL_REGISTRY_NAMES
from ml_pipeline.services.data_service import (
    build_inference_frame,
    get_market_snapshot,
    get_recent_history,
)
from ml_pipeline.services.mlflow_service import get_best_candidate
from ml_pipeline.services.monitoring_service import get_drift_summary


LOCAL_LINEAR_MODEL_PATH = MODELS_DIR / "linear_regression.pkl"


def _load_registered_model():
    best_candidate = get_best_candidate()
    if best_candidate is None:
        return None, None

    try:
        model = mlflow.pyfunc.load_model(best_candidate["model_uri"])
    except Exception:
        return None, None
    return model, best_candidate


def _load_local_fallback_model():
    if not LOCAL_LINEAR_MODEL_PATH.exists():
        return None
    return joblib.load(LOCAL_LINEAR_MODEL_PATH)


def _generate_forecast_points(history: list[dict[str, object]], predicted_price: float):
    latest_point = history[-1]
    latest_price = float(latest_point["close"])
    latest_date = pd.Timestamp(latest_point["date"])
    recent_prices = [point["close"] for point in history[-8:]]
    recent_returns = np.diff(recent_prices) / np.array(recent_prices[:-1])
    momentum = float(recent_returns.mean()) if len(recent_returns) else 0.0
    step = (predicted_price - latest_price) / max(FORECAST_HORIZON_DAYS, 1)

    forecast = []
    for offset in range(1, FORECAST_HORIZON_DAYS + 1):
        projected = latest_price + (step * offset) + (latest_price * momentum * 0.15 * offset)
        forecast.append(
            {
                "date": (latest_date + timedelta(days=offset)).date().isoformat(),
                "predicted_close": round(float(projected), 2),
            }
        )

    return forecast


def predict_next_price() -> dict[str, object]:
    inference_frame, latest_row, close_window = build_inference_frame()
    history = get_recent_history(window=60)

    model, metadata = _load_registered_model()
    if model is not None:
        try:
            prediction = float(model.predict(inference_frame)[0])
            model_name = metadata["model_name"]
            model_version = metadata["version"]
            model_type = metadata["model_type"]
            mae = metadata.get("mae")
            rmse = metadata.get("rmse")
        except Exception:
            model = None

    if model is None:
        local_model = _load_local_fallback_model()
        if local_model is None:
            raise FileNotFoundError("No registered model or local fallback model is available.")

        prediction = float(local_model.predict(inference_frame[FEATURE_COLUMNS])[0])
        model_name = MODEL_REGISTRY_NAMES["linear_regression"]
        model_version = 0
        model_type = "linear_regression"
        mae = None
        rmse = None

    drift_summary = get_drift_summary()
    latest_price = float(latest_row["close"])

    return {
        "latest_price": round(latest_price, 2),
        "predicted_price": round(prediction, 2),
        "model_name": model_name,
        "model_type": model_type,
        "model_version": model_version,
        "mae": round(mae, 4) if mae is not None else None,
        "rmse": round(rmse, 4) if rmse is not None else None,
        "drift_status": drift_summary["status"],
        "last_updated": latest_row["date"].date().isoformat(),
        "market": get_market_snapshot(),
        "history": history,
        "forecast_points": _generate_forecast_points(history, prediction),
        "close_window": close_window,
    }
