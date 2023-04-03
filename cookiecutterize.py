# -*- coding: utf-8 -*-

import shutil
from pathlib import Path
from cookiecutter_maker.maker import Maker

dir_tmp: Path = Path(__file__).absolute().parent.joinpath("tmp")
if dir_tmp.exists():
    shutil.rmtree(dir_tmp)
dir_tmp.mkdir(parents=True, exist_ok=True)

maker = Maker.new(
    input_dir="/Users/sanhehu/Documents/CodeCommit/ami_backup-project",
    output_dir=dir_tmp,
    mapper=[
        ("ami_backup", "package_name"),
        ("Sanhe Hu", "author_name"),
        ("sanhehu@amazon.com", "author_email"),
        ("0.1.1", "semantic_version"),
        ("awshsh_app_dev_us_east_1", "aws_profile"),
        ("807388292768", "aws_account_id"),
        ("us-east-1", "aws_region"),
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
        "bin/tests.py",
    ],
    overwrite=True,
    debug=False,
)
maker.templaterize()
