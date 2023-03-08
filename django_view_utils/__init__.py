from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import TypeAlias

from django.contrib.auth.views import redirect_to_login
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.urls import include
from django.urls import path
from django.utils.module_loading import import_string

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
        return view

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


def view(
    paths: str | list[str],
    name: str,
    login_required: bool = False,
    staff_required: bool = False,
    permissions: str | list[str] | None = None,
):
    """
    Decorator for Django views.

    :param paths: List of paths for the view.
    :param name: Name of the view.
    :param login_required: Whether the view requires the user to be logged in.
    :param staff_required: Whether the view requires the user to be staff.
    :param permissions: List of permissions required for the view.
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if login_required and not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())

            if staff_required and not request.user.is_staff:
                return HttpResponseForbidden()

            if permissions and not request.user.has_perms(permissions):
                return HttpResponseForbidden()

            ViewRegistry.register(name=name, paths=paths, view_func=view_func)

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def include_view_urls(*modules: str):
    for module in modules:
        import_string(f"{module}")

    return include("django_view_utils.urls")
