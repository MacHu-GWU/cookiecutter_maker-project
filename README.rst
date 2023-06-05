
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


Summary
------------------------------------------------------------------------------
`Python Cookiecutter <https://cookiecutter.readthedocs.io>`_ is an awesome library that can create projects from templates. In an enterprise setting, people typically start with a concrete, working project and then convert it into a template that serves as the internal standard for future use (Template -> Project).

📋 `Cookiecutter Maker <https://github.com/MacHu-GWU/cookiecutter_maker-project>`_ is the inverse of ``cookiecutter`` (Project -> Template). It is a Python open source tool that can convert any given folder structure into a ``cookiecutter`` project.


Usage Example
------------------------------------------------------------------------------
Run the following python script to convert your concrete project into a template project:

.. code-block:: python

    from cookiecutter_maker.maker import Maker

    maker = Maker.new(
        # the input concrete project directory
        input_dir="/path-to-input-dir/my_awesome_project",
        # the output template project directory
        output_dir="/path-to-output-dir",
        # define the pair of ``concrete string`` and ``parameter name``
        mapper=[
            ("my_awesome_project", "package_name", "default_package_name"),
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
            # file
            ".coverage",
        ],
        # define what to copy as it is without rending
        # usually you should ignore jinja template files
        no_render=[
            "*.tpl",
        ],
        # over write the output location if already exists
        overwrite=True,
        # mapper could have one key is substring of another key
        # if this is True, it will ignore the error
        ignore_mapper_error=False,
        # when mapper could have one key is substring of another key
        # it will prompt you to confirm to continue
        skip_mapper_prompt=True,
        # do you want to print debug information?
        debug=True,
    )
    maker.templaterize()

In this example, it will create a directory ``{{ cookiecutter.package_name }}`` and a json file ``cookiecutter.json``. Now you can follow the `cookiecutter instruction <https://cookiecutter.readthedocs.io>`_ to generate more concrete projects.


.. _install:

Install
------------------------------------------------------------------------------

``cookiecutter_maker`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install cookiecutter_maker

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade cookiecutter_maker