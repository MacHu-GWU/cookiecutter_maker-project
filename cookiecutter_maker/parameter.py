# -*- coding: utf-8 -*-

"""

"""

import typing as T
import dataclasses
from functools import cached_property

from .str_replace import validate_selector, to_placeholder, replace_with_placeholders
from .path_matcher import PathMatcher


@dataclasses.dataclass
class Parameter:
    """
    :param selector: The selector to locate the text placeholder in the file.
    :param name: The name of the parameter.
    :param default: The default value of the parameter.
    :param choice: The list of choices for the parameter.
    """

    selector: list[str] = dataclasses.field()
    name: str = dataclasses.field()
    default: T.Any = dataclasses.field()
    choice: list[T.Any] = dataclasses.field(default_factory=list)
    include: list[str] = dataclasses.field(default_factory=list)
    exclude: list[str] = dataclasses.field(default_factory=list)

    def _validate(self):
        # if self.choice:
        #     if self.default not in self.choice:
        #         raise ValueError(f"{self.default} is not in {self.choice}")
        pass

    def __post_init__(self):  # pragma: no cover
        validate_selector(self.selector)
        self._validate()

    @cached_property
    def placeholder(self) -> str:  # pragma: no cover
        return to_placeholder(name=self.name, selector=self.selector)

    @cached_property
    def path_matcher(self) -> PathMatcher:
        return PathMatcher.new(include=self.include, exclude=self.exclude)

    def to_cookiecutter_key_value(self) -> tuple[str, T.Any]:
        if self.choice:
            return (self.name, self.choice)
        else:
            return (self.name, self.default)


def replace_with_parameter(
    text: str,
    param_list: list[Parameter],
) -> str:
    replacements = [(param.selector[0], param.placeholder) for param in param_list]
    return replace_with_placeholders(text, replacements)
