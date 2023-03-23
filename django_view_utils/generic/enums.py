from enum import Enum

__all__ = [
    "LevelEnum",
    "IconEnum",
    "map_icon",
]


class LevelEnum(Enum):
    DEFAULT = "default"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    DANGER = "danger"
    WARNING = "warning"
    INFO = "info"
    LIGHT = "light"
    DARK = "dark"


class IconEnum(Enum):
    CREATE = "create"
    EDIT = "edit"
    DELETE = "delete"
    COPY = "copy"
    DOWNLOAD = "download"
    UPLOAD = "upload"
    VIEW = "view"
    SEARCH = "search"
    FILTER = "filter"
    SORT = "sort"


GLYPHICONS = {
    IconEnum.CREATE: "plus",
    IconEnum.EDIT: "pencil",
    IconEnum.DELETE: "trash",
    IconEnum.COPY: "duplicate",
    IconEnum.DOWNLOAD: "download",
    IconEnum.UPLOAD: "upload",
    IconEnum.VIEW: "eye-open",
    IconEnum.SEARCH: "search",
    IconEnum.FILTER: "filter",
    IconEnum.SORT: "sort",
}


def map_icon(*, value: IconEnum | None) -> str | None:
    if value is None:
        return None

    return f"glyphicon glyphicon-{GLYPHICONS[value]}"
