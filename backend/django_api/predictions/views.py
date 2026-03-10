from __future__ import annotations

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ml_pipeline.services.forecast_service import predict_next_price


@api_view(["GET"])
def get_prediction(request):
    return Response(predict_next_price())
