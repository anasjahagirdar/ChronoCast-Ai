from django.urls import path

from .views import experiments_overview


urlpatterns = [
    path("", experiments_overview, name="experiments-overview"),
]
