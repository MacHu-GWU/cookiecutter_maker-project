# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx


def test():
    import cookiecutter_maker

    _ = cookiecutter_maker.Maker


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
