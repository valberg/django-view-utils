# Django View Decorator

[![Tests](https://github.com/valberg/django-view-utils/actions/workflows/test.yml/badge.svg)](https://github.com/valberg/django-view-utils/actions/workflows/test.yml)
[![Documentation](https://readthedocs.org/projects/django-view-utils/badge/?version=latest)](https://django-view-utils.readthedocs.io/en/latest/?badge=latest)
[![PyPI - Version](https://img.shields.io/pypi/v/django-view-utils.svg)](https://pypi.org/project/django-view-utils)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-view-utils.svg)](https://pypi.org/project/django-view-utils)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/valberg/django-view-utils/main.svg)](https://results.pre-commit.ci/latest/github/valberg/django-view-utils/main)

-----

**django-view-utils** aims to be a collection of (opinionated) useful utilities for Django views. Mainly function based views.


**Table of Contents**

- [Features](#features)
- [Motivation](#motivation)
- [Installation](#installation)
- [License](#license)

## Features

### Generic functions

The following generic functions are provided:

- render_list
- render_form

## Motivation

Writing function based views in Django often involves patterns which are perfect candidates for being extracted into
helper functions. This package aims to provide a collection of such functions.

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
