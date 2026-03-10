from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/predictions/", include("predictions.urls")),
    path("api/experiments/", include("experiments.urls")),
    path("api/monitoring/", include("monitoring.urls")),
    path("api/models/", include("model_registry_api.urls")),
    path("api/ab-testing/", include("ab_testing.urls")),
    path("api/roi/", include("roi.urls")),
]
