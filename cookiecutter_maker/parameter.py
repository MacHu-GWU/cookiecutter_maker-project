# -*- coding: utf-8 -*-

"""
:class:`Parameter`, a concrete value in the seed project to replace with a
cookiecutter variable.
"""

import typing as T
import dataclasses
from functools import cached_property

from .str_replace import validate_selector
from .str_replace import to_placeholder
from .str_replace import replace_with_placeholders
from .path_matcher import PathMatcher


def check_dataclass_kwargs(klass, data: dict[str, T.Any]):
    """
    Validate a dict before passing it as ``**kwargs`` to a dataclass.

    Raise a human-friendly ``ValueError`` for unknown keys (usually a typo in
    the config file) and for missing required fields, instead of the
    ``TypeError`` raised by the dataclass constructor.
    """
    fields = dataclasses.fields(klass)
    field_names = {f.name for f in fields}
    unknown = [k for k in data if k not in field_names]
    if unknown:
        raise ValueError(
            f"Unknown {klass.__name__} field(s): {unknown}, "
            f"valid fields are: {sorted(field_names)}"
        )
    required = [
        f.name
        for f in fields
        if f.default is dataclasses.MISSING
        and f.default_factory is dataclasses.MISSING
    ]
    missing = [k for k in required if k not in data]
    if missing:
        raise ValueError(f"Missing required {klass.__name__} field(s): {missing}")


def check_list_of_str(key: str, value: T.Any):
    """
    Raise a human-friendly ``ValueError`` if ``value`` is not a list of str.
    """
    if isinstance(value, list) is False or not all(isinstance(v, str) for v in value):
        raise ValueError(f"'{key}' must be a list of strings, got {value!r}")


@dataclasses.dataclass
class Parameter:
    """
    A concrete value in the seed project to replace with a cookiecutter variable.

    The ``selector`` is a list of strings, from the broadest context to the
    value itself. Only ``selector[0]`` is searched, and inside each match, the
    last selector is replaced with ``{{ cookiecutter.<name> }}``. This replaces
    a value only in a specific context::

        >>> Parameter(selector=['version = "0.1.1"', "0.1.1"], name="version", default="0.1.1").placeholder
        'version = "{{ cookiecutter.version }}"'

    :param selector: A list of strings, from the broadest context to the value
        to replace. Each string must be a substring of the previous one.
    :param name: The variable name, the placeholder is ``{{ cookiecutter.<name> }}``.
    :param default: The default value in ``cookiecutter.json``.
        Exactly one of ``default`` and ``choice`` is required, unless
        ``in_cookiecutter_json`` is False.
    :param choice: A list of choices, the first one is the default.
        See https://cookiecutter.readthedocs.io/en/stable/advanced/choice_variables.html
    :param prompt: Optional human readable prompt, written to ``__prompts__``
        of ``cookiecutter.json``. A string, or a dict for choice labels.
        See https://cookiecutter.readthedocs.io/en/stable/advanced/human_readable_prompts.html
    :param custom_placeholder: Use this instead of ``{{ cookiecutter.<name> }}``
        to replace the last selector, e.g. ``{{ cookiecutter.package_name | slugify }}``.
    :param in_cookiecutter_json: Whether to add this parameter to
        ``cookiecutter.json``. Set to False for a value derived from another
        variable with ``custom_placeholder``.

    :param include: Optional list of file path patterns (relative to the input dir)
        whose content this parameter is applied to. If empty, apply to all files.
    :param exclude: Optional list of file path patterns whose content this
        parameter is NOT applied to. Exclude takes precedence over include.

    .. note::

        ``include`` and ``exclude`` only limit the file **content**. File and
        directory **names** are always replaced with all parameters, so that a
        file always ends up in its renamed parent directory.

        When a longer selector is excluded from a file, a shorter selector of
        another parameter may match inside it. For example, if ``alice@email.com``
        is excluded from ``LICENSE``, the ``alice`` part may still be replaced by
        the ``alice`` parameter.
    """
    # fmt: off
    selector: list[str] = dataclasses.field()
    name: str = dataclasses.field()
    default: T.Any | None = dataclasses.field(default=None)
    choice: list[T.Any] = dataclasses.field(default_factory=list)
    prompt: str | dict[str, T.Any] | None = dataclasses.field(default=None)
    custom_placeholder: str | None = dataclasses.field(default=None)
    in_cookiecutter_json: bool = dataclasses.field(default=True)
    include: list[str] = dataclasses.field(default_factory=list)
    exclude: list[str] = dataclasses.field(default_factory=list)
    # fmt: on

    def _validate(self):
        """
        :raises ValueError: invalid selector, or not exactly one of ``default``
            and ``choice`` when ``in_cookiecutter_json`` is True.
        """
        check_list_of_str("selector", self.selector)
        validate_selector(self.selector)
        if self.selector[0] == "":
            raise ValueError("'selector' can't be an empty string")
        if isinstance(self.name, str) is False or self.name == "":
            raise ValueError(f"'name' must be a non-empty string, got {self.name!r}")
        if isinstance(self.choice, list) is False:
            raise ValueError(f"'choice' must be a list, got {self.choice!r}")
        check_list_of_str("include", self.include)
        check_list_of_str("exclude", self.exclude)
        if isinstance(self.in_cookiecutter_json, bool) is False:
            raise ValueError(
                f"'in_cookiecutter_json' must be true or false, "
                f"got {self.in_cookiecutter_json!r}"
            )
        if self.in_cookiecutter_json:
            if self.default is None:
                if len(self.choice) == 0:
                    raise ValueError("You have to define either a default value or a list of choices.")
            else:
                if len(self.choice):
                    raise ValueError("You can't define both a default value and a list of choices.")

    def __post_init__(self):
        self._validate()

    @classmethod
    def from_dict(cls, data: dict[str, T.Any]) -> "Parameter":
        """
        Create a :class:`Parameter` from a JSON-compatible dict,
        for example one item of ``parameters`` in ``cookiecutter-maker.json``.
        """
        if isinstance(data, dict) is False:
            raise ValueError(f"Each parameter must be an object, got {data!r}")
        check_dataclass_kwargs(cls, data)
        return cls(**data)

    @cached_property
    def placeholder(self) -> str:
        """
        What ``selector[0]`` is replaced with: ``selector[0]`` with the
        narrowest selector replaced by ``{{ cookiecutter.<name> }}``,
        or by :attr:`custom_placeholder` if it is set.
        """
        return to_placeholder(
            name=self.name,
            selector=self.selector,
            token=self.custom_placeholder,
        )

    @cached_property
    def path_matcher(self) -> PathMatcher:
        """
        The :class:`~cookiecutter_maker.path_matcher.PathMatcher` built from
        ``include`` and ``exclude``.
        """
        return PathMatcher.new(include=self.include, exclude=self.exclude)

    def is_applied_to(self, path: str) -> bool:
        """
        Whether this parameter is applied to the content of the given file.

        :param path: file path relative to the input dir, using ``/`` as separator.
        """
        return self.path_matcher.is_match(path)

    def to_cookiecutter_key_value(self) -> tuple[str, T.Any]:
        """
        The key and value of this parameter in ``cookiecutter.json``:
        the choice list if set, otherwise the default value.
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
    Replace ``selector[0]`` of each parameter with its placeholder, in a single
    pass where the longest match wins. See
    :func:`~cookiecutter_maker.str_replace.replace_with_placeholders`.
    """
    replacements = [(param.selector[0], param.placeholder) for param in param_list]
    return replace_with_placeholders(text, replacements)
