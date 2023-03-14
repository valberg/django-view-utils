from functools import wraps
from importlib import import_module

from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden
from django.urls import include

from django_view_utils.apps import ViewRegistry


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

            return view_func(request, *args, **kwargs)

        ViewRegistry.register(name=name, paths=paths, view_func=wrapper)

        return wrapper

    return decorator


def include_view_urls(*modules: str):
    for module in modules:
        import_module(f"{module}")

    return include("django_view_utils.urls")
