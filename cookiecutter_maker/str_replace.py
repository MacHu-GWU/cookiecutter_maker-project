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
# to keep the generated template symmetric and readable. Leading ``{`` are
# included, otherwise ``{}}`` would become ``{{% raw %}...`` and the
# remaining ``{{`` would start a Jinja2 variable.
_jinja_delimiter_pattern = r"\{*(?:\{\{|\}\}|\{%|\{#)"


def _raw(text: str) -> str:
    return "{% raw %}" + text + "{% endraw %}"


def escape_and_replace(
    text: str,
    replacements: list[tuple[str, str]],
) -> str:
    """
    Escape existing Jinja2 syntax and replace the search strings, in a single
    pass, so that:

    - Jinja2 delimiters ``{{``, ``}}``, ``{%`` and ``{#`` in the text are
      wrapped with ``{% raw %}...{% endraw %}``, and come out of cookiecutter
      unchanged. For example, ``{% if x %}`` in a HTML file, or
      ``${#array[@]}`` in a shell script.
    - The ``{% raw %}`` tags we insert are never touched by a replacement,
      and a search string never matches across them.
    - When search strings overlap, the longest one wins, regardless of the order.
    - A literal ``{`` right before a replacement or ``}`` right after it is
      escaped too, otherwise ``${my_proj}`` would become ``${{{ ... }}}``.

    Example:

    >>> escape_and_replace("${my_proj} {{ x }}", [("my_proj", "{{ cookiecutter.name }}")])
    '${% raw %}{{% endraw %}{{ cookiecutter.name }}{% raw %}}{% endraw %} {% raw %}{{{% endraw %} x {% raw %}}}{% endraw %}'

    :param text: The input text.
    :param replacements: List of tuples (search_string, replace_string).
        Empty search strings are ignored. If a search string appears more than
        once, the last one wins.
    """
    mapping = {
        search_string: replace_string
        for search_string, replace_string in replacements
        if search_string
    }
    # Python regex alternation picks the first alternative that matches,
    # so the search strings come first, longest first.
    alternatives = [re.escape(k) for k in sorted(mapping, key=len, reverse=True)]
    alternatives.append(_jinja_delimiter_pattern)
    pattern = re.compile("|".join(alternatives))

    # Split the text into pieces of (text, kind),
    # kind is "literal", "raw" (escaped Jinja2 syntax) or "replaced"
    pieces = []
    pos = 0
    for match in pattern.finditer(text):
        if match.start() > pos:
            pieces.append((text[pos : match.start()], "literal"))
        matched = match.group(0)
        if matched in mapping:
            pieces.append((mapping[matched], "replaced"))
        else:
            pieces.append((_raw(matched), "raw"))
        pos = match.end()
    if pos < len(text):
        pieces.append((text[pos:], "literal"))

    # Escape the literal braces next to a replacement
    chunks = []
    for i, (piece, kind) in enumerate(pieces):
        if kind == "literal":
            head = tail = ""
            if i > 0 and pieces[i - 1][1] == "replaced" and pieces[i - 1][0].endswith("}"):
                rest = piece.lstrip("}")
                head, piece = piece[: len(piece) - len(rest)], rest
            if (
                i + 1 < len(pieces)
                and pieces[i + 1][1] == "replaced"
                and pieces[i + 1][0].startswith("{")
            ):
                rest = piece.rstrip("{")
                piece, tail = rest, piece[len(rest) :]
            piece = (_raw(head) if head else "") + piece + (_raw(tail) if tail else "")
        chunks.append(piece)
    return "".join(chunks)


def replace_double_curly_brackets(text: str) -> str:
    """
    Escape Jinja2 syntax with raw blocks, see :func:`escape_and_replace`.
    """
    return escape_and_replace(text, [])
