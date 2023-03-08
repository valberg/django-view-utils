from django.urls import path

from django_view_utils import include_view_urls

urlpatterns = [
    path(
        "",
        include_view_urls(
            "tests.views",
        ),
    ),
]
