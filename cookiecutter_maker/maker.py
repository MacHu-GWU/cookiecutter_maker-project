# -*- coding: utf-8 -*-

import typing as T

import json
import shutil
import dataclasses
from pathlib import Path
from collections import OrderedDict
from functools import cached_property

from .str_replace import replace_with_placeholders, replace_double_curly_brackets
from .parameter import Parameter, replace_with_parameter
from .path_matcher import PathMatcher
from .exc import MapperValidationError


@dataclasses.dataclass
class Maker:
    """
    Cookiecutter maker.

    :param dir_input: the directory you want to use as a seed.
    :param dir_output: where to put the generated template project.
    :param parameter: a list of :class:`~.cookiecutter_maker.parameter.Parameter`.
    :param include: list of file path pattern that we include from the input dir
        if empty, we include all files and directories.
    :param exclude: list of file path pattern that we exclude from the input dir
    :param no_render: list of file path pattern that we copy it without
        rendering (as it is)
    :param overwrite: allow overwrite the output dir if already exists
    :param ignore_mapper_error: ignore mapper validation error
    :param skip_mapper_prompt: skip prompt asking you to confirm the mapper
    :param debug: if True, show debug info
    :param _skip_validate: internal use only, don't set this parameter.
    """

    dir_input: Path = dataclasses.field()
    dir_output: Path = dataclasses.field()
    parameters: list[Parameter] = dataclasses.field()
    include: list[str] = dataclasses.field(default_factory=list)
    exclude: list[str] = dataclasses.field(default_factory=list)
    no_render: list[str] = dataclasses.field(default_factory=list)
    verbose: bool = dataclasses.field(default=True)

    def _print(self):
        if self.verbose:
            print("---------- parameters ----------")
            for param in self.parameters:
                print(f"- {param.selector[0]!r} -> {param.placeholder!r}")

    def __post_init__(self):
        self._print()

    @cached_property
    def path_matcher(self) -> PathMatcher:
        return PathMatcher.new(
            include=self.include,
            exclude=self.exclude,
            no_render=self.no_render,
        )

    @cached_property
    def dir_template(self) -> Path:
        folder_name = replace_with_parameter(
            text=self.dir_input.name,
            param_list=self.parameters,
        )
        return self.dir_output.joinpath(folder_name)

    @cached_property
    def path_cookiecutter_json(self) -> Path:
        return self.dir_output.joinpath("cookiecutter.json")

    # def _do_we_ignore(self, relpath: Path, is_dir: bool) -> bool:
    #     """
    #     Based on the include and exclude pattern, do we ignore this file?
    #
    #     It has to match include rule and not match exclude rule.
    #
    #     If include is empty, it considered as "match include rule".
    #
    #     If exclude is empty, it considered as "not match exclude rule".
    #     """
    #     if is_dir:
    #         match_include = True
    #     else:
    #         if len(self.include):
    #             match_include = False
    #             for pattern in self.include:
    #                 if relpath.match(pattern):
    #                     match_include = True
    #                     break
    #         else:  # pragma: no cover
    #             match_include = True
    #
    #     match_exclude = False
    #     for pattern in self.exclude:
    #         if relpath.match(pattern):
    #             match_exclude = True
    #             break
    #
    #     if match_include:
    #         return match_exclude
    #     else:
    #         return True

    def _make_template_file(self, p_before: Path) -> T.Optional[Path]:
        """
        Convert a file to a template in the output directory.

        :param p_before: the file path in the input directory.

        :returns: the file path in the output directory.
            If the file is ignored, then return None.
        """
        relpath = p_before.relative_to(self.dir_input)

        if self.path_matcher.is_match(str(relpath)) is False:
            return None

        new_relpath = replace_with_parameter(
            text=str(relpath),
            param_list=self.parameters,
        )
        p_after = self.dir_template.joinpath(new_relpath)

        if self.verbose:
            print(f"from: {p_before}")
            print(f"  to: {p_after}")

        if self.path_matcher.is_render(str(relpath)) is False:
            p_after.write_bytes(p_before.read_bytes())
            return p_after

        # handle binary content files
        b = p_before.read_bytes()

        try:
            text_content = b.decode("utf-8")
        except UnicodeDecodeError:
            # copy binary file as it is
            p_after.write_bytes(b)
            return p_after

        text_content = replace_double_curly_brackets(text_content)
        text_content = replace_with_parameter(
            text=text_content,
            param_list=self.parameters,
        )
        p_after.write_text(text_content, encoding="utf-8")
        return p_after

    def _make_template_dir(self, p_before: Path) -> T.Optional[Path]:
        """
        Convert a directory to a template in the output directory.

        :param p_before: the directory path in the input directory.

        :returns: the directory path in the output directory.
            If the directory is ignored, then return None.
        """
        relpath = p_before.relative_to(self.dir_input)

        if self.path_matcher.is_match(str(relpath)) is False:
            return None

        new_relpath = replace_with_parameter(
            text=str(relpath),
            param_list=self.parameters,
        )
        p_after = self.dir_template.joinpath(new_relpath)
        if self.verbose:
            print(f"from: {p_before}")
            print(f"  to: {p_after}")
        p_after.mkdir(parents=True, exist_ok=True)
        return p_after

    def _make_template(
        self,
        dir_src: Path,
    ):
        """
        Recursively convert a directory to a template.
        """
        p_after = self._make_template_dir(dir_src)
        # if this dir is ignored, then no need to work on sub-folders and files
        if p_after is None:
            return

        for p in dir_src.iterdir():
            if p.is_dir():
                self._make_template(p)
            elif p.is_file():
                self._make_template_file(p)
            else:  # pragma: no cover
                pass

        # cookiecutter_json_data = dict()
        # for _, parameter_name, concrete_string in self.mapper:
        #     cookiecutter_json_data[parameter_name] = concrete_string
        # path_cookiecutter_json.write_text(json.dumps(cookiecutter_json_data, indent=4))

    def readiness_check(self):
        if self.dir_input.exists() is False:
            raise FileNotFoundError(
                f"Input directory {self.dir_input!r} does not exist!!"
            )
        if self.dir_output.exists():
            raise FileExistsError(
                f"Output directory {self.dir_output!r} already exists!!"
            )

    def write_cookiecutter_json(self):
        data = {param.name: param.default for param in self.parameters}
        for param in self.parameters:
            key, value = param.to_cookiecutter_key_value()
            data[key] = value
        self.path_cookiecutter_json.write_text(
            json.dumps(data, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

    def make_template(self):
        self.readiness_check()
        self._make_template(dir_src=self.dir_input)
        self.write_cookiecutter_json()
