from django.urls import path

from .views import roi_summary


urlpatterns = [
    path("", roi_summary, name="roi-summary"),
]
