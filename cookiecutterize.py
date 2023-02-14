# -*- coding: utf-8 -*-

from pathlib import Path
from cookiecutter_maker.maker import Maker

dir_tmp: Path = Path(__file__).absolute().parent.joinpath("tmp")
dir_tmp.mkdir(parents=True, exist_ok=True)

maker = Maker.new(
    input_dir="/path-to-input-dir/my_awesome_project",
    output_dir=dir_tmp,
    mapper=[
        ("my_awesome_project", "package_name"),
    ],
    include=[],
    exclude=[
        # dir
        ".venv",
        ".pytest_cache",
        ".git",
        ".idea",
        "build",
        "dist",
        "htmlcov",
        # file
        ".coverage",
    ],
    overwrite=True,
    debug=True,
)
maker.templaterize()
