# -*- coding: utf-8 -*-

"""
Make sure the Quick Start example in the document works.
"""

from pathlib import Path

from cookiecutter.main import cookiecutter

from cookiecutter_maker.config import load_maker
from cookiecutter_maker.paths import path_enum

dir_quick_start = path_enum.dir_project_root.joinpath("examples", "quick_start")


def test(tmp_path: Path):
    maker = load_maker(
        config=dir_quick_start.joinpath("cookiecutter-maker.json"),
        dir_output=tmp_path.joinpath("template"),
        verbose=False,
    )
    maker.make_template()
    cookiecutter(
        str(maker.dir_output),
        no_input=True,
        output_dir=str(tmp_path),
        extra_context={
            "package_name": "my_tools",
            "version": "1.0.0",
            "author": "Bob",
            "author_email": "bob@example.com",
        },
    )
    dir_project = tmp_path.joinpath("my_tools-project")
    assert dir_project.joinpath("my_tools", "__init__.py").read_text() == '__version__ = "1.0.0"\n'
    pyproject = dir_project.joinpath("pyproject.toml").read_text()
    assert 'name = "my_tools"' in pyproject
    assert '{ name = "Bob", email = "bob@example.com" }' in pyproject
    readme = dir_project.joinpath("README.md").read_text()
    assert "# my_tools" in readme
    assert "version 1.0.0" in readme


if __name__ == "__main__":
    from cookiecutter_maker.tests import run_cov_test

    run_cov_test(
        __file__,
        "cookiecutter_maker.config",
        preview=False,
    )
