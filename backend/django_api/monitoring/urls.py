from django.urls import path

from .views import drift_monitoring


urlpatterns = [
    path("", drift_monitoring, name="monitoring-summary"),
    path("drift/", drift_monitoring, name="drift-monitoring"),
]
