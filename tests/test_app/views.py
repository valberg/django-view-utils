from django.http import HttpRequest
from django.http import HttpResponse
from django_view_decorator import namespaced_decorator_factory

from .models import Bar
from django_view_utils.generic.list import render_list


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
