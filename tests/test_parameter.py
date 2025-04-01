# -*- coding: utf-8 -*-

from cookiecutter_maker.parameter import (
    Parameter,
    replace_with_parameter,
)


class TestParameter:
    def test_to_cookiecutter_key_value(self):
        param = Parameter(
            selector=["Alice"],
            name="author",
            default="Alice",
        )
        assert param.to_cookiecutter_key_value() == ("author", "Alice")

        param = Parameter(
            selector=["MIT"],
            name="license",
            choice=["MIT", "AGPL-3.0-or-later", "Proprietary"],
        )
        assert param.to_cookiecutter_key_value() == (
            "license",
            ["MIT", "AGPL-3.0-or-later", "Proprietary"],
        )


if __name__ == "__main__":
    from cookiecutter_maker.tests import run_cov_test

    run_cov_test(
        __file__,
        "cookiecutter_maker.parameter",
        preview=False,
    )
