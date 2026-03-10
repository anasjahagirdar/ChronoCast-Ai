from __future__ import annotations

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ml_pipeline.services.monitoring_service import get_drift_summary


@api_view(["GET"])
def drift_monitoring(request):
    refresh = request.query_params.get("refresh", "false").lower() == "true"
    return Response(get_drift_summary(refresh=refresh))
