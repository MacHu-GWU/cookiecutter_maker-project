# -*- coding: utf-8 -*-

import pytest

from cookiecutter_maker.parameter import Parameter
from cookiecutter_maker.parameter import replace_with_parameter


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

    def test_validate(self):
        with pytest.raises(ValueError, match="either a default value or a list of choices"):
            Parameter(selector=["a"], name="a")
        with pytest.raises(ValueError, match="both a default value and a list of choices"):
            Parameter(selector=["a"], name="a", default="a", choice=["a", "b"])
        with pytest.raises(ValueError, match="NOT a sub string"):
            Parameter(selector=["abc", "x"], name="a", default="a")
        # no default needed if not in cookiecutter.json
        Parameter(selector=["a"], name="a", in_cookiecutter_json=False)


    def test_placeholder(self):
        param = Parameter(selector=['url = "my-package"', "my-package"], name="slug", default="x")
        assert param.placeholder == 'url = "{{ cookiecutter.slug }}"'

        # custom placeholder keeps the context of the selector hierarchy
        param = Parameter(
            selector=['url = "my-package"', "my-package"],
            name="slug",
            custom_placeholder="{{ cookiecutter.package_name | slugify }}",
            in_cookiecutter_json=False,
        )
        assert param.placeholder == 'url = "{{ cookiecutter.package_name | slugify }}"'

    def test_is_applied_to(self):
        param = Parameter(selector=["a"], name="a", default="a")
        assert param.is_applied_to("any/file.txt") is True

        param = Parameter(
            selector=["a"],
            name="a",
            default="a",
            include=["*.py", "*.toml"],
            exclude=["tests/"],
        )
        assert param.is_applied_to("pyproject.toml") is True
        assert param.is_applied_to("src/a.py") is True
        assert param.is_applied_to("README.md") is False
        assert param.is_applied_to("tests/test_a.py") is False



if __name__ == "__main__":
    from cookiecutter_maker.tests import run_cov_test

    run_cov_test(
        __file__,
        "cookiecutter_maker.parameter",
        preview=False,
    )
