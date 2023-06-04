# -*- coding: utf-8 -*-

import os
import pytest

from cookiecutter_maker.strutils import (
    MapperValidationError,
    validate_mapper,
    replace,
)


def test_validate_mapper():
    mapper = [
        ("john", "name"),
        ("john@email.com", "email"),
    ]
    with pytest.raises(MapperValidationError):
        validate_mapper(mapper)


def test_replace():
    text = "hello alice, hello bob"
    mapper = [
        ("alice", "first person"),
        ("bob", "second person"),
    ]
    assert replace(text, mapper) == "hello first person, hello second person"

    text = "john, john@email.com"
    mapper = [
        ("john", "name"),
        ("john@email.com", "email"),
    ]
    assert replace(text, mapper) == "name, name@email.com"

    text = "john, john@email.com"
    mapper = [
        ("john@email.com", "email"),
        ("john", "name"),
    ]
    assert replace(text, mapper) == "name, email"


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
