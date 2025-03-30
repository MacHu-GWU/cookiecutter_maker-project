
.. image:: https://readthedocs.org/projects/cookiecutter-maker/badge/?version=latest
    :target: https://cookiecutter-maker.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/cookiecutter_maker-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/cookiecutter_maker-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/cookiecutter_maker-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/cookiecutter_maker-project

.. image:: https://img.shields.io/pypi/v/cookiecutter-maker.svg
    :target: https://pypi.python.org/pypi/cookiecutter-maker

.. image:: https://img.shields.io/pypi/l/cookiecutter-maker.svg
    :target: https://pypi.python.org/pypi/cookiecutter-maker

.. image:: https://img.shields.io/pypi/pyversions/cookiecutter-maker.svg
    :target: https://pypi.python.org/pypi/cookiecutter-maker

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/cookiecutter_maker-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/cookiecutter_maker-project

------

.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://cookiecutter-maker.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://cookiecutter-maker.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/cookiecutter_maker-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/cookiecutter_maker-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/cookiecutter_maker-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/cookiecutter-maker#files


Welcome to ``cookiecutter_maker`` Documentation
==============================================================================
.. image:: https://cookiecutter-maker.readthedocs.io/en/latest/_static/cookiecutter_maker-logo.png
    :target: https://cookiecutter-maker.readthedocs.io/en/latest/


What is Cookiecutter Maker?
------------------------------------------------------------------------------
``cookiecutter_maker`` is a Python library that does the reverse of traditional `cookiecutter <https://cookiecutter.readthedocs.io>`_ templating. Instead of creating a template from scratch, it helps you convert an existing project into a cookiecutter template automatically.


Key Concept
------------------------------------------------------------------------------
In software development, teams often start with a working project and want to standardize it as a template for future use. Cookiecutter Maker simplifies this process by:

- Automatically converting concrete projects into cookiecutter templates
- Replacing hardcoded values with parameterized placeholders
- Generating a ``cookiecutter.json`` configuration file
- Handling complex project structures with customizable ``include/exclude`` rules


Documentation
------------------------------------------------------------------------------
For detailed usage, configuration options, and advanced examples, please visit our `Documentation <https://cookiecutter-maker.readthedocs.io/en/latest/>`_ Site.


Usage Example
------------------------------------------------------------------------------
Run the following python script to convert your concrete project into a template project:

.. code-block:: python

    from cookiecutter_maker.api import Maker

    maker = Maker.new(
        # the input concrete project directory
        input_dir="/path-to-input-dir/my_awesome_project",
        # the output template project directory
        output_dir="/path-to-output-dir",
        # define the ``string to replace``, ``parameter name`` and ``default parameter value``
        mapper=[
            ("my_awesome_project", "package_name", "default_package_name"),
        ],
        # define what to include in the input directory
        # it is the relative path from the input directory
        # the rule is 'explicit exclude' > 'explicit include' > 'default include'
        # if empty, then include all files and directories
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
