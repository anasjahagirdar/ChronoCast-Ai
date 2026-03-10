from __future__ import annotations

from rest_framework.decorators import api_view
from rest_framework.response import Response

from ml_pipeline.services.product_analytics import get_ab_test_summary


@api_view(["GET"])
def ab_testing_summary(request):
    return Response(get_ab_test_summary())
