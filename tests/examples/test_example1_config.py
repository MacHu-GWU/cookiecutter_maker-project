# -*- coding: utf-8 -*-

"""
Same as ``test_example1.py``, but the :class:`~cookiecutter_maker.maker.Maker`
is loaded from ``examples/example1/cookiecutter-maker.json``.
"""

from cookiecutter_maker.config import load_maker
from cookiecutter_maker.tests.case import run_case
from cookiecutter_maker.paths import path_enum

dir_example1 = path_enum.dir_project_root.joinpath("examples", "example1")


def test():
    print("")
    maker = load_maker(config=dir_example1.joinpath("cookiecutter-maker.json"))
    assert maker.dir_input == dir_example1.joinpath("my_package-project")
    run_case(
        maker=maker,
        dir_expected_template=dir_example1.joinpath("template"),
        dir_expected_project=dir_example1.joinpath("tmp", "my_package-project"),
    )


if __name__ == "__main__":
    from cookiecutter_maker.tests import run_cov_test

    run_cov_test(
        __file__,
        "cookiecutter_maker.config",
        preview=False,
    )
