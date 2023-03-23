from django.http import HttpRequest
from django.http import HttpResponse

from .models import Bar
from django_view_utils import namespaced_decorator_factory
from django_view_utils import view
from django_view_utils.generic.list import render_list


@view(
    paths="foo",
    name="foo",
    namespace="foo",
)
def foo_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("foo")


@view(
    paths="login_required",
    name="login_required",
    login_required=True,
)
def login_required_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("login_required")


@view(
    paths="staff_required",
    name="staff_required",
    staff_required=True,
)
def staff_required_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("staff_required")


@view(
    paths="permissions_required",
    name="permissions_required",
    permissions=["auth.view_user"],
)
def permissions_required_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("permissions_required")


@view(
    paths="foo/<int:foo_id>/",
    name="foo_id",
)
def foo_id_view(request: HttpRequest, foo_id: int) -> HttpResponse:
    return HttpResponse(f"{foo_id}")


@view(
    paths="no_arguments/",
    name="same_name",
)
def no_arguments_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("no_arguments")


@view(
    paths="arguments/<int:foo_id>/",
    name="same_name",
)
def arguments_view(request: HttpRequest, foo_id: int) -> HttpResponse:
    return HttpResponse(f"{foo_id}")


@view(
    paths=["bar/", "bar/<int:bar_id>/"],
    name="bar",
)
def bar_view(request: HttpRequest, bar_id: int | None = None) -> HttpResponse:
    if bar_id:
        return HttpResponse(f"{bar_id}")
    return HttpResponse("bar")


namespaced_view = namespaced_decorator_factory(
    namespace="namespaced",
)


@namespaced_view(
    paths="namespaced/baz/",
    name="baz",
)
def baz_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("baz")


generic_view = namespaced_decorator_factory(namespace="generic")


@generic_view(
    paths="generic/list/",
    name="list",
)
def generic_list_view(request: HttpRequest) -> HttpResponse:
    bars = Bar.objects.all()
    columns = [
        ("id", "ID"),
        ("name", "Name"),
        ("foo__name", "Foo Name"),
    ]
    return render_list(
        request=request,
        objects=bars,
        columns=columns,
        list_name="Bars",
    )
