# -*- coding: utf-8 -*-

import pytest
from pathlib import Path
from cookiecutter_maker.api import Parameter, Maker
from cookiecutter_maker.paths import dir_unit_test
from cookiecutter_maker.tests.case import run_case

dir_here = Path(__file__).absolute().parent


def test():
    maker = Maker(
        dir_input=dir_here.joinpath("my_package-project"),
        dir_output=dir_here.joinpath("tmp"),
        parameters=[
            Parameter(
                selector=["my_package"],
                name="package_name",
                default="my_package",
            ),
            Parameter(
                selector=["my-package"],
                name="package_name_slug",
                default="my-package",
            ),
            Parameter(
                selector=[
                    'version = "1.0.0"',
                    "1.0.0",
                ],
                name="version",
                default="0.1.1",
            ),
        ],
        no_render=[
            "my_package/template/*.jinja",
        ],
    )
    run_case(
        maker=maker,
        dir_expected=dir_here.joinpath("{{ cookiecutter.package_name }}-project"),
    )


if __name__ == "__main__":
    from cookiecutter_maker.tests import run_cov_test

    run_cov_test(
        __file__,
        "cookiecutter_maker.maker",
        preview=False,
    )
