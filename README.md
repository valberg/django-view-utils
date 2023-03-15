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
from django_view_utils.utils import view

@view(paths="/hello-world/", name="hello-world")
def my_view(request):
    ...
```

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
