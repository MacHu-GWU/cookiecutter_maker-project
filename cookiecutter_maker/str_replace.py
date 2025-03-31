# -*- coding: utf-8 -*-

"""
String replacement utilities.
"""

import uuid


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
    """
    previous = None
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
    Replace multiple strings in text using temporary placeholders to avoid substring conflicts.

    Example:

    >>> replace_with_placeholders(
    ...     text='author = "alice", author_email = "alice@email.com"',
    ...     replacements=[
    ...         ("alice@email.com", "{{ cookiecutter.author_email }}"),
    ...         ("alice", "{{ cookiecutter.author }}"),
    ...     ]
    ... )
    'author = "{{ cookiecutter.author }}", author_email = "{{ cookiecutter.author_email }}"'

    :param text: The input text to perform replacements on
    :param replacements: List of tuples (search_string, replace_string)

    :returns: Text with all replacements applied
    """
    # Create a mapping of search strings to unique placeholders and final replacements
    placeholder_map = {}

    # Generate unique placeholders for each search string
    for search_string, replace_string in replacements:
        # Create a unique placeholder using UUID (guaranteed to not be a substring of other content)
        placeholder = f"__PLACEHOLDER_{uuid.uuid4()}__"
        placeholder_map[search_string] = (placeholder, replace_string)

    # First pass: replace all search strings with their placeholders
    result = text
    for search_string, (placeholder, _) in placeholder_map.items():
        result = result.replace(search_string, placeholder)

    # Second pass: replace all placeholders with their final values
    for _, (placeholder, replace_string) in placeholder_map.items():
        result = result.replace(placeholder, replace_string)

    return result


double_curly_brackets_mapper = {
    "{{": "{% raw %}{{{% endraw %}",
    "}}": "{% raw %}}}{% endraw %}",
}

def replace_double_curly_brackets(text: str) -> str:
    for before, after in double_curly_brackets_mapper.items():
        text = text.replace(before, after)
    return text