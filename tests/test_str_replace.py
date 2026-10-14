# -*- coding: utf-8 -*-

import random

import jinja2
import pytest

from cookiecutter_maker.str_replace import validate_selector
from cookiecutter_maker.str_replace import to_placeholder
from cookiecutter_maker.str_replace import replace_with_placeholders
from cookiecutter_maker.str_replace import replace_double_curly_brackets
from cookiecutter_maker.str_replace import escape_and_replace


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
        # The longest match wins, regardless of the order
        (
            "john, john@email.com",
            [
                ("john", "name"),
                ("john@email.com", "email"),
            ],
            "name, email",
        ),
        # A replacement is never replaced again
        (
            "a b",
            [
                ("a", "b"),
                ("b", "a"),
            ],
            "b a",
        ),
        # Empty search strings are ignored
        ("abc", [("", "x")], "abc"),
        ("abc", [], "abc"),
    ]
    for text, replacements, expected in cases:
        _test_replace_with_placeholders(text, replacements, expected)

    # Short search strings used to randomly collide with the uuid placeholders
    for _ in range(100):
        assert replace_with_placeholders("alpha beta", [("alpha", "A"), ("ab", "X")]) == "A beta"


def test_replace_double_curly_brackets():
    text = """
    f"{{ \"{name}\" }}".format(name="Alice")
    """.strip()
    text = replace_double_curly_brackets(text)
    assert (
        text
        == 'f"{% raw %}{{{% endraw %} "{name}" {% raw %}}}{% endraw %}".format(name="Alice")'
    )

    # Jinja2 block and comment syntax
    assert replace_double_curly_brackets("{% if x %}") == "{% raw %}{%{% endraw %} if x %}"
    assert replace_double_curly_brackets("${#arr[@]}") == "${% raw %}{#{% endraw %}arr[@]}"
    assert replace_double_curly_brackets("{{{") == "{% raw %}{{{{% endraw %}"
    # a "{" right before "}}" must not form a "{{" with the escape tag
    assert replace_double_curly_brackets('{"a": {}}') == '{"a": {% raw %}{}}{% endraw %}'



def test_escape_and_replace_round_trip():
    """
    Whatever the text is, rendering the result with Jinja2 gives back the text
    with only the search string replaced.
    """
    env = jinja2.Environment(keep_trailing_newline=True, undefined=jinja2.StrictUndefined)
    rng = random.Random(0)
    cases = [
        '{"a": {}}', "${my_proj}", 'f"{my_proj}"', "{{my_proj}}", "{%{{", "{}{}}",
        "{# my_proj #}", "{% raw %}my_proj{% endraw %}", "x {{ y }} raw end",
    ]
    for selector in ["my_proj", "raw", "end"]:
        alphabet = ["{", "}", "%", "#", "-", " ", "$", "\n", selector, "a"]
        texts = cases + [
            "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
            for _ in range(3000)
        ]
        for text in texts:
            template = escape_and_replace(text, [(selector, "{{ cookiecutter.n }}")])
            rendered = env.from_string(template).render(cookiecutter={"n": "Z"})
            assert rendered == text.replace(selector, "Z"), (text, template)


if __name__ == "__main__":
    from cookiecutter_maker.tests import run_cov_test

    run_cov_test(
        __file__,
        "cookiecutter_maker.str_replace",
        preview=False,
    )
