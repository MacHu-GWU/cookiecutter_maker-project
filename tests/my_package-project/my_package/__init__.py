# -*- coding: utf-8 -*-

"""
my_package is a sample cookiecutter_maker project.
"""

name = "name"
str_template = f"{{name}}"
assert str_template.format(name="alice") == "alice"
