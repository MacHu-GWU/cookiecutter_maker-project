# -*- coding: utf-8 -*-

import os
import pytest
from pathlib import Path
from cookiecutter_maker.maker import Maker

dir_here = Path(__file__).absolute().parent


class TestMaker:
    def test_do_we_ignore(self):
        maker = Maker.new(
            input_dir="/tmp/input/my_package-project",
            output_dir="/tmp/output",
            mapper=[
                ("my_package", "package_name"),
            ],
            include=[],
            exclude=[
                ".venv",
            ],
            _skip_validate=True,
        )
        assert (
            maker.do_we_ignore(
                Path("/tmp/input/my_package-project/.venv").relative_to(maker.input_dir)
            )
            is True
        )
        maker.templaterize_dir(Path("/tmp/input/my_package-project/.venv"))

    def test_templaterize(self):
        maker = Maker.new(
            input_dir=dir_here.joinpath("my_package-project"),
            output_dir=dir_here.joinpath("output"),
            mapper=[
                ("my_package", "package_name"),
            ],
            include=[],
            exclude=[
                ".git-folder",
                ".venv-folder",
                ".coverage-file",
            ],
            debug=True,
        )
        maker.templaterize()


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
