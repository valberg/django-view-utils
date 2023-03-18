import sys
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeAlias

# If python version is <= 3.10, use typing_extensions
if sys.version_info[1] > 10:
    from typing import TypeVarTuple
else:
    from typing_extensions import TypeVarTuple

from django.apps import AppConfig
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import path, URLPattern, include

from .conf import conf


ViewType: TypeAlias = Callable[[HttpRequest, TypeVarTuple], HttpResponse]


@dataclass(kw_only=True)
class View:
    paths: str | list[str]
    view: ViewType


class ViewRegistry:
    views: dict[str, dict[str, View]] = {}

    @classmethod
    def register(
        cls,
        *,
        name: str,
        paths: str | list[str],
        view_func: ViewType,
        namespace: str | None = None,
    ) -> None:
        cls.views.setdefault(namespace, {})[name] = View(paths=paths, view=view_func)

    @classmethod
    def urlpatterns(cls) -> list[URLPattern]:
        urlpatterns = []
        for namespace, views in cls.views.items():
            _patterns = []
            for name, _view in views.items():
                if isinstance(_view.paths, str):
                    _patterns.append(
                        path(_view.paths, _view.view, name=name),
                    )
                else:
                    for _path in _view.paths:
                        _patterns.append(
                            path(_path, _view.view, name=name),
                        )
            urlpatterns.append(
                path("", include((_patterns, namespace), namespace=namespace)),
            )

        return urlpatterns


class ViewUtilsAppConf(AppConfig):
    name = "django_view_utils"
    verbose_name = "Django View Utils"

    def ready(self) -> None:
        if conf.DJANGO_VIEW_UTILS_AUTODISCOVER_VIEWS:
            from django.utils.module_loading import autodiscover_modules

            autodiscover_modules("views")
