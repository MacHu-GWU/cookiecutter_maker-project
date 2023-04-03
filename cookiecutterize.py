# -*- coding: utf-8 -*-

import shutil
from pathlib import Path
from cookiecutter_maker.maker import Maker

dir_tmp: Path = Path(__file__).absolute().parent.joinpath("tmp")
if dir_tmp.exists():
    shutil.rmtree(dir_tmp)
dir_tmp.mkdir(parents=True, exist_ok=True)

maker = Maker.new(
    input_dir="/Users/sanhehu/Documents/GitHub/afwf_example-project",
    output_dir=dir_tmp,
    mapper=[
        ("afwf_example", "package_name"),
        ("MacHu-GWU", "github_username"),
        ("Sanhe Hu", "author_name"),
        ("husanhe@gmail.com", "author_email"),
        ("/Users/sanhehu/Documents/Alfred-Preferences/Alfred.alfredpreferences/workflows/user.workflow.BE825014-E97C-4213-BEFE-E652C1C83974", "dir_workflow"),
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
        ".poetry-lock-hash.json",
        "requirements-dev.txt",
        "requirements-doc.txt",
        "requirements-main.txt",
        "requirements-test.txt",
    ],
    overwrite=True,
    debug=False,
)
maker.templaterize()
