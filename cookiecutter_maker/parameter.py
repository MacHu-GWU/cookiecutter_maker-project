# -*- coding: utf-8 -*-

"""
This module defines the :class:`Parameter` class used for template parameter substitution
in the cookiecutter_maker package. It provides functionality for defining, validating,
and applying parameter replacements when converting concrete projects to cookiecutter
templates.
"""

import typing as T
import dataclasses
from functools import cached_property

from .str_replace import validate_selector, to_placeholder, replace_with_placeholders
from .path_matcher import PathMatcher


@dataclasses.dataclass
class Parameter:
    """
    Defines a parameter for cookiecutter template substitution.

    A Parameter represents a value in the concrete project that should be replaced
    with a cookiecutter variable in the template. Each parameter has a name,
    a selector list for hierarchical matching, and optional values like default,
    choices, include/exclude patterns.

    The selector is a list of strings used for hierarchical matching, where each
    string is a substring of the previous. This provides precise control over
    the replacement process, from more general to more specific matches.

    :param selector: A list of strings for hierarchical matching, from broadest
        to most specific. Each string must be a substring of the previous one.
    :param name: The name of the parameter, used in the cookiecutter placeholder.
    :param default: The default value for the parameter in the ``cookiecutter.json`` file.
        Required if choice is empty.
    :param choice: Optional list of choices for the parameter. If provided, default must be None.
        See https://cookiecutter.readthedocs.io/en/stable/advanced/choice_variables.html
    :param prompt: Optional human readable prompt.
    :param custom_placeholder: Optional custom placeholder string for the parameter,
        this will override the default ``{{ cookiecutter.name }}`` format.
    :param in_cookiecutter_json: Whether to include this parameter in the cookiecutter.json file.
        If False, the parameter will be used for replacements but not added to cookiecutter.json.
        Defaults to True.

    :param include: Optional list of file path patterns where this parameter should be applied.
    :param exclude: Optional list of file path patterns where this parameter should not be applied.

    TODO make parameter level include and exclude really work.
    """
    # fmt: off
    selector: list[str] = dataclasses.field()
    name: str = dataclasses.field()
    default: T.Optional[T.Any] = dataclasses.field(default=None)
    choice: list[T.Any] = dataclasses.field(default_factory=list)
    prompt: T.Optional[T.Union[str, dict[str, T.Any]]] = dataclasses.field(default=None)
    custom_placeholder: T.Optional[str] = dataclasses.field(default=None)
    in_cookiecutter_json: bool = dataclasses.field(default=True)
    include: list[str] = dataclasses.field(default_factory=list)
    exclude: list[str] = dataclasses.field(default_factory=list)
    # fmt: on

    def _validate(self):
        """
        Validate parameter configuration.
        """
        validate_selector(self.selector)
        if self.in_cookiecutter_json:
            if self.default is None:
                if len(self.choice) == 0:
                    raise ValueError("You have to define either a default value or a list of choices.")
            else:
                if len(self.choice):
                    raise ValueError("You can't define both a default value and a list of choices.")

    def __post_init__(self):  # pragma: no cover
        self._validate()

    @cached_property
    def placeholder(self) -> str:  # pragma: no cover
        """
        Generate the cookiecutter placeholder string for this parameter.

        The placeholder is created using the parameter name and selector,
        following the cookiecutter template format: ``{{ cookiecutter.param_name }}``
        """
        if self.custom_placeholder:
            return self.custom_placeholder
        else:
            return to_placeholder(name=self.name, selector=self.selector)

    @cached_property
    def path_matcher(self) -> PathMatcher:
        """
        Create a PathMatcher to determine where this parameter should be applied.
        """
        return PathMatcher.new(include=self.include, exclude=self.exclude)

    def to_cookiecutter_key_value(self) -> tuple[str, T.Any]:
        """
        Generate a key-value pair for the ``cookiecutter.json`` file.
        """
        if self.choice:
            return (self.name, self.choice)
        else:
            return (self.name, self.default)


def replace_with_parameter(
    text: str,
    param_list: list[Parameter],
) -> str:
    """
    Replace text with parameter placeholders.

    This function takes a text string and a list of parameters, and replaces
    occurrences of each parameter's selector with its cookiecutter placeholder.
    """
    replacements = [(param.selector[0], param.placeholder) for param in param_list]
    return replace_with_placeholders(text, replacements)
