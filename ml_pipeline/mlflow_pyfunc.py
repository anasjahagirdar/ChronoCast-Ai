from __future__ import annotations

import json

import joblib
import mlflow.pyfunc
import numpy as np
import pandas as pd


class LinearForecastModel(mlflow.pyfunc.PythonModel):
    def __init__(self, feature_columns: list[str]):
        self.feature_columns = feature_columns
        self.model = None

    def load_context(self, context):
        self.model = joblib.load(context.artifacts["model_path"])

    def predict(self, context, model_input):
        frame = pd.DataFrame(model_input)
        return self.model.predict(frame[self.feature_columns])


class ArimaForecastModel(mlflow.pyfunc.PythonModel):
    def __init__(self, forecast_steps: int = 1):
        self.forecast_steps = forecast_steps
        self.model = None

    def load_context(self, context):
        self.model = joblib.load(context.artifacts["model_path"])

    def predict(self, context, model_input):
        frame = pd.DataFrame(model_input)
        steps = max(len(frame.index), self.forecast_steps, 1)
        forecast = self.model.forecast(steps=steps)
        return np.asarray(forecast, dtype=float)


class LstmForecastModel(mlflow.pyfunc.PythonModel):
    def __init__(self, window_size: int):
        self.window_size = window_size
        self.model = None
        self.scaler = None

    def load_context(self, context):
        from tensorflow import keras

        scaler_bundle = joblib.load(context.artifacts["scaler_path"])
        self.scaler = scaler_bundle["scaler"]
        self.window_size = int(scaler_bundle["window_size"])
        self.model = keras.models.load_model(context.artifacts["model_path"])

    def predict(self, context, model_input):
        frame = pd.DataFrame(model_input)
        if "close_window" not in frame.columns:
            raise ValueError("LSTM inference requires a 'close_window' column.")

        raw_window = frame.iloc[0]["close_window"]
        if isinstance(raw_window, str):
            window = json.loads(raw_window)
        else:
            window = raw_window

        series = np.asarray(window, dtype=float).reshape(-1, 1)
        if len(series) != self.window_size:
            raise ValueError(
                f"Expected {self.window_size} close values, received {len(series)}."
            )

        scaled = self.scaler.transform(series).reshape(1, self.window_size, 1)
        prediction_scaled = self.model.predict(scaled, verbose=0).reshape(-1, 1)
        prediction = self.scaler.inverse_transform(prediction_scaled).ravel()
        return prediction
