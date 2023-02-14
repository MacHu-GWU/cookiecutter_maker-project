# -*- coding: utf-8 -*-

import itertools
import typing as T


def replace(
    text: str,
    mapper: T.List[T.Tuple[str, str]],
) -> str:
    for key1, key2 in itertools.combinations(
        [k for k, _ in mapper],
        2,
    ):
        if (key1 in key2) or (key2 in key1):
            raise ValueError(f"One of {key1!r} and {key2!r} is substring of another!!")
    for before, after in mapper:
        text = text.replace(before, after)
    return text
