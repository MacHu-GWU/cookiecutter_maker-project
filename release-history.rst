.. _release_history:

Release and Version History
==============================================================================


Backlog (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.1.0 (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Breaking Changes**

- Drop support for Python 3.9 and 3.10. Now supports Python 3.11 ~ 3.14.
- ``cookiecutter_maker.__version__`` is now read from the installed package metadata; the ``_version`` module and its ``__short_description__`` / ``__license__`` / ``__author__`` / ``__author_email__`` / ``__maintainer__`` / ``__maintainer_email__`` attributes are removed.

**Features and Improvements**

- Add the ``cookiecutter-maker`` command line interface, powered by `Python Fire <https://github.com/google/python-fire>`_. It is an optional dependency, install it with ``pip install "cookiecutter-maker[cli]"`` or run it with ``uvx --from "cookiecutter-maker[cli]" cookiecutter-maker``.
    - ``cookiecutter-maker init``: create a sample ``cookiecutter-maker.json`` config file.
    - ``cookiecutter-maker make``: generate the template. Command line arguments (``--dir_input``, ``--dir_output``, ``--dir_hooks``, ``--include``, ``--exclude``, ``--no_render``, ``--verbose``, ``--overwrite``) take precedence over the config file (``--config``, default to ``./cookiecutter-maker.json``).
    - ``cookiecutter-maker version``: print the version.
- Add the ``cookiecutter_maker.config`` module to load a ``Maker`` from a JSON config file and merge it with overrides. Relative paths in the config file are resolved against the config file's directory.
- Add ``Maker.from_dict`` and ``Parameter.from_dict``, unknown or missing fields raise a clear ``ValueError``.
- ``Parameter.include`` / ``Parameter.exclude`` now work (they were accepted but ignored before). They limit which files' **content** a parameter is applied to, e.g. replace the version only in ``pyproject.toml`` but not in ``uv.lock``. File and directory names always use all parameters.
- Add ``Maker.overwrite``, delete the existing ``dir_output`` before generating the template. For safety, it only deletes an empty directory or a previously generated template (has ``cookiecutter.json``), and never deletes ``dir_input`` or its parents.

**Minor Improvements**

- ``Maker`` now raises ``ValueError`` for duplicate parameter names or duplicate ``selector[0]``, which used to silently override each other.

**Bugfixes**

- Fix ``include``: any non-empty ``include`` used to skip the root directory and crash. Now ``include`` patterns apply to files only, directories are only filtered by ``exclude``, and directories without included files are not created.
- Fix Jinja2 block and comment syntax in the seed project (e.g. ``{% if x %}`` in HTML, ``${#array[@]}`` in shell scripts) breaking the generated template. ``{%`` and ``{#`` are now escaped like ``{{``.
- Fix parameter replacement randomly corrupting text when a selector is short (it could match inside the internal UUID placeholders), and depending on the order of parameters when selectors overlap. Now all selectors are replaced in a single pass and the longest match wins.
- Fix infinite recursion when ``dir_output`` is inside ``dir_input``, the output directory is now skipped.
- Fix ``no_render`` files being rendered by cookiecutter anyway: cookiecutter matches ``_copy_without_render`` with ``fnmatch`` against the template path, so most git-style patterns (e.g. ``vendor/``, ``/*.html``, ``*/vendor/**/*.*``) never matched. ``cookiecutter.json`` now lists the exact template path of each ``no_render`` file instead of the patterns.
- Use ``/`` as the path separator for ``include`` / ``exclude`` / ``no_render`` pattern matching on Windows.
- Fix the misspelled ``classifier`` key in ``pyproject.toml``, so the PyPI classifiers (license, supported Python versions) are actually published.

**Miscellaneous**

- Migrate the development workflow from poetry + ``bin/`` scripts to mise + uv + Claude Code, and the build backend from poetry-core to setuptools.


1.0.2 (2025-04-02)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

- Add optional property ``prompt`` to ``Parameter``.
- Add optional property ``custom_placeholder`` to ``Parameter``.
- Add optional property ``in_cookiecutter_json`` to ``Parameter``.

**Miscellaneous**

- Update unit test for the three new properties of ``Parameter``.
- Update the line diff in the test.


1.0.1 (2025-04-01)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**💥Breaking Changes**

- Rework the API:
    - now it uses more reliable ``pathspec`` to match files.
    - now it support using ``selector`` to precisely select the sub string you want to substitute.
- Drop Python3.8 support. Now only support Python3.9+.

**Features and Improvements**

- Add ``Parameter`` to the public API.

**Minor Improvements**

- Add a comprehensive integration test.


0.3.1 (2023-06-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- allow user to specify the default value of the parameter.
- add ``ignore_mapper_error`` and ``skip_mapper_prompt`` arguments to ``Maker.new(..)``.
- add ``cleanup_output_dir`` argument to ``Maker.templaterize(...)``.

**Miscellaneous**

- add test on Python3.7, 3.8, 3.9, 3.10


0.2.1 (2023-02-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- also generate the ``cookiecutter.json`` file.

**Minor Improvements**

- update documents.


0.1.1 (2023-02-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
