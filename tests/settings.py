from __future__ import annotations

from pathlib import Path
from typing import Any

ALLOWED_HOSTS: list[str] = []

BASE_DIR = Path(__file__).resolve().parent

DATABASES: dict[str, dict[str, Any]] = {}

INSTALLED_APPS = [
    # Third Party
    "django_view_utils",
    # Contrib
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
]

MIDDLEWARE: list[str] = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

ROOT_URLCONF = "tests.urls"

SECRET_KEY = "NOTASECRET"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates" / "django"],
        "OPTIONS": {"context_processors": []},
    },
]

USE_TZ = True

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_URL = "/static/"
