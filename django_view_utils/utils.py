import sys
from collections.abc import Callable
from collections.abc import Sequence
from functools import wraps
from importlib import import_module
from typing import Any

from django.contrib.auth.views import redirect_to_login
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.urls import include
from django.urls import URLPattern
from django.urls import URLResolver

from django_view_utils.apps import ViewRegistry

# If python version is <= 3.10, use typing_extensions
if sys.version_info[1] > 10:
    from typing import TypeVarTuple
else:
    from typing_extensions import TypeVarTuple


def view(
    paths: str | list[str],
    name: str,
    login_required: bool = False,
    staff_required: bool = False,
    permissions: str | list[str] | None = None,
) -> Callable[
    [Callable[[HttpRequest], HttpResponse]],
    Callable[[HttpRequest], HttpResponse],
]:
    """
    Decorator for Django views.

    :param paths: List of paths for the view.
    :param name: Name of the view.
    :param login_required: Whether the view requires the user to be logged in.
    :param staff_required: Whether the view requires the user to be staff.
    :param permissions: List of permissions required for the view.
    """

    def decorator(
        view_func: Callable[[HttpRequest], HttpResponse],
    ) -> Callable[[HttpRequest], HttpResponse]:
        @wraps(view_func)
        def wrapper(
            request: HttpRequest,
            *args: TypeVarTuple,
            **kwargs: Any,
        ) -> HttpResponse:
            if login_required and not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())

            if staff_required and not request.user.is_staff:
                return HttpResponseForbidden()

            if permissions and not request.user.has_perms(permissions):
                return HttpResponseForbidden()

            return view_func(request, *args, **kwargs)

        ViewRegistry.register(name=name, paths=paths, view_func=wrapper)

        return wrapper

    return decorator


def include_view_urls(
    *,
    modules: list[str],
) -> tuple[Sequence[URLResolver | URLPattern], str | None, str | None]:
    for module in modules:
        import_module(f"{module}")

    return include("django_view_utils.urls")
