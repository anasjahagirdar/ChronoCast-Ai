from __future__ import annotations

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ml_pipeline.services.product_analytics import get_models_snapshot


@api_view(["GET"])
def model_registry_summary(request):
    return Response(get_models_snapshot())
