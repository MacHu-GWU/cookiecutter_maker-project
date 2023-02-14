# -*- coding: utf-8 -*-

from ._version import __version__

__short_description__ = "Convert any git repo into a cookiecutter projects template."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from .maker import Maker
except ImportError:
    pass
