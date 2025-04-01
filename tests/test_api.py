# -*- coding: utf-8 -*-

from cookiecutter_maker import api


def test():
    _ = api
    _ = api.Parameter
    _ = api.Maker


if __name__ == "__main__":
    from cookiecutter_maker.tests import run_cov_test

    run_cov_test(
        __file__,
        "cookiecutter_maker.api",
        preview=False,
    )
