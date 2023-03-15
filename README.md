# Django View Utils

[![Tests](https://github.com/valberg/django-view-utils/actions/workflows/test.yml/badge.svg)](https://github.com/valberg/django-view-utils/actions/workflows/test.yml)
[![Documentation](https://readthedocs.org/projects/django-view-utils/badge/?version=latest)](https://django-view-utils.readthedocs.io/en/latest/?badge=latest)
[![PyPI - Version](https://img.shields.io/pypi/v/django-view-utils.svg)](https://pypi.org/project/django-view-utils)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-view-utils.svg)](https://pypi.org/project/django-view-utils)

-----

**django-view-utils** aims to be a collection of useful utilities for Django views. Mainly function based views.

## Features

### `@view` decorator

The `@view` decorator is a simple way to create a view function and register it with a URL.

```python

# <app>/views.url

from django_view_utils import view


@view(paths="/hello-world/", name="hello-world")
def my_view(request):
    ...


# <app>/urls.py

from django.urls import path
from django_view_utils import include_view_urls

urlpatterns = [
    path("", include_view_urls()),
]
```

By default, django-view-utils will look for a `views.py` file in your app.

This can be disabled by setting `DJANGO_VIEW_UTILS_AUTO_DISCOVER` to `False`, then registering view modules is up to you by supplying the `modules` keyword argument to `include_view_urls`.

#### `@view` decorator options
Conveniently it also supports `login_required`, `staff_required` and `permission_required`.

```python
@view(paths="/hello-world/", name="hello-world", login_required=True)
def my_view(request):
    ...

@view(paths="/hello-world/", name="hello-world", staff_required=True)
def my_view(request):
    ...

@view(paths="/hello-world/", name="hello-world", permissions=["myapp.can_do_something"])
def my_view(request):
    ...
```

#### Inspiration

This decorator is very much inspired by the idea of "locality of behaviour" by Carson Gross (creator of HTMX): https://htmx.org/essays/locality-of-behaviour/.

It also bears resemblance to the `@app.route` decorator in Flask, the `@app.<HTTP method>` decorator in FastAPI and probably many other Python web frameworks.


**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install django-view-utils
```

## Development

```console
git clone
cd django-view-utils
pip install hatch
hatch run tests:cov
hatch run tests:typecheck
```

## License

`django-view-utils` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
