
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


.. _install:

Install
------------------------------------------------------------------------------

``cookiecutter_maker`` is released on PyPI, so all you need is:

.. code-block:: console

    $ pip install cookiecutter_maker

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade cookiecutter_maker
