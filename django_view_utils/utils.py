from collections.abc import Sequence
from importlib import import_module

from django.urls import include
from django.urls import URLPattern
from django.urls import URLResolver


def include_view_urls(
    *,
    modules: list[str] | None = None,
) -> tuple[Sequence[URLResolver | URLPattern], str | None, str | None]:
    if modules:
        for module in modules:
            import_module(f"{module}")

    return include("django_view_utils.urls")
