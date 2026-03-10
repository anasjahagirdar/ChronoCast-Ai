from django.urls import path

from .views import model_registry_summary


urlpatterns = [
    path("", model_registry_summary, name="model-registry-summary"),
]
