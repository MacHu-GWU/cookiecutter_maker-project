# -*- coding: utf-8 -*-

import typing as T
import itertools

from .exc import MapperValidationError


def validate_mapper(
    mapper: T.List[T.Tuple[str, str]],
):
    """
    For example, if you want to replace ``john.doe -> name`` and
    ``john.doe@email.com -> email``. Then it is possible that you end up with
    ``john.doe@email.com -> {{ name }}@email.com``. This function detect
    if any key is substring of another.
    """
    for key1, key2 in itertools.combinations(
        [k for k, _ in mapper],
        2,
    ):
        if (key1 in key2) or (key2 in key1):
            raise MapperValidationError(
                f"One of {key1!r} and {key2!r} is substring of another!"
            )


def replace(
    text: str,
    mapper: T.List[T.Tuple[str, str]],
) -> str:
    """
    Replace string using mapper.

    Example::

        >>> replace(
        ...     text="my name is john, my email is john@email.com",
        ...     mapper=[
        ...         ("john@email.com", "email"),
        ...         ("john", "name"),
        ...     ],
        ... )
        'my name is {{ name }}, my email is {{ email }}'
    """
    for before, after in mapper:
        text = text.replace(before, after)
    return text
