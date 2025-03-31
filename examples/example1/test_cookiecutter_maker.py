# -*- coding: utf-8 -*-

import shutil
from pathlib import Path
from cookiecutter_maker.maker import Maker, Parameter

dir_here = Path(__file__).absolute().parent
dir_input = dir_here / "my_package-project"
dir_output = dir_here / "tmp"
if dir_output.exists():
    shutil.rmtree(dir_output)

maker = Maker(
    dir_input=dir_input,
    dir_output=dir_output,
    parameters=[
        Parameter(
            selector=["my_package"],
            name="package_name",
            default="my_package",
        ),
        Parameter(
            selector=["my-package"],
            name="package_name_slug",
            default="my-package",
        ),
        Parameter(
            selector=[
                'version = "1.0.0"',
                "1.0.0",
            ],
            name="version",
            default="0.1.1",
        ),
    ],
    no_render=[
        "my_package/template/*.jinja",
    ],
)
maker.make_template()
