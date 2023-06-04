# -*- coding: utf-8 -*-

import typing as T

import json
import shutil
import dataclasses
from pathlib import Path
from collections import OrderedDict

from .exc import MapperValidationError
from .strutils import validate_mapper, replace


@dataclasses.dataclass
class Maker:
    """
    Cookiecutter maker.
    """

    input_dir: Path = dataclasses.field()
    output_dir: Path = dataclasses.field()
    mapper: T.List[T.Tuple[str, str, str]] = dataclasses.field()
    processed_mapper: T.List[T.Tuple[str, str]] = dataclasses.field()
    include: T.List[str] = dataclasses.field(default_factory=list)
    exclude: T.List[str] = dataclasses.field(default_factory=list)
    no_render: T.List[str] = dataclasses.field(default_factory=list)
    overwrite: T.Optional[bool] = dataclasses.field(default=False)
    debug: bool = dataclasses.field(default=False)

    # ---
    _after_dir: T.Optional[Path] = dataclasses.field(default=None)

    @classmethod
    def new(
        cls,
        input_dir: T.Union[str, Path],
        output_dir: T.Union[str, Path],
        mapper: T.List[T.Tuple[str, str, str]],
        include: T.Optional[T.List[str]] = None,
        exclude: T.Optional[T.List[str]] = None,
        no_render: T.Optional[T.List[str]] = None,
        overwrite: bool = False,
        ignore_mapper_error: bool = False,
        skip_mapper_prompt: bool = False,
        debug: bool = False,
        _skip_validate: bool = False,
    ):
        """
        Create a new :class:`Maker` instance.

        :param input_dir: the directory you want to templaterize.
        :param output_dir: where to put the generated template project?
        :param mapper: a list of tuple. each tuple include three items. 1 is the
            concrete string you want to replace, 2 is the parameter name, 3 is the
            default value for cookiecutter to prompt user to input.
        :param include: list of file path pattern that we include from the input dir
        :param exclude: list of file path pattern that we exclude from the input dir
        :param no_render: list of file path pattern that we copy it without
            rendering (as it is)
        :param overwrite: allow overwrite the output dir if already exists
        :param ignore_mapper_error: ignore mapper validation error
        :param skip_mapper_prompt: skip prompt asking you to confirm the mapper
        :param debug: if True, show debug info
        :param _skip_validate: internal use only, don't set this parameter.
        """
        maker = cls(
            input_dir=cls._preprocess_input_dir(input_dir, _skip_validate),
            output_dir=cls._preprocess_output_dir(output_dir),
            mapper=mapper,
            processed_mapper=cls._preprocess_mapper(
                mapper,
                ignore_mapper_error=ignore_mapper_error,
                skip_mapper_prompt=skip_mapper_prompt,
            ),
            include=cls._preprocess_include(include),
            exclude=cls._preprocess_exclude(exclude),
            no_render=cls._preprocess_no_render(no_render),
            overwrite=overwrite,
            debug=debug,
        )
        maker._after_dir = maker.output_dir.joinpath(
            replace(maker.input_dir.name, maker.processed_mapper)
        )
        return maker

    # --------------------------------------------------------------------------
    # preprocess arguments
    # --------------------------------------------------------------------------
    @classmethod
    def _preprocess_input_dir(
        cls,
        input_dir: T.Union[str, Path],
        _skip_validate: bool = False,
    ) -> Path:
        if isinstance(input_dir, str):
            input_dir = Path(input_dir)
        if _skip_validate is False:
            if input_dir.exists() is False:
                raise FileNotFoundError(
                    f"Input directory {input_dir!r} does not exist!!"
                )
        return input_dir

    @classmethod
    def _preprocess_output_dir(
        cls,
        output_dir: T.Union[str, Path],
    ) -> Path:
        if isinstance(output_dir, str):
            output_dir = Path(output_dir)
        return output_dir

    @classmethod
    def _preprocess_mapper(
        cls,
        mapper: T.List[T.Tuple[str, str, str]],
        ignore_mapper_error: bool = False,
        skip_mapper_prompt: bool = False,
    ) -> T.List[T.Tuple[str, str]]:
        if len(mapper) == 0:
            raise ValueError("mapper cannot be empty")

        dict_mapper = OrderedDict()
        # handle {{ and }} string
        dict_mapper["{{"] = "{% raw %}{{{% endraw %}"
        dict_mapper["}}"] = "{% raw %}}}{% endraw %}"
        for before, after, _ in mapper:
            dict_mapper[before] = f"{{{{ cookiecutter.{after} }}}}"
        list_mapper = [(k, v) for k, v in dict_mapper.items()]

        try:
            validate_mapper(list_mapper)
        except MapperValidationError as e:
            if ignore_mapper_error:
                return list_mapper
            if skip_mapper_prompt:
                return list_mapper
            else:  # pragma: no cover
                answer = input(
                    f"{e}\n"
                    f"I suggest to put substring later than the super string in mapper\n"
                    f"Are you sure to continue? [y/n]: "
                )
                if answer.lower() in ["y", "yes"]:
                    return list_mapper
                else:
                    raise e
        except Exception as e:  # pragma: no cover
            raise e
        return list_mapper

    @classmethod
    def _preprocess_include(
        cls,
        include: T.Optional[T.List[str]],
    ) -> T.List[str]:  # pragma: no cover
        if include is None:
            include = list()
        return include

    @classmethod
    def _preprocess_exclude(
        cls,
        exclude: T.Optional[T.List[str]],
    ) -> T.List[str]:  # pragma: no cover
        if exclude is None:
            exclude = list()
        return exclude

    @classmethod
    def _preprocess_no_render(
        cls,
        no_render: T.Optional[T.List[str]],
    ) -> T.List[str]:  # pragma: no cover
        if no_render is None:
            no_render = list()
        # *.jinja template itself is a template file,
        # most likely you don't want to render it.
        no_render.append("*.jinja")
        return no_render

    def _do_we_ignore(
        self,
        relpath: Path,
        is_dir: bool
    ) -> bool:
        """
        Based on the include and exclude pattern, do we ignore this file?

        It has to match include rule and not match exclude rule.

        If include is empty, it considered as "match include rule".

        If exclude is empty, it considered as "not match exclude rule".
        """
        if is_dir:
            match_include = True
        else:
            if len(self.include):
                match_include = False
                for pattern in self.include:
                    if relpath.match(pattern):
                        match_include = True
                        break
            else: # pragma: no cover
                match_include = True

        match_exclude = False
        for pattern in self.exclude:
            if relpath.match(pattern):
                match_exclude = True
                break

        if match_include:
            return match_exclude
        else:
            return True

    def _do_we_render(self, relpath: Path) -> bool:
        for pattern in self.no_render:
            if relpath.match(pattern):
                return False
        return True

    def _templaterize_file(self, p_before: Path) -> T.Optional[Path]:
        """
        Create a templaterized file in the output directory.
        """
        relpath = p_before.relative_to(self.input_dir)

        if self._do_we_ignore(relpath, is_dir=False):
            return None

        new_relpath = replace(str(relpath), self.processed_mapper)
        p_after = self._after_dir.joinpath(new_relpath)

        if p_after.exists():
            if self.overwrite is False:
                raise FileExistsError(
                    f"File already exists: {p_after!r}! maybe use 'overwrite = True'!"
                )

        if self.debug:
            # print(f"{str(p_before):<160} -> {str(p_after)}")
            print(f"{p_before} -> {p_after}")

        if self._do_we_render(relpath) is False:
            p_after.write_bytes(p_before.read_bytes())
            return p_after

        # handle binary content files
        b = p_before.read_bytes()

        try:
            s = b.decode("utf-8")
        except UnicodeDecodeError:
            # copy binary file as it is
            p_after.write_bytes(b)
            return p_after

        text = replace(s, self.processed_mapper)
        p_after.write_text(text)
        return p_after

    def _templaterize_dir(self, p_before: Path) -> T.Optional[Path]:
        """
        Create a templaterized directory in the output directory (empty folder).
        """
        relpath = p_before.relative_to(self.input_dir)

        if self._do_we_ignore(relpath, is_dir=True):
            return None

        new_relpath = replace(str(relpath), self.processed_mapper)
        p_after = self._after_dir.joinpath(new_relpath)
        if self.debug:
            # print(f"{str(p_before):<160} -> {str(p_after)}")
            print(f"{p_before} -> {p_after}")
        p_after.mkdir(parents=True, exist_ok=True)
        return p_after

    def _templaterize(
        self,
        dir_src: Path,
    ):
        """
        Recursively templaterize a directory.
        """
        p_after = self._templaterize_dir(dir_src)

        if (
            p_after is None
        ):  # if this dir is ignored, then no need to work on sub-folders and files
            return

        for p in dir_src.iterdir():
            if p.is_dir():
                self._templaterize(p)
            elif p.is_file():
                self._templaterize_file(p)
            else:  # pragma: no cover
                pass

        path_cookiecutter_json = self.output_dir.joinpath("cookiecutter.json")
        cookiecutter_json_data = dict()
        for _, parameter_name, concrete_string in self.mapper:
            cookiecutter_json_data[parameter_name] = concrete_string
        path_cookiecutter_json.write_text(json.dumps(cookiecutter_json_data, indent=4))

    def templaterize(
        self,
        cleanup_output_dir: bool = False,
    ):
        if cleanup_output_dir:
            shutil.rmtree(self.output_dir, ignore_errors=True)
        self._templaterize(dir_src=self.input_dir)
