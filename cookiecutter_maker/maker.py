# -*- coding: utf-8 -*-
import shutil
import typing as T
import os
import dataclasses
from pathlib import Path
from collections import OrderedDict

from .strutils import replace


@dataclasses.dataclass
class Maker:
    input_dir: Path = dataclasses.field()
    output_dir: Path = dataclasses.field()
    mapper: T.List[T.Tuple[str, str]] = dataclasses.field()
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
        mapper: T.List[T.Tuple[str, str]],
        include: T.Optional[T.List[str]] = None,
        exclude: T.Optional[T.List[str]] = None,
        no_render: T.Optional[T.List[str]] = None,
        overwrite: bool = False,
        debug: bool = False,
        _skip_validate: bool = False,
    ):
        maker = cls(
            input_dir=cls._preprocess_input_dir(input_dir, _skip_validate),
            output_dir=cls._preprocess_output_dir(output_dir),
            mapper=cls._preprocess_mapper(mapper),
            include=cls._preprocess_include(include),
            exclude=cls._preprocess_exclude(exclude),
            no_render=cls._preprocess_no_render(no_render),
            overwrite=overwrite,
            debug=debug,
        )
        maker._after_dir = maker.output_dir.joinpath(
            replace(maker.input_dir.name, maker.mapper)
        )
        return maker

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
                raise ValueError(f"Input directory {input_dir!r} does not exist!!")
        return input_dir

    @classmethod
    def _preprocess_output_dir(cls, output_dir: T.Union[str, Path]) -> Path:
        if isinstance(output_dir, str):
            output_dir = Path(output_dir)
        return output_dir

    @classmethod
    def _preprocess_mapper(
        cls,
        mapper: T.List[T.Tuple[str, str]],
    ) -> T.List[T.Tuple[str, str]]:
        if len(mapper) == 0:
            raise ValueError("mapper cannot be empty")
        dict_mapper = OrderedDict()
        dict_mapper["{{"] = "{% raw %}{{{% endraw %}"
        dict_mapper["}}"] = "{% raw %}}}{% endraw %}"
        for before, after in mapper:
            dict_mapper[before] = f"{{{{ cookiecutter.{after} }}}}"
        list_mapper = [(k, v) for k, v in dict_mapper.items()]
        return list_mapper

    @classmethod
    def _preprocess_include(
        cls,
        include: T.Optional[T.List[str]],
    ) -> T.List[str]:
        if include is None:
            include = list()
        return include

    @classmethod
    def _preprocess_exclude(
        cls,
        exclude: T.Optional[T.List[str]],
    ) -> T.List[str]:
        if exclude is None:
            exclude = list()
        return exclude

    @classmethod
    def _preprocess_no_render(
        cls,
        no_render: T.Optional[T.List[str]],
    ) -> T.List[str]:
        if no_render is None:
            no_render = list()
        no_render.append("*.jinja")
        return no_render

    def do_we_ignore(self, relpath: Path) -> bool:
        if len(self.include):
            match_include = False
            for pattern in self.include:
                if relpath.match(pattern):
                    match_include = True
                    break
        else:
            match_include = True

        match_exclude = False
        for pattern in self.exclude:
            if relpath.match(pattern):
                match_exclude = True
                break

        if match_include:
            return match_exclude
        else:
            return False

    def do_we_render(self, relpath: Path) -> bool:
        for pattern in self.no_render:
            if relpath.match(pattern):
                return False
        return True

    def templaterize_file(self, p_before: Path) -> T.Optional[Path]:
        relpath = p_before.relative_to(self.input_dir)

        if self.do_we_ignore(relpath):
            return None

        new_relpath = replace(str(relpath), self.mapper)
        p_after = self._after_dir.joinpath(new_relpath)

        if p_after.exists():
            if self.overwrite is False:
                raise ValueError(
                    f"File already exists: {p_after!r}! maybe use 'overwrite = True'!"
                )

        if self.debug:
            print(f"{str(p_before):<160} -> {str(p_after)}")

        if self.do_we_render(relpath) is False:
            p_after.write_bytes(p_before.read_bytes())
            return p_after

        try:
            b = p_before.read_bytes()
            s = b.decode("utf-8")
        except UnicodeDecodeError:
            p_after.write_bytes(b)
            return p_after

        text = replace(s, self.mapper)
        p_after.write_text(text)
        return p_after

    def templaterize_dir(self, p_before: Path) -> T.Optional[Path]:
        relpath = p_before.relative_to(self.input_dir)

        if self.do_we_ignore(relpath):
            return None

        new_relpath = replace(str(relpath), self.mapper)
        p_after = self._after_dir.joinpath(new_relpath)
        if self.debug:
            print(f"{str(p_before):<160} -> {str(p_after)}")
        p_after.mkdir(parents=True, exist_ok=True)
        return p_after

    def _templaterize(
        self,
        dir_src: Path,
    ):
        p_after = self.templaterize_dir(dir_src)

        if (
            p_after is None
        ):  # if this dir is ignored, then no need to work on subfolders and files
            return

        for p in dir_src.iterdir():
            if p.is_dir():
                self._templaterize(p)
            elif p.is_file():
                self.templaterize_file(p)
            else:
                pass

    def templaterize(self):
        self._templaterize(dir_src=self.input_dir)
