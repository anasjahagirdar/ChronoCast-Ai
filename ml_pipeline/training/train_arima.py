from __future__ import annotations

import joblib
import mlflow
import mlflow.pyfunc
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.arima.model import ARIMA

from ml_pipeline.config import (
    MODEL_ARTIFACT_NAMES,
    MODEL_REGISTRY_NAMES,
    MODELS_DIR,
    PROCESSED_DATA_PATH,
    TARGET_COLUMN,
)
from ml_pipeline.mlflow_pyfunc import ArimaForecastModel
from mlops.mlflow.mlflow_config import setup_mlflow
from mlops.mlflow.model_registry import ModelRegistryManager


def train_arima_model(order: tuple[int, int, int] = (5, 1, 0)) -> dict[str, float]:
    setup_mlflow()
    frame = pd.read_csv(PROCESSED_DATA_PATH)
    series = frame[TARGET_COLUMN].astype(float)

    split_index = int(len(series) * 0.8)
    train = series.iloc[:split_index]
    test = series.iloc[split_index:]

    with mlflow.start_run(run_name="ARIMA_Model"):
        model = ARIMA(train, order=order)
        fitted_model = model.fit()
        predictions = fitted_model.forecast(steps=len(test))

        mae = mean_absolute_error(test, predictions)
        rmse = mean_squared_error(test, predictions, squared=False)

        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        local_model_path = MODELS_DIR / "arima_model.pkl"
        joblib.dump(fitted_model, local_model_path)

        mlflow.log_params(
            {
                "model_type": "arima",
                "order": str(order),
                "train_rows": len(train.index),
                "test_rows": len(test.index),
            }
        )
        mlflow.log_metrics({"mae": mae, "rmse": rmse})
        mlflow.pyfunc.log_model(
            artifact_path=MODEL_ARTIFACT_NAMES["arima"],
            python_model=ArimaForecastModel(forecast_steps=1),
            artifacts={"model_path": str(local_model_path)},
        )

        run_id = mlflow.active_run().info.run_id
        model_uri = f"runs:/{run_id}/{MODEL_ARTIFACT_NAMES['arima']}"
        registry = ModelRegistryManager()
        version = registry.register_model(
            model_uri=model_uri,
            model_name=MODEL_REGISTRY_NAMES["arima"],
            tags={"model_type": "arima"},
        )
        registry.promote_to_production(
            model_name=MODEL_REGISTRY_NAMES["arima"],
            version=version,
        )

        return {"mae": float(mae), "rmse": float(rmse), "version": version}


if __name__ == "__main__":
    print(train_arima_model())
