# -*- coding: utf-8 -*-

"""
Command line interface, powered by `Python Fire <https://github.com/google/python-fire>`_.

Fire is an optional dependency, install it with ``pip install "cookiecutter-maker[cli]"``,
or run without installing::

    uvx --from "cookiecutter-maker[cli]" cookiecutter-maker make

All the logic lives in :mod:`cookiecutter_maker.config`, this module only
exposes it as commands.
"""

import sys

from . import __version__
from .config import load_maker
from .config import write_sample_config


class Command:
    """
    Convert a concrete project into a cookiecutter template.

    Run ``cookiecutter-maker init`` to create a sample ``cookiecutter-maker.json``,
    edit it, then run ``cookiecutter-maker make``.
    """

    def make(
        self,
        config: str | None = None,
        dir_input: str | None = None,
        dir_output: str | None = None,
        dir_hooks: str | None = None,
        include: str | list[str] | None = None,
        exclude: str | list[str] | None = None,
        no_render: str | list[str] | None = None,
        verbose: bool | None = None,
        overwrite: bool | None = None,
    ):
        """
        Generate the cookiecutter template.

        Command line arguments take precedence over the config file.
        Arguments not provided fall back to the config file.

        :param config: config file path, default to ./cookiecutter-maker.json if exists.
        :param dir_input: the seed project directory.
        :param dir_output: where to write the generated template.
        :param dir_hooks: optional cookiecutter hooks directory.
        :param include: file path patterns to include, e.g. "src,tests" or '["src","tests"]'.
            Replaces the value in the config file.
        :param exclude: file path patterns to exclude, same format as include.
        :param no_render: file path patterns to copy without rendering, same format as include.
        :param verbose: print verbose output, use --verbose / --noverbose.
        :param overwrite: delete the existing dir_output first, use --overwrite / --nooverwrite.
        """
        maker = load_maker(
            config=config,
            dir_input=dir_input,
            dir_output=dir_output,
            dir_hooks=dir_hooks,
            include=include,
            exclude=exclude,
            no_render=no_render,
            verbose=verbose,
            overwrite=overwrite,
        )
        maker.make_template()
        print(f"Template is generated at: {maker.dir_output}")

    def init(
        self,
        path: str | None = None,
        overwrite: bool = False,
    ):
        """
        Create a sample config file.

        :param path: where to write the config file, default to ./cookiecutter-maker.json.
        :param overwrite: overwrite the existing config file.
        """
        path = write_sample_config(path=path, overwrite=overwrite)
        print(f"Config file is created at: {path}")

    def version(self):
        """
        Print the cookiecutter_maker version.
        """
        print(__version__)


def main():
    try:
        import fire
    except ImportError:  # pragma: no cover
        print(
            "The cookiecutter-maker CLI requires the 'cli' extra, install it with:\n"
            '    pip install "cookiecutter-maker[cli]"\n'
            "or run it with:\n"
            '    uvx --from "cookiecutter-maker[cli]" cookiecutter-maker',
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        fire.Fire(Command(), name="cookiecutter-maker")
    except (FileNotFoundError, FileExistsError, ValueError) as e:
        # json.JSONDecodeError is a subclass of ValueError
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
