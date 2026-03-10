from __future__ import annotations

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ml_pipeline.services.product_analytics import simulate_roi


@api_view(["GET"])
def roi_summary(request):
    investment_amount = float(request.query_params.get("investment", 10000))
    horizon_days = int(request.query_params.get("days", 7))
    return Response(
        simulate_roi(
            investment_amount=investment_amount,
            horizon_days=horizon_days,
        )
    )
