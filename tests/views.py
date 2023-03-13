from django.http import HttpRequest
from django.http import HttpResponse

from django_view_utils.utils import view


@view(
    paths="foo",
    name="foo",
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
