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
from django.urls import path, URLPattern

from .conf import conf


ViewType: TypeAlias = Callable[[HttpRequest, TypeVarTuple], HttpResponse]


@dataclass(kw_only=True)
class View:
    paths: str | list[str]
    view: ViewType


class ViewRegistry:
    views: dict[str, View] = {}

    @classmethod
    def register(
        cls,
        *,
        name: str,
        paths: str | list[str],
        view_func: ViewType,
    ) -> None:
        cls.views[name] = View(paths=paths, view=view_func)

    @classmethod
    def urlpatterns(cls) -> list[URLPattern]:
        urlpatterns = []
        for name, _view in cls.views.items():
            if isinstance(_view.paths, str):
                urlpatterns.append(
                    path(_view.paths, _view.view, name=name),
                )
            else:
                for _path in _view.paths:
                    urlpatterns.append(
                        path(_path, _view.view, name=name),
                    )

        return urlpatterns


class ViewUtilsAppConf(AppConfig):
    name = "django_view_utils"
    verbose_name = "Django View Utils"

    def ready(self) -> None:
        if conf.DJANGO_VIEW_UTILS_AUTODISCOVER_VIEWS:
            from django.utils.module_loading import autodiscover_modules

            autodiscover_modules("views")
