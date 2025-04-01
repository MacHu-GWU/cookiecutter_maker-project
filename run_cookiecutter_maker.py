# -*- coding: utf-8 -*-

"""
Convert a seed repo into a project template.
"""

import shutil
from pathlib import Path
from cookiecutter_maker.api import Parameter, Maker

dir_here: Path = Path(__file__).absolute().parent
dir_tmp = dir_here.joinpath("tmp")
if dir_tmp.exists():
    shutil.rmtree(dir_tmp)

maker = Maker(
    # the input concrete project directory
    dir_input=Path.home().joinpath("Documents", "GitHub", "cookiecutter_pywf_open_source_demo-project"),
    # the output template project directory
    dir_output=dir_tmp,
    # define the pair of ``concrete string`` and ``parameter name``
    parameters=[
        Parameter(
            selector=["cookiecutter_pywf_open_source_demo"],
            name="package_name",
            default="your_package_name",
        ),
        Parameter(
            selector=["cookiecutter-pywf-open-source-demo"],
            name="package_name_slug",
            default="your-package-name",
        ),

        Parameter(
            selector=["cookiecutter-pywf-open-source-demo"],
            name="package_name_slug",
            default="your-package-name",
        ),
        Parameter(
            selector=["MacHu-GWU"],
            name="github_username",
            default="your_github_username",
        ),
        Parameter(
            selector=['name = "Sanhe Hu", ', "Sanhe Hu"],
            name="author",
            default="Firstname Lastname",
        ),
        Parameter(
            selector=['email = "husanhe@gmail.com" },', "husanhe@gmail.com"],
            name="author_email",
            default="firstname.lastname@email.com",
        ),
        Parameter(
            selector=['dev_python = "3.11.8"', "3.11.8"],
            name="dev_python_version",
            default="3.11.8",
        ),
    ],
    # define what to include in the input directory
    # it is the relative path from the input directory
    # the rule is 'explicit exclude' > 'explicit include' > 'default include'
    include=[],
    # define what to exclude in the input directory
    # it is the relative path from the input directory
    exclude=[
        # dir
        ".venv",
        ".pytest_cache",
        ".git",
        ".idea",
        "build",
        "dist",
        "htmlcov",
        "__pycache__",
        ".poetry",
        "tmp",
        "bin/pywf_open_source",
        "docs/source/cookiecutter_pywf_open_source_demo",
        # file
        ".coverage",
    ],
    no_render=[
        # dir
        "cookiecutter_pywf_open_source_demo/vendor/**/*.*",
        # file
        "poetry.lock",
        "requirements.txt",
        "requirements-automation.txt",
        "requirements-dev.txt",
        "requirements-doc.txt",
        "requirements-test.txt",
    ],
    # do you want to print debug information?
    verbose=True,
)
maker.make_template()
