from __future__ import annotations

import json

from ml_pipeline.services.forecast_service import predict_next_price


def predict_price():
    return predict_next_price()


if __name__ == "__main__":
    print(json.dumps(predict_price(), indent=2))
