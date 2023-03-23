import contextlib
from collections.abc import Callable
from dataclasses import dataclass
from functools import reduce
from typing import Any

from django.core.exceptions import FieldError
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
from django.db.models import QuerySet
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

try:
    from zen_queries import queries_disabled
except ImportError:
    queries_disabled = contextlib.nullcontext

try:
    from django_filters import FilterSet
except ImportError:
    FilterSet = None

from .enums import IconEnum
from .enums import LevelEnum
from .enums import map_icon

__all__ = [
    "RowAction",
    "ViewRowAction",
    "DeleteRowAction",
    "EditRowAction",
    "ListAction",
    "CreateListAction",
    "render_list",
]

from ..utils import paginated_context


# Public


@dataclass(kw_only=True)
class RowAction:
    """
    An action that can be performed on a row in a table.

    :param label: The label of the action
    :param url_name: The name of the URL to reverse
    :param url_kwargs: A dictionary of keyword arguments to pass to the URL
    :param icon: The icon to use for the action
    :param level: The level of the action
    :param show_func: A function that takes an object and returns a boolean
    """

    label: str
    url_name: str
    url_kwargs: dict[str, str]
    icon: IconEnum | None = None
    level: LevelEnum = LevelEnum.DEFAULT
    permissions: list[str] | None = None
    show_func: Callable | None = None

    def reverse_url(self, *, obj: Model) -> str:
        """
        Reverse the URL for this action.
        """
        return reverse(
            self.url_name,
            kwargs={key: getattr(obj, value) for key, value in self.url_kwargs.items()},
        )

    def show(self, *, request: HttpRequest, obj: Model) -> bool:
        """
        Check if this action should be shown.
        """
        has_permissions = (
            all(request.user.has_perm(perm) for perm in self.permissions)
            if self.permissions
            else True
        )
        show_func_result = self.show_func(obj) if self.show_func else True

        return all(
            [
                has_permissions,
                show_func_result,
            ],
        )


@dataclass(kw_only=True)
class ViewRowAction(RowAction):
    label: str = _("View")
    icon: IconEnum = IconEnum.VIEW
    level: LevelEnum = LevelEnum.DEFAULT


@dataclass(kw_only=True)
class DeleteRowAction(RowAction):
    label: str = _("Delete")
    icon: IconEnum = IconEnum.DELETE
    level: LevelEnum = LevelEnum.DANGER


@dataclass(kw_only=True)
class EditRowAction(RowAction):
    label: str = _("Edit")
    icon: IconEnum = IconEnum.EDIT
    level: LevelEnum = LevelEnum.INFO


@dataclass(kw_only=True)
class ListAction:
    """
    An action that can be performed on the whole list.

    :param label: The label of the action
    :param url_name: The name of the URL to reverse
    :param url_kwargs: A dictionary of keyword arguments to pass to the URL
    :param icon: The icon to use for the action
    :param level: The level of the action
    """

    label: str
    url_name: str
    url_kwargs: dict[str, Any] | None = None
    icon: IconEnum | None = None
    level: LevelEnum = LevelEnum.DEFAULT
    permissions: list[str] | None = None

    def reverse_url(self) -> str:
        """
        Reverse the URL for this action.
        """
        return reverse(self.url_name, kwargs=self.url_kwargs or {})

    def icon_class(self):
        return map_icon(value=self.icon)

    def show(self, *, request: HttpRequest) -> bool:
        """
        Check if this action should be shown.
        """
        return (
            all(request.user.has_perm(perm) for perm in self.permissions)
            if self.permissions
            else True
        )


@dataclass(kw_only=True)
class CreateListAction(ListAction):
    label: str = "Create"
    icon: IconEnum = IconEnum.CREATE
    level: LevelEnum = LevelEnum.SUCCESS


def render_list(
    *,
    request: HttpRequest,
    objects: QuerySet,
    list_name: str,
    columns: list[tuple[str, str]],
    row_actions: list[RowAction] | None = None,
    list_actions: list[ListAction] | None = None,
    back_url: str | None = None,
    filter_set_class: type[FilterSet] | None = None,
    header_template: str | None = None,
    header_context: dict[str, Any] | None = None,
    footer_template: str | None = None,
    footer_context: dict[str, Any] | None = None,
) -> HttpResponse:
    """
    Render a list of objects with a table.

    :param request: The HTTP request
    :param objects: The objects to render
    :param list_name: The name of the list
    :param columns: A list of tuples containing the accessor name and the column name
    :param row_actions: A list of actions that can be performed on each row
    :param list_actions: A list of actions that can be performed on the whole list
    :param back_url: The URL to go back to
    :param filter_set_class: A FilterSet class to filter the objects
    :param header_template: The name of the template to render in the header
    :param header_context: A dictionary of context variables to pass to the header
        template
    :param footer_template: The name of the template to render in the footer
    :param footer_context: A dictionary of context variables to pass to the footer
        template
    """
    header_footer_context = {}

    if header_template:
        header_context = header_context or {}
        rendered_header = render_to_string(header_template, header_context)
        header_footer_context["header"] = rendered_header

    if footer_template:
        footer_context = footer_context or {}
        rendered_footer = render_to_string(footer_template, footer_context)
        header_footer_context["footer"] = rendered_footer

    context = header_footer_context | _list_context(
        request=request,
        objects=objects,
        list_name=list_name,
        columns=columns,
        row_actions=row_actions,
        list_actions=list_actions,
        back_url=back_url,
        paginate_by=25,
        filter_set_class=filter_set_class,
    )

    render_kwargs = {
        "request": request,
        "template_name": "generic/list.html",
        "context": context,
    }
    return render(**render_kwargs)


# Internals


@dataclass
class Row:
    """
    A row in a table.
    """

    data: dict[str, str]
    actions: list[dict[str, str]]


def _filterset_context(
    *,
    request: HttpRequest,
    filter_set_class: type[FilterSet],
    objects: QuerySet,
) -> tuple[dict[str, Any], QuerySet]:
    if filter_set_class and FilterSet is None:
        raise ImproperlyConfigured(
            "You must install django-filter to use filtersets.",
        )
    filter_set = filter_set_class(request.GET, queryset=objects)
    objects = filter_set.qs
    context = {"filter_form": filter_set.form.as_p()}
    return context, objects


def _list_actions(
    *,
    request: HttpRequest,
    list_actions: list[ListAction],
) -> list[dict[str, str]]:
    return [
        {
            "label": action.label,
            "url": action.reverse_url(),
            "icon": action.icon_class() if action.icon else None,
            "level": action.level.value,
        }
        for action in list_actions
        if action.show(request=request)
    ]


def _rows(
    *,
    request: HttpRequest,
    objects: QuerySet,
    columns: list[tuple[str, str]],
    row_actions: list[RowAction] | None = None,
) -> list[Row]:
    rows = []
    row_actions = row_actions or []
    for obj in objects:
        with queries_disabled():
            row = Row(
                data={
                    # Recurse through the column accessor name to get the value
                    column: reduce(getattr, [obj] + column[0].split("__"))
                    for column in columns
                },
                actions=[
                    {
                        "label": action.label,
                        "url": action.reverse_url(obj=obj),
                        "icon": map_icon(value=action.icon),
                        "level": action.level.value if action.level else None,
                    }
                    for action in row_actions
                    if action.show(
                        request=request,
                        obj=obj,
                    )
                ],
            )
            rows.append(row)
    return rows


def _list_context(
    *,
    request: HttpRequest,
    objects: QuerySet,
    list_name: str,
    columns: list[tuple[str, str]],
    row_actions: list[RowAction] | None = None,
    list_actions: list[ListAction] | None = None,
    back_url: str | None = None,
    paginate_by: int = None,
    filter_set_class: type[FilterSet] | None = None,
):
    order_by = request.GET.get("order_by")
    total_count = len(objects)

    context = {
        "list_name": list_name,
        "columns": columns,
        "total_count": total_count,
        "order_by": order_by,
        "back_url": back_url,
        "row_actions": row_actions,
    }

    # Select related for fields that are using "__" in the accessor name
    objects = objects.select_related(
        *[column[0].split("__")[0] for column in columns if "__" in column[0]],
    )

    if order_by:
        with contextlib.suppress(FieldError):
            objects = objects.order_by(order_by)

    if filter_set_class:
        filterset_context, objects = _filterset_context(
            request=request,
            filter_set_class=filter_set_class,
            objects=objects,
        )
        context |= filterset_context

    if paginate_by:
        context |= paginated_context(
            request=request,
            objects=objects,
            paginate_by=paginate_by,
        )

    context["rows"] = _rows(
        request=request,
        objects=objects,
        columns=columns,
        row_actions=row_actions,
    )

    if list_actions:
        context["list_actions"] = _list_actions(
            request=request,
            list_actions=list_actions,
        )

    return context
