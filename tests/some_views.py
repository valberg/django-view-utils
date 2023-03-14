from django.http import HttpResponse

from django_view_utils.utils import view


@view(paths="baz/", name="baz")
def baz_view(request):
    return HttpResponse("baz")
