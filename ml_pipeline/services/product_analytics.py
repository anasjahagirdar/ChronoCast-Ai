from __future__ import annotations

from math import inf

import numpy as np

from ml_pipeline.config import MLFLOW_EXPERIMENT_NAME
from ml_pipeline.services.data_service import load_processed_dataset
from ml_pipeline.services.forecast_service import predict_next_price
from ml_pipeline.services.mlflow_service import (
    get_model_leaderboard,
    list_experiment_runs,
    list_registered_models,
    summarize_experiments,
)


def get_models_snapshot() -> dict[str, object]:
    leaderboard = get_model_leaderboard()
    versions = list_registered_models()
    production_model = leaderboard[0] if leaderboard else None
    return {
        "production_model": production_model,
        "leaderboard": leaderboard,
        "versions": versions,
    }


def get_experiments_snapshot(limit: int = 12) -> dict[str, object]:
    return {
        "experiment_name": MLFLOW_EXPERIMENT_NAME,
        "summary": summarize_experiments(limit=limit),
        "runs": list_experiment_runs(limit=limit),
    }


def simulate_roi(investment_amount: float = 10000.0, horizon_days: int = 7) -> dict[str, object]:
    forecast = predict_next_price()
    processed = load_processed_dataset().tail(45).copy()
    close_series = processed["close"].astype(float)
    returns = close_series.pct_change().fillna(0.0)
    latest_price = forecast["latest_price"]
    predicted_price = forecast["predicted_price"]

    expected_return_pct = ((predicted_price - latest_price) / latest_price) * 100
    fee_pct = 0.2
    volatility_pct = float(returns.tail(30).std() * 100)
    upside_buffer = latest_price * (volatility_pct / 100) * 0.75

    scenarios = [
        {
            "label": "Defensive",
            "expected_price": round(predicted_price - upside_buffer, 2),
        },
        {
            "label": "Base",
            "expected_price": round(predicted_price, 2),
        },
        {
            "label": "Bull",
            "expected_price": round(predicted_price + upside_buffer, 2),
        },
    ]

    for scenario in scenarios:
        roi_pct = ((scenario["expected_price"] - latest_price) / latest_price) * 100 - fee_pct
        scenario["roi_pct"] = round(roi_pct, 2)
        scenario["pnl"] = round(investment_amount * (roi_pct / 100), 2)

    buy_and_hold_values = []
    strategy_values = []
    starting_price = float(close_series.iloc[0])
    strategy_multiplier = 0.35 if expected_return_pct < 0 else min(1.25, 0.65 + abs(expected_return_pct) / 5)
    capital = investment_amount

    for _, row in processed.iterrows():
        price_ratio = float(row["close"]) / starting_price
        buy_and_hold_values.append(
            {"date": row["date"].date().isoformat(), "value": round(float(investment_amount * price_ratio), 2)}
        )

    for daily_return, (_, row) in zip(returns, processed.iterrows()):
        capital *= 1 + (daily_return * strategy_multiplier)
        strategy_values.append(
            {"date": row["date"].date().isoformat(), "value": round(float(capital), 2)}
        )

    signal = "Bullish" if expected_return_pct > 1 else "Defensive" if expected_return_pct < -1 else "Neutral"
    return {
        "investment_amount": investment_amount,
        "horizon_days": horizon_days,
        "latest_price": latest_price,
        "predicted_price": predicted_price,
        "expected_return_pct": round(expected_return_pct, 2),
        "signal": signal,
        "volatility_pct": round(volatility_pct, 2),
        "fee_pct": fee_pct,
        "scenarios": scenarios,
        "equity_curve": {
            "strategy": strategy_values,
            "buy_and_hold": buy_and_hold_values,
        },
    }


def get_ab_test_summary() -> dict[str, object]:
    leaderboard = get_model_leaderboard()
    if not leaderboard:
        return {
            "winner": None,
            "confidence": None,
            "lift_pct": None,
            "allocation": {"control": 50, "challenger": 50},
            "variants": [],
            "history": [],
            "is_simulated": True,
        }

    challenger = leaderboard[0]
    control = leaderboard[1] if len(leaderboard) > 1 else leaderboard[0]
    control_mae = control["mae"] or inf
    challenger_mae = challenger["mae"] or inf
    if control_mae in (0, inf) or challenger_mae in (0, inf):
        lift_pct = 0.0
    else:
        lift_pct = ((control_mae - challenger_mae) / control_mae) * 100
    confidence = min(99.0, max(52.0, 65.0 + abs(lift_pct) * 4))

    processed = load_processed_dataset().tail(14)
    history = []
    control_reward = 100.0
    challenger_reward = 100.0
    challenger_edge = max(lift_pct, -8) / 100

    for index, (_, row) in enumerate(processed.iterrows(), start=1):
        realized_return = 0.004 * np.sin(index / 2.3) + ((float(row["close"]) / float(processed.iloc[0]["close"])) - 1) * 0.08
        control_reward *= 1 + realized_return
        challenger_reward *= 1 + realized_return + challenger_edge * 0.03
        history.append(
            {
                "date": row["date"].date().isoformat(),
                "control_reward": round(float(control_reward), 2),
                "challenger_reward": round(float(challenger_reward), 2),
            }
        )

    variants = [
        {
            "variant": "Control",
            "model_name": control["model_name"],
            "model_type": control["model_type"],
            "mae": control["mae"],
            "rmse": control["rmse"],
            "traffic_share": 50,
            "expected_win_rate": round(48.0 - min(6.0, lift_pct / 2), 2),
        },
        {
            "variant": "Challenger",
            "model_name": challenger["model_name"],
            "model_type": challenger["model_type"],
            "mae": challenger["mae"],
            "rmse": challenger["rmse"],
            "traffic_share": 50,
            "expected_win_rate": round(52.0 + min(8.0, lift_pct / 2), 2),
        },
    ]

    return {
        "winner": challenger["model_name"] if lift_pct >= 0 else control["model_name"],
        "confidence": round(confidence, 2),
        "lift_pct": round(lift_pct, 2),
        "allocation": {"control": 50, "challenger": 50},
        "variants": variants,
        "history": history,
        "is_simulated": True,
    }
