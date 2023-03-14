from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeAlias

from django.apps import AppConfig
from django.http import HttpRequest
from django.http import HttpResponse
from django.urls import path

from .conf import conf


ViewType: TypeAlias = Callable[[HttpRequest, ...], HttpResponse]


@dataclass(kw_only=True)
class View:
    paths: str | list[str]
    view: ViewType


class ViewRegistry:
    views: dict[str, View] = {}

    @classmethod
    def register(cls, *, name: str, paths: str, view_func: ViewType):
        cls.views[name] = View(paths=paths, view=view_func)

    @classmethod
    def urlpatterns(cls):
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

    def ready(self):
        if conf.DJANGO_VIEW_UTILS_AUTODISCOVER_VIEWS:
            from django.utils.module_loading import autodiscover_modules

            autodiscover_modules("views")
