from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ML_PIPELINE_DIR = PROJECT_ROOT / "ml_pipeline"
DATA_DIR = ML_PIPELINE_DIR / "data_pipeline" / "data"
MODELS_DIR = ML_PIPELINE_DIR / "models"
REPORTS_DIR = ML_PIPELINE_DIR / "monitoring" / "reports"
MLRUNS_DIR = PROJECT_ROOT / "mlruns"
MLFLOW_DB_PATH = PROJECT_ROOT / "mlflow.db"

RAW_DATA_PATH = DATA_DIR / "btc_usd_raw.csv"
PROCESSED_DATA_PATH = DATA_DIR / "btc_usd_processed.csv"
FEATURE_DATA_PATH = DATA_DIR / "btc_usd_features.csv"

FEATURE_COLUMNS = [
    "ma_7",
    "ma_30",
    "volatility",
    "lag_1",
    "lag_7",
    "return",
]

TARGET_COLUMN = "close"
DATE_COLUMN = "date"
LSTM_WINDOW_SIZE = 30
FORECAST_HORIZON_DAYS = 7

MLFLOW_EXPERIMENT_NAME = os.getenv(
    "MLFLOW_EXPERIMENT_NAME",
    "chronocast_btc_forecasting",
)
MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    f"sqlite:///{MLFLOW_DB_PATH.as_posix()}",
)

MODEL_REGISTRY_NAMES = {
    "linear_regression": "ChronoCast_Linear_Model",
    "arima": "ChronoCast_ARIMA_Model",
    "lstm": "ChronoCast_LSTM_Model",
}

MODEL_ARTIFACT_NAMES = {
    "linear_regression": "linear_forecaster",
    "arima": "arima_forecaster",
    "lstm": "lstm_forecaster",
}

PRODUCTION_STAGE = "Production"
DEFAULT_API_REFRESH_SECONDS = int(os.getenv("CHRONOCAST_REFRESH_SECONDS", "30"))
