# -*- coding: utf-8 -*-

import os
import pytest

from cookiecutter_maker.strutils import (
    replace,
)


def test_replace():
    text = "hello alice, hello bob"
    mapper = [
        ("alice", "first person"),
        ("bob", "second person"),
    ]
    assert replace(text, mapper) == "hello first person, hello second person"

    mapper = [
        ("alice", "first person"),
        ("alice bob", "second person"),
    ]
    with pytest.raises(ValueError):
        replace(text, mapper)


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
