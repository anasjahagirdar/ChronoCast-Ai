from django.urls import path

from .views import get_prediction


urlpatterns = [
    path("", get_prediction, name="prediction-detail"),
]
