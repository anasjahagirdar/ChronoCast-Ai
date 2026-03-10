from __future__ import annotations

import time

import mlflow

from ml_pipeline.config import MLFLOW_TRACKING_URI, PRODUCTION_STAGE
from mlops.mlflow.mlflow_config import get_mlflow_client


class ModelRegistryManager:
    def __init__(self, tracking_uri: str = MLFLOW_TRACKING_URI):
        mlflow.set_tracking_uri(tracking_uri)
        self.client = get_mlflow_client()

    def register_model(self, model_uri: str, model_name: str, tags: dict | None = None):
        result = mlflow.register_model(model_uri=model_uri, name=model_name, tags=tags or {})
        self._wait_until_ready(model_name, int(result.version))
        return int(result.version)

    def _wait_until_ready(self, model_name: str, version: int, timeout_seconds: int = 60):
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            model_version = self.client.get_model_version(name=model_name, version=str(version))
            if model_version.status == "READY":
                return
            time.sleep(1)
        raise TimeoutError(f"Model {model_name} version {version} did not become READY in time.")

    def promote_to_stage(self, model_name: str, version: int, stage: str):
        self.client.transition_model_version_stage(
            name=model_name,
            version=str(version),
            stage=stage,
            archive_existing_versions=(stage == PRODUCTION_STAGE),
        )
        return stage

    def promote_to_production(self, model_name: str, version: int):
        self.promote_to_stage(model_name=model_name, version=version, stage=PRODUCTION_STAGE)
        try:
            self.client.set_registered_model_alias(
                name=model_name,
                alias="production",
                version=str(version),
            )
        except Exception:
            pass
        return PRODUCTION_STAGE
