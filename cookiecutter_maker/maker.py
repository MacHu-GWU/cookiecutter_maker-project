# -*- coding: utf-8 -*-

"""
This module provides the core functionality for converting an existing project
into a cookiecutter template. It handles file replacement, directory structure
transformation, and generation of cookiecutter.json configuration.

The main class is :class:`Maker`, which orchestrates the entire template conversion process.
"""

import typing as T

import glob
import json
import shutil
import dataclasses
from pathlib import Path
from functools import cached_property

from .str_replace import replace_double_curly_brackets
from .parameter import Parameter
from .parameter import replace_with_parameter
from .parameter import check_dataclass_kwargs
from .path_matcher import PathMatcher


@dataclasses.dataclass
class Maker:
    """
    Cookiecutter maker class for converting concrete projects into cookiecutter templates.

    :param dir_input: The directory you want to use as a seed project.
    :param dir_output: Where to place the generated template project.
    :param parameter: a list of :class:`~.cookiecutter_maker.parameter.Parameter`
        defining substitution rules.
    :param include: List of file path patterns to include from the input dir.
        If empty, we include all files and directories. If not empty, only
        the matched files are included, and only the directories containing
        included files are created.
    :param exclude: List of file path patterns to exclude from the input dir.
        If empty, we exclude nothing.
    :param no_render: List of file path patterns to copy without rendering.
        The matched files are listed one by one in ``_copy_without_render``
        of ``cookiecutter.json``, because cookiecutter matches this setting
        with ``fnmatch`` against the template path, not with the git-style
        patterns against the seed project path.
    :param dir_hooks: Optional directory containing cookiecutter hooks.
    :param verbose: Whether to print verbose output during processing
    :param overwrite: If True, delete the existing ``dir_output`` before
        generating the template. For safety, it only deletes an empty directory
        or a previously generated template (has ``cookiecutter.json``), and never
        deletes ``dir_input`` or its parents. If False, raise an error when
        ``dir_output`` already exists.
    """

    dir_input: Path = dataclasses.field()
    dir_output: Path = dataclasses.field()
    parameters: list[Parameter] = dataclasses.field()
    include: list[str] = dataclasses.field(default_factory=list)
    exclude: list[str] = dataclasses.field(default_factory=list)
    no_render: list[str] = dataclasses.field(default_factory=list)
    dir_hooks: Path | None = dataclasses.field(default=None)
    verbose: bool = dataclasses.field(default=True)
    overwrite: bool = dataclasses.field(default=False)

    def __post_init__(self):
        self._validate()
        # template paths (relative to dir_template) of the no_render files,
        # filled by make_template, see write_cookiecutter_json
        self._copy_without_render: list[str] = []

    def _validate(self):
        """
        Validate that parameters don't conflict with each other.
        """
        names = [param.name for param in self.parameters if param.in_cookiecutter_json]
        duplicates = sorted({name for name in names if names.count(name) > 1})
        if duplicates:
            raise ValueError(f"Duplicate parameter name(s): {duplicates}")
        selectors = [param.selector[0] for param in self.parameters]
        duplicates = sorted({sel for sel in selectors if selectors.count(sel) > 1})
        if duplicates:
            raise ValueError(
                f"Duplicate parameter selector(s): {duplicates}, "
                f"each string can only be replaced by one parameter."
            )

    @classmethod
    def from_dict(cls, data: dict[str, T.Any]) -> "Maker":
        """
        Create a :class:`Maker` from a JSON-compatible dict, for example the
        content of a ``cookiecutter-maker.json`` file.

        Path fields are converted to :class:`~pathlib.Path` as is, relative
        paths are NOT resolved here. Each item in ``parameters`` can be either
        a dict or a :class:`~cookiecutter_maker.parameter.Parameter` object.
        """
        check_dataclass_kwargs(cls, data)
        kwargs = dict(data)
        for key in ["dir_input", "dir_output", "dir_hooks"]:
            if kwargs.get(key) is not None:
                kwargs[key] = Path(kwargs[key])
        kwargs["parameters"] = [
            param if isinstance(param, Parameter) else Parameter.from_dict(param)
            for param in kwargs["parameters"]
        ]
        return cls(**kwargs)

    @cached_property
    def path_matcher(self) -> PathMatcher:
        """
        Create and return a :class:`~.cookiecutter_maker.path_matcher.PathMatcher`
        instance for filtering files and directories.
        """
        return PathMatcher.new(
            include=self.include,
            exclude=self.exclude,
            no_render=self.no_render,
        )

    @cached_property
    def dir_template(self) -> Path:
        """
        Determine the output template directory path.

        This creates the path for the project template folder with cookiecutter
        variables in the name, based on the original input directory name.
        """
        folder_name = replace_with_parameter(
            text=self.dir_input.name,
            param_list=self.parameters,
        )
        return self.dir_output.joinpath(folder_name)

    @cached_property
    def path_cookiecutter_json(self) -> Path:
        """
        Get the path for the ``cookiecutter.json`` configuration file.

        This file will contain the parameter definitions, default values,
        and other cookiecutter configuration options.
        """
        return self.dir_output.joinpath("cookiecutter.json")

    def _make_template_file(self, p_before: Path) -> Path | None:
        """
        Convert a file to a template in the output directory.

        :param p_before: the file path in the input directory.

        :returns: the file path in the output directory.
            If the file is ignored, then return None.
        """
        # Get the relative path from the input directory,
        # always use "/" as separator for pattern matching
        relpath = p_before.relative_to(self.dir_input).as_posix()

        # Check if this file should be included based on include/exclude rules
        if self.path_matcher.is_match(relpath) is False:
            return None

        # Apply parameter substitutions to the file path
        new_relpath = replace_with_parameter(
            text=relpath,
            param_list=self.parameters,
        )
        p_after = self.dir_template.joinpath(new_relpath)

        # Print processing information if verbose mode is enabled
        if self.verbose:
            print(f"from: {relpath}")
            print(f"  to: {p_after.relative_to(self.dir_output)}")

        # The parent directory is not created yet when include is set
        p_after.parent.mkdir(parents=True, exist_ok=True)

        # For files that should be copied without rendering, just copy as-is
        if self.path_matcher.is_render(relpath) is False:
            p_after.write_bytes(p_before.read_bytes())
            template_relpath = p_after.relative_to(self.dir_template).as_posix()
            self._copy_without_render.append(template_relpath)
            return p_after

        # Read the file content as bytes
        b = p_before.read_bytes()

        # Try to decode as text; if it fails, treat as binary
        try:
            text_content = b.decode("utf-8")
            text_content = p_before.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # For binary files, copy as-is without processing
            p_after.write_bytes(b)
            return p_after

        # For text files, process the content
        # 1. Escape any existing Jinja2/cookiecutter syntax
        text_content = replace_double_curly_brackets(text_content)
        # 2. Apply parameter substitutions
        text_content = replace_with_parameter(
            text=text_content,
            param_list=self.parameters,
        )
        # Write the processed content to the output file
        p_after.write_text(text_content, encoding="utf-8")
        return p_after

    def _make_template_dir(self, p_before: Path) -> Path | None:
        """
        Convert a directory to a template in the output directory.

        :param p_before: the directory path in the input directory.

        :returns: the directory path in the output directory.
            If the directory is ignored, then return None.
        """
        # Get the relative path from the input directory,
        # always use "/" as separator for pattern matching
        relpath = p_before.relative_to(self.dir_input).as_posix()
        is_root = relpath == "."

        # Directories are only filtered by exclude rules, include rules are
        # applied to files, otherwise ``include=["*.py"]`` would skip the
        # directories that contain the python files. The root is always processed.
        if is_root is False and self.path_matcher.is_excluded(relpath):
            return None

        # Apply parameter substitutions to the directory path
        new_relpath = replace_with_parameter(
            text=relpath,
            param_list=self.parameters,
        )
        p_after = self.dir_template.joinpath(new_relpath)

        # Print processing information if verbose mode is enabled
        if self.verbose:
            print(f"from: {relpath}")
            print(f"  to: {p_after.relative_to(self.dir_output)}")

        # Create the directory (and parent directories if needed).
        # When include is set, directories are created by the included files,
        # so we don't end up with empty directories.
        if is_root or len(self.include) == 0:
            p_after.mkdir(parents=True, exist_ok=True)
        return p_after

    def _make_template(
        self,
        dir_src: Path,
    ):
        """
        Recursively convert a directory to a template.

        This method walks through the directory tree and processes each item:

        - For directories, it calls :meth:`_make_template_dir`
        - For files, it calls :meth:`_make_template_file`
        - Skips items that are not files or directories
        """
        p_after = self._make_template_dir(dir_src)

        # If this directory is ignored, skip processing its contents
        if p_after is None:
            return

        # Process each item in the directory
        dir_output = self.dir_output.resolve()
        for p in dir_src.iterdir():
            if p.is_dir():
                # Skip the output directory if it is inside the input directory,
                # otherwise we keep copying the output into itself
                if p.resolve() == dir_output:
                    continue
                # Recursively process subdirectories
                self._make_template(p)
            elif p.is_file():
                # Process files
                self._make_template_file(p)
            else:  # pragma: no cover
                # Skip any items that are neither files nor directories
                # (like symbolic links, device files, etc.)
                pass

    def readiness_check(self):
        """
        Perform pre-execution checks to ensure the operation can proceed.
        """
        # Check if input directory exists
        if self.dir_input.exists() is False:
            raise FileNotFoundError(
                f"Input directory {self.dir_input!r} does not exist!!"
            )

        # Check if output directory already exists
        if self.dir_output.exists():
            if self.overwrite is False:
                raise FileExistsError(
                    f"Output directory {self.dir_output!r} already exists!! "
                    f"Use overwrite=True to delete it before generating the template."
                )
            if self.dir_output.is_dir() is False:
                raise FileExistsError(
                    f"Output path {self.dir_output!r} exists and is not a directory!!"
                )
            # Never delete the seed project itself
            dir_input = self.dir_input.resolve()
            dir_output = self.dir_output.resolve()
            if dir_output == dir_input or dir_output in dir_input.parents:
                raise ValueError(
                    f"Output directory {self.dir_output!r} is the input directory "
                    f"or one of its parents, refuse to overwrite it!!"
                )
            # Only delete an empty directory or a previously generated template,
            # in case dir_output is mistakenly set to something like "." or "~"
            is_empty = next(self.dir_output.iterdir(), None) is None
            if (is_empty or self.path_cookiecutter_json.exists()) is False:
                raise ValueError(
                    f"Output directory {self.dir_output!r} is not empty and doesn't "
                    f"look like a generated template (no cookiecutter.json), "
                    f"refuse to overwrite it!!"
                )

        # If hooks directory is specified, check if it exists
        if self.dir_hooks is not None:
            if self.dir_hooks.exists() is False:
                raise FileNotFoundError(
                    f"Hooks directory {self.dir_hooks!r} does not exist!!"
                )

    def _print_parameters(self):
        """
        Print the parameters and their placeholders.

        This is a debugging helper method that prints each parameter's
        selector and the corresponding placeholder that will replace it.
        Only prints if verbose mode is enabled.
        """
        if self.verbose:
            print("---------- parameters ----------")
            for param in self.parameters:
                print(f"- {param.selector[0]!r} -> {param.placeholder!r}")

    def write_cookiecutter_json(self):
        """
        Create the ``cookiecutter.json`` configuration file.

        See https://cookiecutter.readthedocs.io/en/stable/tutorials/tutorial2.html#step-2-create-cookiecutter-json
        """
        # Start with an empty dictionary
        data = {}
        prompts = {}
        # Add each parameter's configuration
        for param in self.parameters:
            if param.in_cookiecutter_json:
                key, value = param.to_cookiecutter_key_value()
                data[key] = value
                if param.prompt:
                    prompts[key] = param.prompt

        if prompts:
            data["__prompts__"] = prompts

        # List the no_render files by their exact template path, escaped for fnmatch
        if self._copy_without_render:
            data["_copy_without_render"] = [
                glob.escape(path) for path in sorted(self._copy_without_render)
            ]

        # Force to use POSIX line endings
        data["_new_lines"] = "\n"

        # Write the JSON file with nice formatting
        self.path_cookiecutter_json.write_text(
            json.dumps(data, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

    def copy_hooks(self):
        """
        Copy the hooks directory to the output template if specified.

        `Cookiecutter hooks <https://cookiecutter.readthedocs.io/en/stable/advanced/hooks.html>`_
        are scripts that run before or after template generation.
        If a hooks directory is specified, it is copied to the output template.
        """
        if self.dir_hooks is None:
            return
        dir_hooks_output = self.dir_output.joinpath("hooks")
        shutil.copytree(src=self.dir_hooks, dst=dir_hooks_output)

    def make_template(self):
        """
        Execute the full template generation process.
        """
        # Perform pre-execution validation
        self.readiness_check()
        # Remove the existing output directory if overwrite is enabled
        if self.overwrite and self.dir_output.exists():
            shutil.rmtree(self.dir_output)
        # Print parameter information if verbose
        self._print_parameters()
        # Print processing start message if verbose
        if self.verbose:
            print("---------- make template ----------")
        # Process the input directory recursively
        self._copy_without_render = []
        self._make_template(dir_src=self.dir_input)
        # Generate the cookiecutter.json configuration file
        self.write_cookiecutter_json()
        # Copy hooks if specified
        self.copy_hooks()
