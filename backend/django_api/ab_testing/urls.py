from django.urls import path

from .views import ab_testing_summary


urlpatterns = [
    path("", ab_testing_summary, name="ab-testing-summary"),
]
