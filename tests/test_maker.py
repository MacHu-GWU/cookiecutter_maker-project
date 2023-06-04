# -*- coding: utf-8 -*-

import os
import pytest
import shutil
from pathlib import Path
from cookiecutter_maker.maker import Maker

dir_here = Path(__file__).absolute().parent


class TestMaker:
    def test_preprocess_input_dir(self):
        with pytest.raises(FileNotFoundError):
            Maker._preprocess_input_dir(input_dir=dir_here.joinpath("not-exists"))

    def test_preprocess_output_dir(self):
        assert isinstance(
            Maker._preprocess_output_dir(output_dir=dir_here.joinpath("output")),
            Path,
        )

    def test_preprocess_mapper(self):
        with pytest.raises(ValueError):
            Maker._preprocess_mapper(mapper=[])

        invalid_mapper = [
            ("john", "name", "your_name"),
            ("john@email.com", "email", "your_email"),
        ]
        Maker._preprocess_mapper(
            mapper=invalid_mapper,
            ignore_mapper_error=True,
        )
        Maker._preprocess_mapper(
            mapper=invalid_mapper,
            skip_mapper_prompt=True,
        )

    def _test_do_we_ignore(self):
        maker = Maker.new(
            input_dir="/tmp/input/my_package-project",
            output_dir="/tmp/output",
            mapper=[
                ("my_package", "package_name", "this_is_my_package"),
            ],
            include=[
                "my_package/*",
                "template/*",
                "*.py",
                "*.png",
                "*.rst",
            ],
            exclude=[
                ".venv",
            ],
            _skip_validate=True,
        )
        assert (
            maker._do_we_ignore(
                Path(
                    "/tmp/input/my_package-project/my_package/__init__.py"
                ).relative_to(maker.input_dir),
                is_dir=False,
            )
            is False
        )
        assert (
            maker._do_we_ignore(
                Path("/tmp/input/my_package-project/README.rst").relative_to(
                    maker.input_dir
                ),
                is_dir=False,
            )
            is False
        )
        assert (
            maker._do_we_ignore(
                Path("/tmp/input/my_package-project/image.jpg").relative_to(
                    maker.input_dir
                ),
                is_dir=False,
            )
            is True
        )
        assert (
            maker._do_we_ignore(
                Path("/tmp/input/my_package-project/.venv").relative_to(
                    maker.input_dir
                ),
                is_dir=True,
            )
            is True
        )
        maker._templaterize_dir(Path("/tmp/input/my_package-project/.venv"))

    def _test_templaterize(self):
        print("")
        dir_input = dir_here.joinpath("my_package-project")
        dir_output = dir_here.joinpath("output")
        maker = Maker.new(
            input_dir=dir_input,
            output_dir=dir_output,
            mapper=[
                ("my_package", "package_name", "this_is_my_package"),
                ("john.doe@email.com", "author_email", "john.doe@email.com"),
                ("john.doe", "author_name", "john.doe"),
            ],
            include=None,
            exclude=[
                ".git-folder",
                ".venv-folder",
                ".coverage-file",
            ],
            no_render=[
                "*.tpl",
            ],
            overwrite=True,
            ignore_mapper_error=False,
            skip_mapper_prompt=True,
            debug=False,
        )
        maker.templaterize(cleanup_output_dir=True)

        assert maker.output_dir.joinpath(".git-folder").exists() is False
        assert maker.output_dir.joinpath(".venv-folder").exists() is False
        assert maker.output_dir.joinpath("test.txt").exists() is False

        assert maker.output_dir.joinpath("cookiecutter.json").exists() is True

        dir_project = maker.output_dir.joinpath(
            "{{ cookiecutter.package_name }}-project"
        )
        assert dir_project.exists() is True

        assert (
            dir_project.joinpath(
                "{{ cookiecutter.package_name }}", "__init__.py"
            ).exists()
            is True
        )
        assert dir_project.joinpath("template", "email.jinja").exists() is True
        assert dir_project.joinpath("template", "email.tpl").exists() is True
        assert dir_project.joinpath("python-icon.png").exists() is True
        assert dir_project.joinpath("README.rst").exists() is True

        assert (
            "This is my_package"
            in dir_project.joinpath("template", "email.jinja").read_text()
        )
        assert (
            "This is my_package"
            in dir_project.joinpath("template", "email.tpl").read_text()
        )

        with pytest.raises(FileExistsError):
            maker.overwrite = False
            maker.templaterize(cleanup_output_dir=False)

    def test(self):
        self._test_do_we_ignore()
        self._test_templaterize()


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
