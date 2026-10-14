.. _filtering-files:

Filtering Files
==============================================================================
A seed project usually contains things that don't belong in a template: ``.git``, virtual environments, build artifacts, lock files. And some files should go into the template without any change. ``Maker`` has three lists of patterns for this:

.. list-table::
    :header-rows: 1

    * - Option
      - What it does
    * - ``exclude``
      - Matched files and folders are left out. An excluded folder is not walked at all.
    * - ``include``
      - If not empty, only matched **files** are kept. Empty means all files.
    * - ``no_render``
      - Matched files are kept, but copied as is: no parameter replacement in the content, and cookiecutter won't render them either.

``exclude`` always wins over ``include``.

Each :class:`~cookiecutter_maker.parameter.Parameter` has its own ``include`` and ``exclude`` too. They don't filter files, they limit which files a parameter is applied to, see `Limit a Parameter to Some Files`_.


Pattern Syntax
------------------------------------------------------------------------------
Patterns use the `.gitignore syntax <https://git-scm.com/docs/gitignore#_pattern_format>`_ (implemented by `pathspec <https://pypi.org/project/pathspec/>`_), matched against the path relative to ``dir_input``, with ``/`` as the separator on every OS.

.. list-table::
    :header-rows: 1

    * - Pattern
      - Matches
      - Doesn't match
    * - ``*.py``
      - ``a.py``, ``src/a.py``, ``src/sub/a.py``
      - ``a.txt``
    * - ``/*.py``
      - ``a.py`` (root level only)
      - ``src/a.py``
    * - ``src/*.py``
      - ``src/a.py``
      - ``a.py``, ``src/sub/a.py``
    * - ``src/**/*.py``
      - ``src/a.py``, ``src/sub/a.py``
      - ``a.py``
    * - ``build`` or ``build/``
      - the ``build`` folder and everything in it, at any level
      - ``build.py``
    * - ``src/*``
      - everything inside ``src``, recursively
      - ``src`` itself

A typical ``exclude`` for a Python project:

.. code-block:: json

    "exclude": [
        ".git",
        ".venv",
        "__pycache__",
        "*.pyc",
        ".pytest_cache",
        "htmlcov",
        "build",
        "dist",
        "uv.lock"
    ]

.. tip::

    If ``cookiecutter-maker.json`` is inside the seed project, add it to ``exclude``. If ``dir_output`` is inside the seed project, it is skipped automatically.


include
------------------------------------------------------------------------------
``include`` is for "I only want these files". It applies to files only: folders are walked as long as they are not excluded, so ``include=["*.py"]`` keeps all python files in all folders.

When ``include`` is not empty, a folder is created in the template only if it contains at least one included file, so you don't get empty folders.

.. code-block:: python

    Maker(
        ...,
        include=["*.py", "pyproject.toml", "README.md"],
        exclude=["tests/"],
    )


no_render
------------------------------------------------------------------------------
Use ``no_render`` for files that must stay exactly as they are, for example:

- Jinja2 templates (``*.jinja``, ``*.j2``) that are part of your project, not part of the cookiecutter template.
- Vendored third party code, where a parameter value might appear by coincidence.

These files are copied byte for byte. Their **names** are still parameterized. In ``cookiecutter.json``, ``cookiecutter_maker`` lists the exact template path of each of them in ``_copy_without_render``, so cookiecutter copies them without rendering too. Files that are not valid UTF-8 (images, text in other encodings ...) are copied and listed the same way, without being in ``no_render``:

.. code-block:: json

    "_copy_without_render": [
        "{{ cookiecutter.package_name }}/template/index.html.jinja",
        "{{ cookiecutter.package_name }}/vendor/__init__.py",
        "{{ cookiecutter.package_name }}/vendor/another_package.py"
    ]

.. note::

    You don't need ``no_render`` just because a file contains ``{{ }}``, existing Jinja2 syntax is escaped automatically (see :ref:`core-concepts`). Use it when the content must not change at all.


.. _parameter-include-exclude:

Limit a Parameter to Some Files
------------------------------------------------------------------------------
Sometimes the same text means different things in different files, and the surrounding text can't tell them apart (so a :ref:`selector hierarchy <core-concepts>` doesn't help). For example, the project version ``0.1.1`` in ``pyproject.toml``, and a dependency that happens to have the same version in a requirements file.

Each :class:`~cookiecutter_maker.parameter.Parameter` also has ``include`` and ``exclude``, with the same pattern syntax. They limit which files' **content** the parameter is applied to:

.. code-block:: python

    Parameter(
        selector=['version = "0.1.1"', "0.1.1"],
        name="version",
        default="0.1.1",
        include=["pyproject.toml", "*/_version.py"],
    )

Two things to know:

- They only limit the file **content**. Folder and file **names** always use all parameters, so a file always ends up in its renamed parent folder.
- When a longer selector is excluded from a file, a shorter selector of another parameter may still match inside it. For example, if the ``alice@acme.com`` parameter excludes ``LICENSE``, the ``alice`` parameter still replaces the ``alice`` part of the email in ``LICENSE``.
