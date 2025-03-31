# -*- coding: utf-8 -*-

import pytest
from cookiecutter_maker.str_replace import (
    validate_selector,
    to_placeholder,
    replace_with_placeholders,
)


def _test_validate_selector(selector, valid):
    if valid:
        validate_selector(selector)
    else:
        with pytest.raises(ValueError):
            validate_selector(selector)


def test_validate_selector():
    # fmt: off
    cases = [
        # Valid selectors - each pattern is a substring of the previous
        (["abcdef", "cde", "de"], True),
        (["pattern"], True),
        (["abc", "abc", "abc"], True),  # Identical patterns are valid
        (["abc", "ab", ""], True),  # Empty string is a substring of any string
        # Invalid selectors
        (["abc", "def"], False),  # "def" is not in "abc"
        (["", "a"], False),  # "a" is not in ""
        (["abc", "ABC"], False),  # Case-sensitive comparison
    ]
    # fmt: on
    for selector, valid in cases:
        _test_validate_selector(selector, valid)


def _test_to_placeholder(name, selector, expected):
    assert to_placeholder(name, selector) == expected


def test_to_placeholder():
    # fmt: off
    cases = [
        # Basic test case from the docstring
        (
            "author",
            ['author = "Alice"', '= "Alice"', "Alice"],
            'author = "{{ cookiecutter.author }}"'
        ),
        # Single pattern case
        (
            "project_name",
            ["my_project"],
            "{{ cookiecutter.project_name }}"
        ),
        # Multiple replacements
        (
            "version",
            ["version=1.0.0", "=1.0.0", "1.0.0"],
            "version={{ cookiecutter.version }}"
        ),
        # Multiple words with spaces
        (
            "full_name",
            ["name: John Doe", "John Doe"],
            "name: {{ cookiecutter.full_name }}"
        ),
        # With special characters
        (
            "email",
            ["email: user@example.com", "user@example.com"],
            "email: {{ cookiecutter.email }}"
        ),
        # With numbers and symbols
        (
            "port",
            ["PORT=8080", "8080"],
            "PORT={{ cookiecutter.port }}"
        ),
        # Path-like strings
        (
            "package_name",
            ["/path/to/mypackage", "to/mypackage", "mypackage"],
            "/path/to/{{ cookiecutter.package_name }}"
        ),
        # Using quotes and escapes
        (
            "quote",
            ['text = "quoted"', '"quoted"', "quoted"],
            'text = "{{ cookiecutter.quote }}"'
        ),
        # Multiple identical patterns
        (
            "repeated",
            ["pattern", "pattern", "pattern"],
            "{{ cookiecutter.repeated }}"
        ),
    ]
    # fmt: on
    for name, selector, expected in cases:
        _test_to_placeholder(name, selector, expected)


def _test_replace_with_placeholders(text, replacements, expected):
    assert replace_with_placeholders(text, replacements) == expected


def test_replace_with_placeholders():
    cases = [
        (
            "john, john@email.com",
            [
                ("john@email.com", "email"),
                ("john", "name"),
            ],
            "name, email",
        ),
        (
            "project, project_dir, project_file",
            [
                ("project_dir", "pkg_path"),
                ("project_file", "pkg_module"),
                ("project", "pkg"),
            ],
            "pkg, pkg_path, pkg_module",
        ),
    ]
    for text, replacements, expected in cases:
        _test_replace_with_placeholders(text, replacements, expected)


def test_parameter():
    param = Parameter(
        selector=['author = "Alice"', '= "Alice"', "Alice"],
        name="author",
        default="Alice",
        choice=[],
    )


if __name__ == "__main__":
    from cookiecutter_maker.tests import run_cov_test

    run_cov_test(
        __file__,
        "cookiecutter_maker.parameter",
        preview=False,
    )
