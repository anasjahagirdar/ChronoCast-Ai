from __future__ import annotations

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ml_pipeline.services.product_analytics import get_experiments_snapshot


@api_view(["GET"])
def experiments_overview(request):
    limit = int(request.query_params.get("limit", 12))
    return Response(get_experiments_snapshot(limit=limit))
