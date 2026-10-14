
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

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/cookiecutter_maker-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
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
`cookiecutter <https://cookiecutter.readthedocs.io>`_ creates new projects from a template. ``cookiecutter_maker`` does the reverse: it turns a **working project** into a cookiecutter template.

Writing a template by hand means editing a project full of ``{{ cookiecutter.xxx }}`` that you can't run or test. With ``cookiecutter_maker``, you keep developing a normal project (the "seed"), and generate the template from it whenever it changes. You tell it which concrete values to parameterize, it takes care of the rest:

- Replaces the values in file contents, file names and folder names.
- Replaces a value only in the context you want, e.g. the project version but not a dependency that happens to have the same version.
- Limits a parameter to some files, e.g. replace the version in ``pyproject.toml`` but not in ``CHANGELOG.md``.
- Keeps existing Jinja2 syntax (GitHub Actions ``${{ }}``, HTML templates, ``{}}`` in JSON ...) working in the generated projects.
- Filters files with ``.gitignore`` style patterns, and copies binary or "do not touch" files as is.
- Writes ``cookiecutter.json``, with defaults, choices and prompts.


30 Seconds Example
------------------------------------------------------------------------------
Next to your project ``acme_tools-project/``, create a ``cookiecutter-maker.json``:

.. code-block:: json

    {
        "dir_input": "./acme_tools-project",
        "dir_output": "./template",
        "parameters": [
            {"selector": ["acme_tools"], "name": "package_name", "default": "acme_tools"},
            {"selector": ["0.1.0"], "name": "version", "default": "0.1.0"},
            {"selector": ["Alice"], "name": "author", "default": "Alice"}
        ],
        "exclude": [".git", ".venv", "__pycache__"]
    }

Generate the template, then use it like any cookiecutter template:

.. code-block:: console

    $ uvx --from "cookiecutter-maker[cli]" cookiecutter-maker make
    $ uvx cookiecutter ./template

Prefer Python? The same thing is available as ``cookiecutter_maker.api.Maker``. See the `Quick Start <https://cookiecutter-maker.readthedocs.io/en/latest/01-Quick-Start/index.html>`_ for the full walkthrough.


.. _install:

Install
------------------------------------------------------------------------------
``cookiecutter_maker`` is released on PyPI. Install the library and the command line interface:

.. code-block:: console

    $ pip install "cookiecutter-maker[cli]"

Or only the library, for the Python API:

.. code-block:: console

    $ pip install cookiecutter-maker

Or run the command line without installing, using `uv <https://docs.astral.sh/uv/>`_:

.. code-block:: console

    $ uvx --from "cookiecutter-maker[cli]" cookiecutter-maker --help


Use With AI Coding Agents
------------------------------------------------------------------------------
This repo ships an `Agent Skill <https://code.claude.com/docs/en/skills>`_ that teaches AI coding agents such as `Claude Code <https://claude.com/claude-code>`_ how to use ``cookiecutter_maker``: the public API, the command line options and the config file format, without reading the source code.

Copy the `pypi-cookiecutter_maker <https://github.com/MacHu-GWU/cookiecutter_maker-project/tree/main/.claude/skills/pypi-cookiecutter_maker>`_ folder into your project's ``.claude/skills/`` (or ``~/.claude/skills/`` for all projects). The agent then loads it automatically whenever you ask it to turn a project into a cookiecutter template.
