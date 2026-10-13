# -*- coding: utf-8 -*-

"""
String replacement utilities.
"""

import re


def validate_selector(selector: list[str]):
    """
    Validates that each pattern in the selector list is a substring of the previous pattern.

    This function ensures that patterns in a selector form a narrowing hierarchy where
    each subsequent pattern is more specific (a substring) of the previous pattern.

    :param selector: A list of string patterns to validate. Cannot be empty.

    :raises: ValueError, If the selector is empty or if any pattern is not a substring
        of the previous pattern in the sequence.
    """
    if len(selector) == 0:  # pragma: no cover
        raise ValueError("Selector cannot be empty")
    previous = None
    for pattern in selector:
        if previous is None:
            previous = pattern
            continue
        elif pattern in previous:
            pass
        else:
            raise ValueError(f"{pattern} is NOT a sub string of {previous}")


def to_placeholder(
    name: str,
    selector: list[str],
    token: str | None = None,
) -> str:
    """
    Convert a selector to a placeholder token that can be used in a template.

    Example:

    >>> to_placeholder(
    ... name="author",
    ... selector=['author = "Alice"', '= "Alice"', "Alice"]
    ... )
    'author = "{{ cookiecutter.author }}"'

    :param name: The name of the parameter.
    :param selector: A list of string patterns to validate. Cannot be empty.
    :param token: what the narrowest selector is replaced with,
        default to ``{{ cookiecutter.<name> }}``.
    """
    previous = None
    if token is None:
        token = "{{ cookiecutter." + name + " }}"
    for pattern in selector[::-1]:
        if previous is None:
            previous = (pattern, token)
        else:
            token = pattern.replace(previous[0], previous[1])
            # print(f"{token = }, {pattern = }, {previous = }") # for debug only
            previous = (pattern, token)
    return token


def replace_with_placeholders(
    text: str,
    replacements: list[tuple[str, str]],
):
    """
    Replace multiple strings in text in a single pass, so that a replacement
    is never replaced again by a later one.

    When search strings overlap, the longest one wins, regardless of the order
    in ``replacements``. For example, ``alice@email.com`` is replaced as a whole
    even if ``alice`` comes first.

    Example:

    >>> replace_with_placeholders(
    ...     text='author = "alice", author_email = "alice@email.com"',
    ...     replacements=[
    ...         ("alice", "{{ cookiecutter.author }}"),
    ...         ("alice@email.com", "{{ cookiecutter.author_email }}"),
    ...     ]
    ... )
    'author = "{{ cookiecutter.author }}", author_email = "{{ cookiecutter.author_email }}"'

    :param text: The input text to perform replacements on
    :param replacements: List of tuples (search_string, replace_string).
        Empty search strings are ignored. If a search string appears more than
        once, the last one wins.

    :returns: Text with all replacements applied
    """
    mapping = {
        search_string: replace_string
        for search_string, replace_string in replacements
        if search_string
    }
    if not mapping:
        return text
    # Python regex alternation picks the first alternative that matches,
    # so sort by length descending to prefer the longest match.
    pattern = re.compile(
        "|".join(re.escape(k) for k in sorted(mapping, key=len, reverse=True))
    )
    return pattern.sub(lambda match: mapping[match.group(0)], text)


# Jinja2 delimiters that need to be escaped in the seed project.
# Only the opening delimiters matter for Jinja2, ``}}`` is escaped as well
# to keep the generated template symmetric and readable.
_jinja_delimiter_pattern = re.compile(r"\{\{|\}\}|\{%|\{#")


def replace_double_curly_brackets(text: str) -> str:
    """
    Escape Jinja2 syntax with raw blocks.

    When converting a seed project to a cookiecutter template, Jinja2 syntax
    in the original files needs special handling. This function wraps the
    Jinja2 delimiters ``{{``, ``}}``, ``{%`` and ``{#`` with
    ``{% raw %}...{% endraw %}``, so they are preserved as literal text in the
    generated project, rather than being interpreted by cookiecutter. For example,
    ``{% if x %}`` in a seed HTML file, or ``${#array[@]}`` in a seed shell script.
    """
    return _jinja_delimiter_pattern.sub(
        lambda match: "{% raw %}" + match.group(0) + "{% endraw %}",
        text,
    )
