from typing import Any

from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest


def paginated_context(
    *,
    request: HttpRequest,
    objects: QuerySet,
    paginate_by: int,
) -> dict[str, Any]:
    """
    Returns a context dictionary for paginated object lists.

    :param request: Request object.
    :param objects: QuerySet of objects to paginate.
    :param paginate_by: Number of objects per page.
    :return:
    """
    paginator = Paginator(object_list=objects, per_page=paginate_by)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(number=page_number)

    return {
        "page_obj": page_obj,
        "paginator": paginator,
        "is_paginated": page_obj.has_other_pages(),
    }
