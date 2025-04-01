# -*- coding: utf-8 -*-

from {{ cookiecutter.package_name }}.impl import add_two


def test_add_two():
    assert add_two(1, 2) == 3
