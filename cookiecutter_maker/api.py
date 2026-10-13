# -*- coding: utf-8 -*-

"""
Public API.

- :class:`~cookiecutter_maker.maker.Maker`: convert a seed project into a cookiecutter template.
- :class:`~cookiecutter_maker.parameter.Parameter`: a value to replace with a cookiecutter variable.

To load a ``cookiecutter-maker.json`` config file, see :func:`cookiecutter_maker.config.load_maker`.
"""

from .maker import Parameter
from .maker import Maker
