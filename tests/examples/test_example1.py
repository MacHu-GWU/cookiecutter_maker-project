# -*- coding: utf-8 -*-

from pathlib import Path
from cookiecutter_maker.api import Parameter, Maker
from cookiecutter_maker.tests.case import run_case
from cookiecutter_maker.paths import dir_project_root

dir_example1 = dir_project_root.joinpath("examples", "example1")


def test():
    print("")
    maker = Maker(
        dir_input=dir_example1.joinpath("my_package-project"),
        dir_output=dir_example1.joinpath("tmp"),
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
                    'version = "0.1.1"',
                    "0.1.1",
                ],
                name="version",
                default="0.1.1",
            ),
            Parameter(
                selector=[
                    'authors = [\n    { name = "Alice"',
                    'name = "Alice"',
                    "Alice",
                ],
                name="author",
                default="Alice",
            ),
            Parameter(
                selector=[
                    'email = "alice@email.com" }, # author',
                    'email = "alice@email.com"',
                    "alice@email.com",
                ],
                name="author_email",
                default="alice@email.com",
            ),
            Parameter(
                selector=[
                    'maintainers = [\n    { name = "Alice"',
                    'name = "Alice"',
                    "Alice",
                ],
                name="maintainer",
                default="Alice",
            ),
            Parameter(
                selector=[
                    'email = "alice@email.com" }, # maintainer',
                    'email = "alice@email.com"',
                    "alice@email.com",
                ],
                name="maintainer_email",
                default="alice@email.com",
            ),
            Parameter(
                selector=[
                    'license = "MIT"',
                    "MIT",
                ],
                name="license",
                choice=["MIT", "AGPL-3.0-or-later", "Proprietary"],
            ),
        ],
        include=[

        ],
        exclude=[
            "LICENSE.txt",
        ],
        no_render=[
            "*.jinja",
            "*/vendor/**/*.*",
        ],
        dir_hooks=dir_example1.joinpath("hooks"),
    )
    run_case(
        maker=maker,
        dir_expected_template=dir_example1.joinpath(
            "{{ cookiecutter.package_name }}-project"
        ),
        dir_expected_project=dir_example1.joinpath("tmp", "my_package-project"),
    )


if __name__ == "__main__":
    from cookiecutter_maker.tests import run_cov_test

    run_cov_test(
        __file__,
        "cookiecutter_maker.maker",
        preview=False,
    )
