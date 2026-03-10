from __future__ import annotations

import mlflow
from mlflow.tracking import MlflowClient

from ml_pipeline.config import MLFLOW_EXPERIMENT_NAME, MLFLOW_TRACKING_URI, MLRUNS_DIR


def setup_mlflow(experiment_name: str = MLFLOW_EXPERIMENT_NAME) -> str:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    MLRUNS_DIR.mkdir(parents=True, exist_ok=True)

    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        if MLFLOW_TRACKING_URI.startswith("http://") or MLFLOW_TRACKING_URI.startswith("https://"):
            experiment_id = mlflow.create_experiment(name=experiment_name)
        else:
            artifact_location = (MLRUNS_DIR / experiment_name).resolve().as_uri()
            experiment_id = mlflow.create_experiment(
                name=experiment_name,
                artifact_location=artifact_location,
            )
    else:
        experiment_id = experiment.experiment_id

    mlflow.set_experiment(experiment_name)
    return experiment_id


def get_mlflow_client() -> MlflowClient:
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    return MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
