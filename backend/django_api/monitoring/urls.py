from django.urls import path

from .views import drift_monitoring


urlpatterns = [
    path("drift/", drift_monitoring, name="drift-monitoring"),
]
