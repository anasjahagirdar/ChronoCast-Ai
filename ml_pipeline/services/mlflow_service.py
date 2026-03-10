from __future__ import annotations

from datetime import datetime, timezone
from math import inf

import mlflow
from mlflow.entities import ViewType

from ml_pipeline.config import MLFLOW_EXPERIMENT_NAME, MODEL_REGISTRY_NAMES
from mlops.mlflow.mlflow_config import get_mlflow_client, setup_mlflow


def _ms_to_iso(timestamp_ms):
    if not timestamp_ms:
        return None
    return datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).isoformat()


def _safe_float(value):
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def get_experiment():
    try:
        setup_mlflow()
        return mlflow.get_experiment_by_name(MLFLOW_EXPERIMENT_NAME)
    except Exception:
        return None


def list_experiment_runs(limit: int = 20) -> list[dict[str, object]]:
    experiment = get_experiment()
    if experiment is None:
        return []

    try:
        client = get_mlflow_client()
        runs = client.search_runs(
            [experiment.experiment_id],
            order_by=["attribute.start_time DESC"],
            run_view_type=ViewType.ACTIVE_ONLY,
            max_results=limit,
        )
    except Exception:
        return []

    serialized = []
    for run in runs:
        metrics = {name: _safe_float(value) for name, value in run.data.metrics.items()}
        duration_ms = None
        if run.info.end_time and run.info.start_time:
            duration_ms = run.info.end_time - run.info.start_time

        serialized.append(
            {
                "run_id": run.info.run_id,
                "run_name": run.data.tags.get("mlflow.runName", run.info.run_id[:8]),
                "status": run.info.status,
                "artifact_uri": run.info.artifact_uri,
                "start_time": _ms_to_iso(run.info.start_time),
                "end_time": _ms_to_iso(run.info.end_time),
                "duration_seconds": round(duration_ms / 1000, 2) if duration_ms else None,
                "params": dict(run.data.params),
                "metrics": metrics,
                "tags": dict(run.data.tags),
                "model_type": run.data.params.get("model_type", "unknown"),
            }
        )

    return serialized


def summarize_experiments(limit: int = 20) -> dict[str, object]:
    runs = list_experiment_runs(limit=limit)
    if not runs:
        return {
            "total_runs": 0,
            "best_run_name": None,
            "best_mae": None,
            "last_run_at": None,
        }

    ranked = sorted(runs, key=lambda item: item["metrics"].get("mae") or inf)
    return {
        "total_runs": len(runs),
        "best_run_name": ranked[0]["run_name"],
        "best_mae": ranked[0]["metrics"].get("mae"),
        "last_run_at": runs[0]["start_time"],
    }


def list_registered_models() -> list[dict[str, object]]:
    try:
        client = get_mlflow_client()
    except Exception:
        return []
    versions = []

    for model_type, model_name in MODEL_REGISTRY_NAMES.items():
        try:
            search_results = client.search_model_versions(f"name='{model_name}'")
        except Exception:
            search_results = []

        for version in search_results:
            run_metrics = {}
            if version.run_id:
                try:
                    run_metrics = {
                        key: _safe_float(value)
                        for key, value in client.get_run(version.run_id).data.metrics.items()
                    }
                except Exception:
                    run_metrics = {}

            versions.append(
                {
                    "model_name": model_name,
                    "model_type": model_type,
                    "version": int(version.version),
                    "stage": version.current_stage or "None",
                    "status": version.status,
                    "run_id": version.run_id,
                    "source": version.source,
                    "model_uri": f"models:/{model_name}/{version.version}",
                    "created_at": _ms_to_iso(version.creation_timestamp),
                    "updated_at": _ms_to_iso(version.last_updated_timestamp),
                    "mae": run_metrics.get("mae"),
                    "rmse": run_metrics.get("rmse"),
                    "tags": dict(getattr(version, "tags", {}) or {}),
                }
            )

    return sorted(
        versions,
        key=lambda item: (
            0 if item["stage"] == "Production" else 1,
            item["mae"] if item["mae"] is not None else inf,
            -item["version"],
        ),
    )


def get_model_leaderboard() -> list[dict[str, object]]:
    best_per_model = {}
    for record in list_registered_models():
        key = record["model_name"]
        current_best = best_per_model.get(key)
        if current_best is None:
            best_per_model[key] = record
            continue

        current_score = current_best["mae"] if current_best["mae"] is not None else inf
        next_score = record["mae"] if record["mae"] is not None else inf
        if next_score < current_score or (
            next_score == current_score and record["version"] > current_best["version"]
        ):
            best_per_model[key] = record

    return sorted(best_per_model.values(), key=lambda item: item["mae"] or inf)


def get_best_candidate():
    leaderboard = get_model_leaderboard()
    if not leaderboard:
        return None
    production_candidates = [item for item in leaderboard if item["stage"] == "Production"]
    ranked = production_candidates or leaderboard
    return ranked[0]
