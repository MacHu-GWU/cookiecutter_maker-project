# -*- coding: utf-8 -*-

from pathlib import Path
from cookiecutter_maker.maker import Maker

dir_tmp: Path = Path(__file__).absolute().parent.joinpath("tmp")
dir_tmp.mkdir(parents=True, exist_ok=True)

maker = Maker.new(
    input_dir="/Users/sanhehu/Documents/Bitbucket/udm-studio/sound_credit_ingest-project",
    output_dir=dir_tmp,
    mapper=[
        ("sound_credit_ingest", "package_name"),
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
        ".current-env-name.json",
        ".poetry-lock-hash.json",
        "requirements-main.txt",
        "requirements-dev.txt",
        "requirements-test.txt",
        "requirements-doc.txt",
    ],
    overwrite=True,
    debug=False,
)
maker.templaterize()
