# -*- coding: utf-8 -*-

"""
Load :class:`~cookiecutter_maker.maker.Maker` from a ``cookiecutter-maker.json``
config file, and merge it with command line overrides.

Precedence, from highest to lowest:

1. Command line arguments (any value that is not ``None``).
2. The config file (``--config``, or ``./cookiecutter-maker.json`` if exists).
3. The default values of :class:`~cookiecutter_maker.maker.Maker`.

Relative paths in the config file are resolved against the directory of the
config file, relative paths from the command line are resolved against the
current working directory.

This module only uses the standard library, so it works without the ``cli`` extra.
"""

import typing as T

import os
import json
from pathlib import Path

from .maker import Maker

CONFIG_FILENAME = "cookiecutter-maker.json"

PATH_FIELDS = ("dir_input", "dir_output", "dir_hooks")
LIST_FIELDS = ("include", "exclude", "no_render")

SAMPLE_CONFIG = {
    "dir_input": "./my_project",
    "dir_output": "./tmp",
    "parameters": [
        {
            "selector": ["my_project"],
            "name": "project_name",
            "default": "my_project",
            "prompt": "Your project name",
        },
        {
            "selector": ["0.1.1"],
            "name": "version",
            "default": "0.1.1",
        },
        {
            "selector": ["MIT"],
            "name": "license",
            "choice": ["MIT", "Apache-2.0", "Proprietary"],
        },
    ],
    "include": [],
    "exclude": [
        ".git",
        ".venv",
        "__pycache__",
        "*.pyc",
        "build",
        "dist",
    ],
    "no_render": [
        "*.jinja",
        "*.j2",
    ],
    "dir_hooks": None,
    "verbose": True,
    "overwrite": False,
}


def resolve_path(value: str | Path, base: Path) -> Path:
    """
    Expand ``~`` and resolve a relative path against ``base``.
    """
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = base.joinpath(path)
    return Path(os.path.normpath(path))


def normalize_list(value: str | list | tuple) -> list[str]:
    """
    Normalize a list-like command line value to a list of strings.

    ``".git,.venv"`` and ``[".git", ".venv"]`` both become ``[".git", ".venv"]``.

    Fire may also parse a value like ``--exclude=1`` into a non-string scalar.
    """
    if isinstance(value, (list, tuple)):
        return [str(item) for item in value]
    return [item.strip() for item in str(value).split(",") if item.strip()]


def find_config(
    config: str | Path | None = None,
    cwd: Path | None = None,
) -> Path | None:
    """
    Locate the config file.

    :param config: explicit config file path. Raise ``FileNotFoundError``
        if it doesn't exist.
    :param cwd: the directory to look for ``cookiecutter-maker.json`` when
        ``config`` is not given. Default to the current working directory.

    :returns: the absolute path of the config file, or ``None`` if ``config``
        is not given and there is no ``cookiecutter-maker.json`` in ``cwd``.
    """
    cwd = Path.cwd() if cwd is None else cwd
    if config is not None:
        path = resolve_path(config, cwd)
        if path.is_file() is False:
            raise FileNotFoundError(f"Config file {str(path)!r} does not exist!!")
        return path
    path = cwd.joinpath(CONFIG_FILENAME)
    if path.is_file():
        return path
    return None


def read_config(path: Path) -> dict[str, T.Any]:
    """
    Read the config file, resolving relative paths against its directory.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) is False:
        raise ValueError(f"Config file {str(path)!r} must be a JSON object!!")
    for key in PATH_FIELDS:
        if data.get(key) is not None:
            data[key] = str(resolve_path(data[key], path.parent))
    return data


def apply_overrides(
    data: dict[str, T.Any],
    overrides: dict[str, T.Any],
    cwd: Path | None = None,
) -> dict[str, T.Any]:
    """
    Return a new dict with non-``None`` command line values overriding ``data``.

    List values replace (not extend) the value from the config file.
    """
    cwd = Path.cwd() if cwd is None else cwd
    data = dict(data)
    for key, value in overrides.items():
        if value is None:
            continue
        if key in PATH_FIELDS:
            value = str(resolve_path(str(value), cwd))
        elif key in LIST_FIELDS:
            value = normalize_list(value)
        data[key] = value
    return data


def load_maker(
    config: str | Path | None = None,
    cwd: Path | None = None,
    **overrides,
) -> Maker:
    """
    Create a :class:`~cookiecutter_maker.maker.Maker` from the config file
    and the command line overrides. See the module docstring for precedence.

    :param config: explicit config file path, see :func:`find_config`.
    :param cwd: default to the current working directory.
    :param overrides: any :class:`~cookiecutter_maker.maker.Maker` field,
        ``None`` means "not provided".
    """
    cwd = Path.cwd() if cwd is None else cwd
    path_config = find_config(config=config, cwd=cwd)
    data = {} if path_config is None else read_config(path_config)
    data = apply_overrides(data, overrides, cwd=cwd)
    if "parameters" not in data:
        raise ValueError(
            "'parameters' is not defined, it can only be set in the config file, "
            "create one with 'cookiecutter-maker init' or pass '--config'."
        )
    return Maker.from_dict(data)


def write_sample_config(
    path: str | Path | None = None,
    overwrite: bool = False,
    cwd: Path | None = None,
) -> Path:
    """
    Write a sample ``cookiecutter-maker.json`` config file.

    :param path: where to write the config file,
        default to ``./cookiecutter-maker.json``.
    :param overwrite: whether to overwrite the existing file.
    """
    cwd = Path.cwd() if cwd is None else cwd
    path = cwd.joinpath(CONFIG_FILENAME) if path is None else resolve_path(path, cwd)
    if path.exists() and overwrite is False:
        raise FileExistsError(
            f"Config file {str(path)!r} already exists!! "
            f"Use overwrite=True to replace it."
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(SAMPLE_CONFIG, indent=4) + "\n", encoding="utf-8")
    return path
