.. _reference:

Reference
==============================================================================


Config File
------------------------------------------------------------------------------
``cookiecutter-maker.json`` is a JSON object. Its keys are the arguments of :class:`~cookiecutter_maker.maker.Maker`, and each item of ``parameters`` is an object whose keys are the arguments of :class:`~cookiecutter_maker.parameter.Parameter`. A misspelled key raises an error instead of being ignored.

- Relative paths (``dir_input``, ``dir_output``, ``dir_hooks``) are relative to the **directory of the config file**, not the current directory. ``~`` is expanded.
- JSON doesn't allow comments.
- ``cookiecutter-maker init`` writes a sample to start from.


Maker Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
    :header-rows: 1
    :widths: 15 15 70

    * - Key
      - Default
      - Description
    * - ``dir_input``
      - required
      - The seed project folder. Its name, parameterized, becomes the project folder in the template.
    * - ``dir_output``
      - required
      - Where to write the template. Must not exist, unless ``overwrite`` is true.
    * - ``parameters``
      - required
      - List of parameters, see `Parameter Options`_. Config file only, not available on the command line.
    * - ``include``
      - ``[]``
      - If not empty, only matched files are kept. See :ref:`filtering-files`.
    * - ``exclude``
      - ``[]``
      - Matched files and folders are left out.
    * - ``no_render``
      - ``[]``
      - Matched files are copied as is.
    * - ``dir_hooks``
      - ``null``
      - A `cookiecutter hooks <https://cookiecutter.readthedocs.io/en/stable/advanced/hooks.html>`_ folder, copied to ``<dir_output>/hooks``.
    * - ``verbose``
      - ``true``
      - Print every parameter and every file processed.
    * - ``overwrite``
      - ``false``
      - Delete an existing ``dir_output`` first, see `Overwrite Safety`_.


Parameter Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. list-table::
    :header-rows: 1
    :widths: 22 15 63

    * - Key
      - Default
      - Description
    * - ``selector``
      - required
      - List of strings, from the broadest context to the value to replace. Each one must be a substring of the previous one. See :ref:`core-concepts`.
    * - ``name``
      - required
      - Variable name, the placeholder is ``{{ cookiecutter.<name> }}``.
    * - ``default``
      - ``null``
      - Default value in ``cookiecutter.json``.
    * - ``choice``
      - ``[]``
      - List of choices, the first one is the default. Exactly one of ``default`` and ``choice`` is required, unless ``in_cookiecutter_json`` is false.
    * - ``prompt``
      - ``null``
      - What cookiecutter asks the user, written to ``__prompts__`` (`human readable prompts <https://cookiecutter.readthedocs.io/en/stable/advanced/human_readable_prompts.html>`_). A string, or an object for choice labels.
    * - ``custom_placeholder``
      - ``null``
      - Use this instead of ``{{ cookiecutter.<name> }}``, e.g. ``{{ cookiecutter.package_name | slugify }}``.
    * - ``in_cookiecutter_json``
      - ``true``
      - Set to false for a derived value that should not be a variable of its own, usually with ``custom_placeholder``.
    * - ``include``
      - ``[]``
      - If not empty, only apply this parameter to the content of matched files. See :ref:`parameter-include-exclude`.
    * - ``exclude``
      - ``[]``
      - Don't apply this parameter to the content of matched files.


Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
These raise an error before anything is written:

- Unknown or missing keys.
- A selector that is not a substring of the previous one.
- Both or neither of ``default`` and ``choice``.
- Two parameters with the same ``selector[0]``, or the same ``name`` in ``cookiecutter.json``.
- ``dir_input`` or ``dir_hooks`` doesn't exist, or ``dir_output`` exists without ``overwrite``.


Overwrite Safety
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``overwrite`` deletes ``dir_output`` before generating the template. To protect you from a wrong path such as ``.`` or ``~``, it only deletes ``dir_output`` when:

- it is an empty folder, or a previously generated template (it has a ``cookiecutter.json``), and
- it is not ``dir_input``, nor a parent of ``dir_input``.

Otherwise it raises an error and deletes nothing.


Command Line
------------------------------------------------------------------------------
Install with ``pip install "cookiecutter-maker[cli]"``, or run with ``uvx --from "cookiecutter-maker[cli]" cookiecutter-maker``. Add ``--help`` to any command for details.


cookiecutter-maker make
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generate the template.

.. code-block:: bash

    cookiecutter-maker make [--config PATH] [--dir_input PATH] [--dir_output PATH]
                            [--dir_hooks PATH] [--include PATTERNS] [--exclude PATTERNS]
                            [--no_render PATTERNS] [--verbose | --noverbose]
                            [--overwrite | --nooverwrite]

**Where the settings come from**, from highest to lowest priority:

1. Command line options.
2. The config file: ``--config``, or ``./cookiecutter-maker.json`` if it exists.
3. The defaults in `Maker Options`_.

Other rules:

- Relative paths on the command line are relative to the **current directory**.
- ``--include``, ``--exclude`` and ``--no_render`` accept a comma separated string (``".git,.venv"``) or a JSON list (``'[".git", ".venv"]'``). They **replace** the list in the config file, not extend it.
- Both ``--dir_input`` and ``--dir-input`` styles work.
- Errors such as a missing file print a one line message and exit with code 1.

Examples:

.. code-block:: bash

    # use ./cookiecutter-maker.json
    cookiecutter-maker make

    # another config file, and regenerate the template
    cookiecutter-maker make --config path/to/cookiecutter-maker.json --overwrite

    # override some settings of the config file
    cookiecutter-maker make --dir_output ./out --exclude ".git,.venv,uv.lock" --noverbose


cookiecutter-maker init
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Write a sample config file to start from.

.. code-block:: bash

    cookiecutter-maker init [--path PATH] [--overwrite]

``--path`` defaults to ``./cookiecutter-maker.json``. An existing file is not replaced unless ``--overwrite`` is given.


cookiecutter-maker version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Print the installed version.


Python API
------------------------------------------------------------------------------
Everything above is also available in Python:

- :class:`cookiecutter_maker.api.Maker` and :class:`cookiecutter_maker.api.Parameter`: build the objects directly, then call :meth:`~cookiecutter_maker.maker.Maker.make_template`.
- :meth:`Maker.from_dict() <cookiecutter_maker.maker.Maker.from_dict>`: build a ``Maker`` from the same structure as the config file. Relative paths are kept as is.
- :func:`cookiecutter_maker.config.load_maker`: what ``cookiecutter-maker make`` does. Read the config file, apply overrides (keyword arguments, ``None`` means "not set"), and return a ``Maker``.

See the API document for details.
