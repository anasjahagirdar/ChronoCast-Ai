from __future__ import annotations

import json

import pandas as pd

from ml_pipeline.config import (
    DATE_COLUMN,
    FEATURE_COLUMNS,
    FEATURE_DATA_PATH,
    LSTM_WINDOW_SIZE,
    PROCESSED_DATA_PATH,
    TARGET_COLUMN,
)


def _read_csv(path):
    frame = pd.read_csv(path)
    if DATE_COLUMN in frame.columns:
        frame[DATE_COLUMN] = pd.to_datetime(frame[DATE_COLUMN])
    return frame


def load_processed_dataset() -> pd.DataFrame:
    return _read_csv(PROCESSED_DATA_PATH)


def load_feature_dataset() -> pd.DataFrame:
    return _read_csv(FEATURE_DATA_PATH)


def get_recent_history(window: int = 60) -> list[dict[str, object]]:
    processed = load_processed_dataset().tail(window)
    return [
        {
            "date": row[DATE_COLUMN].date().isoformat(),
            "close": float(row[TARGET_COLUMN]),
            "volume": float(row["volume"]),
        }
        for _, row in processed.iterrows()
    ]


def build_inference_frame(window_size: int = LSTM_WINDOW_SIZE):
    feature_frame = load_feature_dataset()
    processed_frame = load_processed_dataset()

    latest_row = feature_frame.iloc[-1].copy()
    close_window = processed_frame[TARGET_COLUMN].tail(window_size).astype(float).tolist()

    payload = {
        DATE_COLUMN: latest_row[DATE_COLUMN].date().isoformat(),
        TARGET_COLUMN: float(latest_row[TARGET_COLUMN]),
        "close_window": json.dumps(close_window),
    }
    for feature_name in FEATURE_COLUMNS:
        payload[feature_name] = float(latest_row[feature_name])

    return pd.DataFrame([payload]), latest_row, close_window


def get_market_snapshot() -> dict[str, float]:
    processed = load_processed_dataset()
    latest = processed.iloc[-1]
    previous = processed.iloc[-2]
    last_7 = processed.tail(7)
    last_30 = processed.tail(30)
    returns = last_30[TARGET_COLUMN].pct_change().dropna()

    return {
        "latest_price": float(latest[TARGET_COLUMN]),
        "change_24h_pct": float(
            ((latest[TARGET_COLUMN] - previous[TARGET_COLUMN]) / previous[TARGET_COLUMN]) * 100
        ),
        "high_7d": float(last_7["high"].max()),
        "low_7d": float(last_7["low"].min()),
        "avg_volume_7d": float(last_7["volume"].mean()),
        "volatility_30d_pct": float(returns.std() * 100),
    }
