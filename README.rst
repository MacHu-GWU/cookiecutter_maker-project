
.. image:: https://readthedocs.org/projects/cookiecutter_maker/badge/?version=latest
    :target: https://cookiecutter_maker.readthedocs.io/index.html
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/cookiecutter_maker-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/cookiecutter_maker-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/cookiecutter_maker-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/cookiecutter_maker-project

.. image:: https://img.shields.io/pypi/v/cookiecutter_maker.svg
    :target: https://pypi.python.org/pypi/cookiecutter_maker

.. image:: https://img.shields.io/pypi/l/cookiecutter_maker.svg
    :target: https://pypi.python.org/pypi/cookiecutter_maker

.. image:: https://img.shields.io/pypi/pyversions/cookiecutter_maker.svg
    :target: https://pypi.python.org/pypi/cookiecutter_maker

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/cookiecutter_maker-project

------


.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://cookiecutter_maker.readthedocs.io/index.html

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://cookiecutter_maker.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Source_Code-blue.svg
    :target: https://cookiecutter_maker.readthedocs.io/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/cookiecutter_maker-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/cookiecutter_maker-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/cookiecutter_maker-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/cookiecutter_maker#files


Welcome to ``cookiecutter_maker`` Documentation
==============================================================================
`cookiecutter <https://cookiecutter.readthedocs.io>`_ is an awesome library that can create projects from templates. However, you need to create a working template first. People actually usually start with a concrete, working project, then convert it into a template for future use. ``cookiecutter_maker`` is a Python open source tool can convert any git repo into a cookiecutter projects template.

Usage:

.. code-block:: python

    from cookiecutter_maker.maker import Maker

    maker = Maker.new(
        input_dir="/path-to-input-dir/my_awesome_project",
        output_dir="/path-to-output-dir",
        mapper=[
            ("my_awesome_project", "package_name"),
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
        ],
        overwrite=True,
        debug=True,
    )
    maker.templaterize()


.. _install:

Install
------------------------------------------------------------------------------

``cookiecutter_maker`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install cookiecutter_maker

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade cookiecutter_maker