Quick Start
==============================================================================
`cookiecutter <https://cookiecutter.readthedocs.io>`_ creates a new project from a template. ``cookiecutter_maker`` does the reverse: it turns a **working project** (the "seed") into a cookiecutter template, by replacing the concrete values you choose (package name, version, author ...) with cookiecutter variables.

This page walks through the whole round trip in a few minutes, using the command line. You can find all the files used here in `examples/quick_start <https://github.com/MacHu-GWU/cookiecutter_maker-project/tree/main/examples/quick_start>`_.


Install
------------------------------------------------------------------------------
The command line interface is an optional extra. Install it with:

.. code-block:: bash

    pip install "cookiecutter-maker[cli]"

Or run it without installing, using `uv <https://docs.astral.sh/uv/>`_:

.. code-block:: bash

    uvx --from "cookiecutter-maker[cli]" cookiecutter-maker --help

The rest of this page writes ``cookiecutter-maker`` for short.


Step 1. Start From a Seed Project
------------------------------------------------------------------------------
Here is a tiny but real Python project. Everything in it is concrete, nothing is a template yet::

    acme_tools-project/
    ├── README.md
    ├── pyproject.toml
    └── acme_tools/
        └── __init__.py

.. literalinclude:: ../../../examples/quick_start/acme_tools-project/pyproject.toml
   :language: toml
   :caption: acme_tools-project/pyproject.toml

.. literalinclude:: ../../../examples/quick_start/acme_tools-project/README.md
   :language: markdown
   :caption: acme_tools-project/README.md

We want a template where the package name, version, author and email can be changed.

.. note::

    The name of the seed folder becomes the name of the project folder in the template, and cookiecutter requires it to contain a variable. So the folder name must contain one of the values you parameterize, like ``acme_tools`` in ``acme_tools-project``.


Step 2. Write a Config File
------------------------------------------------------------------------------
Create a ``cookiecutter-maker.json`` next to the seed project. Run ``cookiecutter-maker init`` to get a sample one, then edit it:

.. literalinclude:: ../../../examples/quick_start/cookiecutter-maker.json
   :language: json
   :caption: cookiecutter-maker.json

- ``dir_input``: the seed project. ``dir_output``: where to write the template. Relative paths are relative to the config file.
- ``parameters``: each one says "replace this concrete string (``selector``) with the cookiecutter variable ``name``, whose default value is ``default``". The optional ``prompt`` is what cookiecutter asks the user.
- ``exclude``: files and folders that should not go into the template.


Step 3. Generate the Template
------------------------------------------------------------------------------
.. code-block:: bash

    cookiecutter-maker make

``make`` reads ``./cookiecutter-maker.json`` by default, and prints every replacement it makes:

.. code-block:: text

    ---------- parameters ----------
    - 'acme_tools' -> '{{ cookiecutter.package_name }}'
    - '0.1.0' -> '{{ cookiecutter.version }}'
    - 'Alice' -> '{{ cookiecutter.author }}'
    - 'alice@acme.com' -> '{{ cookiecutter.author_email }}'
    ---------- make template ----------
    from: .
      to: {{ cookiecutter.package_name }}-project
    from: acme_tools
      to: {{ cookiecutter.package_name }}-project/{{ cookiecutter.package_name }}
    from: acme_tools/__init__.py
      to: {{ cookiecutter.package_name }}-project/{{ cookiecutter.package_name }}/__init__.py
    from: pyproject.toml
      to: {{ cookiecutter.package_name }}-project/pyproject.toml
    from: README.md
      to: {{ cookiecutter.package_name }}-project/README.md
    Template is generated at: .../examples/quick_start/template

The result is a standard cookiecutter template. Folder names, file names and file contents are all parameterized::

    template/
    ├── cookiecutter.json
    └── {{ cookiecutter.package_name }}-project/
        ├── README.md
        ├── pyproject.toml
        └── {{ cookiecutter.package_name }}/
            └── __init__.py

.. code-block:: toml
    :caption: template/{{ cookiecutter.package_name }}-project/pyproject.toml

    [project]
    name = "{{ cookiecutter.package_name }}"
    version = "{{ cookiecutter.version }}"
    description = "Handy tools by Acme."
    authors = [
        { name = "{{ cookiecutter.author }}", email = "{{ cookiecutter.author_email }}" },
    ]

.. code-block:: json
    :caption: template/cookiecutter.json

    {
        "package_name": "acme_tools",
        "version": "0.1.0",
        "author": "Alice",
        "author_email": "alice@acme.com",
        "__prompts__": {
            "package_name": "Python package name, in snake case"
        },
        "_new_lines": "\n"
    }

Run ``make`` again after you change the seed project or the config. Add ``--overwrite`` to replace the previous template.


Step 4. Create a New Project From the Template
------------------------------------------------------------------------------
Now use cookiecutter as usual:

.. code-block:: bash

    uvx cookiecutter ./template

Answer the prompts with ``my_tools``, ``1.0.0``, ``Bob`` and ``bob@example.com``, and you get a new project with the same structure:

.. code-block:: markdown
    :caption: my_tools-project/README.md

    # my_tools

    Handy tools by Acme, version 1.0.0.

    ```python
    import my_tools

    print(my_tools.__version__)
    ```

.. code-block:: toml
    :caption: my_tools-project/pyproject.toml

    [project]
    name = "my_tools"
    version = "1.0.0"
    description = "Handy tools by Acme."
    authors = [
        { name = "Bob", email = "bob@example.com" },
    ]


Use the Python API Instead
------------------------------------------------------------------------------
The command line is a thin wrapper of the Python API. The same template can be generated with:

.. code-block:: python

    from pathlib import Path
    from cookiecutter_maker.api import Maker
    from cookiecutter_maker.api import Parameter

    maker = Maker(
        dir_input=Path("acme_tools-project"),
        dir_output=Path("template"),
        parameters=[
            Parameter(
                selector=["acme_tools"],
                name="package_name",
                default="acme_tools",
                prompt="Python package name, in snake case",
            ),
            Parameter(selector=["0.1.0"], name="version", default="0.1.0"),
            Parameter(selector=["Alice"], name="author", default="Alice"),
            Parameter(selector=["alice@acme.com"], name="author_email", default="alice@acme.com"),
        ],
        exclude=[".git", ".venv", "__pycache__", "*.pyc"],
    )
    maker.make_template()

Or load the config file and override some fields, exactly like the command line does:

.. code-block:: python

    from cookiecutter_maker.config import load_maker

    maker = load_maker(config="cookiecutter-maker.json", overwrite=True)
    maker.make_template()


Next Steps
------------------------------------------------------------------------------
- :ref:`core-concepts`: how a parameter decides what to replace, and how to replace a value only in a specific context.
- :ref:`filtering-files`: control which files go into the template, which files are copied as is, and limit a parameter to some files.
- :ref:`reference`: every config field and command line option.
- :ref:`examples`: a full featured example with choices, prompts, derived variables and hooks.
