# -*- coding: utf-8 -*-

from my_package.impl import add_two


def test_add_two():
    assert add_two(1, 2) == 3
