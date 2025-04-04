# -*- coding: utf-8 -*-

"""
Generate the AI knowledge base for the project.

.. code-block:: bash

    pip install "docpack>=0.1.1,<1.0.0"
"""

import shutil
from pathlib import Path

from cookiecutter_maker.paths import dir_project_root, PACKAGE_NAME
from docpack.api import GitHubPipeline

dir_here = Path(__file__).absolute().parent
dir_tmp = dir_here / "tmp"
shutil.rmtree(dir_tmp, ignore_errors=True)
dir_tmp.mkdir()

gh_pipeline = GitHubPipeline(
    domain="github.com",
    account="MacHu-GWU",
    repo=f"{PACKAGE_NAME}-project",
    branch="main",
    dir_repo=dir_project_root,
    include=[
        "README.rst",
        "Makefile",
        "poetry.toml",
        "pyproject.toml",
        "release-history.rst",
        f"{PACKAGE_NAME}/**/*.py",
        "tests/**/*.py",
        "docs/source/**/index.rst",
        "examples/*/**/*.*",
    ],
    exclude=[
        f"{PACKAGE_NAME}/tests/**",
        f"{PACKAGE_NAME}/tests/**/*.*",
        f"{PACKAGE_NAME}/vendor/**",
        f"{PACKAGE_NAME}/vendor/**/*.*",
        f"tests/all.py",
        f"tests/**/all.py",
        f"tests/examples/**/*.*",
        f"docs/source/index.rst",
        "examples/*/tmp/**/*.*",
        "examples/*/tmp/*.*",
        f".DS_Store",
        f"*.pyc",
        f"*.ico",
        f"*.png",
    ],
    dir_out=dir_tmp,
)
gh_pipeline.fetch()

filename = "all_in_one_knowledge_base.txt"
lines = [
    path.read_text()
    for path in dir_tmp.glob("*.xml")
]
dir_tmp.joinpath(filename).write_text("\n".join(lines), encoding="utf-8")
