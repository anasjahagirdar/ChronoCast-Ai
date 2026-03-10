from __future__ import annotations

import joblib
import mlflow
import mlflow.pyfunc
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

from ml_pipeline.config import (
    FEATURE_COLUMNS,
    FEATURE_DATA_PATH,
    MODEL_ARTIFACT_NAMES,
    MODEL_REGISTRY_NAMES,
    MODELS_DIR,
    TARGET_COLUMN,
)
from ml_pipeline.mlflow_pyfunc import LinearForecastModel
from mlops.mlflow.mlflow_config import setup_mlflow
from mlops.mlflow.model_registry import ModelRegistryManager


def train_linear_model() -> dict[str, float]:
    setup_mlflow()
    frame = pd.read_csv(FEATURE_DATA_PATH)

    X_train, X_test, y_train, y_test = train_test_split(
        frame[FEATURE_COLUMNS],
        frame[TARGET_COLUMN],
        test_size=0.2,
        shuffle=False,
    )

    with mlflow.start_run(run_name="Linear_Regression_Model"):
        model = LinearRegression()
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        rmse = mean_squared_error(y_test, predictions, squared=False)

        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        local_model_path = MODELS_DIR / "linear_regression.pkl"
        joblib.dump(model, local_model_path)

        mlflow.log_params(
            {
                "model_type": "linear_regression",
                "feature_count": len(FEATURE_COLUMNS),
                "train_rows": len(X_train.index),
                "test_rows": len(X_test.index),
            }
        )
        mlflow.log_metrics({"mae": mae, "rmse": rmse})
        mlflow.pyfunc.log_model(
            artifact_path=MODEL_ARTIFACT_NAMES["linear_regression"],
            python_model=LinearForecastModel(feature_columns=FEATURE_COLUMNS),
            artifacts={"model_path": str(local_model_path)},
        )

        run_id = mlflow.active_run().info.run_id
        model_uri = f"runs:/{run_id}/{MODEL_ARTIFACT_NAMES['linear_regression']}"
        registry = ModelRegistryManager()
        version = registry.register_model(
            model_uri=model_uri,
            model_name=MODEL_REGISTRY_NAMES["linear_regression"],
            tags={"model_type": "linear_regression"},
        )
        registry.promote_to_production(
            model_name=MODEL_REGISTRY_NAMES["linear_regression"],
            version=version,
        )

        return {"mae": float(mae), "rmse": float(rmse), "version": version}


if __name__ == "__main__":
    print(train_linear_model())
