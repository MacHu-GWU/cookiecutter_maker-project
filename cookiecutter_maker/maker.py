# -*- coding: utf-8 -*-

"""
This module provides the core functionality for converting an existing project
into a cookiecutter template. It handles file replacement, directory structure
transformation, and generation of cookiecutter.json configuration.

The main class is :class:`Maker`, which orchestrates the entire template conversion process.
"""

import typing as T

import json
import shutil
import dataclasses
from pathlib import Path
from functools import cached_property

from .str_replace import replace_double_curly_brackets
from .parameter import Parameter, replace_with_parameter
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
        If empty, we include all files and directories.
    :param exclude: List of file path patterns to exclude from the input dir.
        If empty, we exclude nothing.
    :param no_render: List of file path patterns to copy without rendering.
    :param dir_hooks: Optional directory containing cookiecutter hooks.
    :param verbose: Whether to print verbose output during processing
    """

    dir_input: Path = dataclasses.field()
    dir_output: Path = dataclasses.field()
    parameters: list[Parameter] = dataclasses.field()
    include: list[str] = dataclasses.field(default_factory=list)
    exclude: list[str] = dataclasses.field(default_factory=list)
    no_render: list[str] = dataclasses.field(default_factory=list)
    dir_hooks: T.Optional[Path] = dataclasses.field(default=None)
    verbose: bool = dataclasses.field(default=True)

    def __post_init__(self):
        pass

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

    def _make_template_file(self, p_before: Path) -> T.Optional[Path]:
        """
        Convert a file to a template in the output directory.

        :param p_before: the file path in the input directory.

        :returns: the file path in the output directory.
            If the file is ignored, then return None.
        """
        # Get the relative path from the input directory
        relpath = p_before.relative_to(self.dir_input)

        # Check if this file should be included based on include/exclude rules
        if self.path_matcher.is_match(str(relpath)) is False:
            return None

        # Apply parameter substitutions to the file path
        new_relpath = replace_with_parameter(
            text=str(relpath),
            param_list=self.parameters,
        )
        p_after = self.dir_template.joinpath(new_relpath)

        # Print processing information if verbose mode is enabled
        if self.verbose:
            print(f"from: {p_before.relative_to(self.dir_input)}")
            print(f"  to: {p_after.relative_to(self.dir_output)}")

        # For files that should be copied without rendering, just copy as-is
        if self.path_matcher.is_render(str(relpath)) is False:
            p_after.write_bytes(p_before.read_bytes())
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

    def _make_template_dir(self, p_before: Path) -> T.Optional[Path]:
        """
        Convert a directory to a template in the output directory.

        :param p_before: the directory path in the input directory.

        :returns: the directory path in the output directory.
            If the directory is ignored, then return None.
        """
        # Get the relative path from the input directory
        relpath = p_before.relative_to(self.dir_input)

        # Check if this directory should be included based on include/exclude rules
        if self.path_matcher.is_match(str(relpath)) is False:
            return None

        # Apply parameter substitutions to the directory path
        new_relpath = replace_with_parameter(
            text=str(relpath),
            param_list=self.parameters,
        )
        p_after = self.dir_template.joinpath(new_relpath)

        # Print processing information if verbose mode is enabled
        if self.verbose:
            print(f"from: {p_before.relative_to(self.dir_input)}")
            print(f"  to: {p_after.relative_to(self.dir_output)}")

        # Create the directory (and parent directories if needed)
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
        for p in dir_src.iterdir():
            if p.is_dir():
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
            raise FileExistsError(
                f"Output directory {self.dir_output!r} already exists!!"
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

        # If no_render patterns are specified, add them to the config
        if self.no_render:
            data["_copy_without_render"] = self.no_render

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
        # Print parameter information if verbose
        self._print_parameters()
        # Print processing start message if verbose
        if self.verbose:
            print("---------- make template ----------")
        # Process the input directory recursively
        self._make_template(dir_src=self.dir_input)
        # Generate the cookiecutter.json configuration file
        self.write_cookiecutter_json()
        # Copy hooks if specified
        self.copy_hooks()
