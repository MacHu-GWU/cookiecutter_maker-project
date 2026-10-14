.. _core-concepts:

Core Concepts
==============================================================================
This page explains how ``cookiecutter_maker`` turns a seed project into a template, and how to tell it exactly which strings to replace.


How a Template Is Made
------------------------------------------------------------------------------
:meth:`Maker.make_template() <cookiecutter_maker.maker.Maker.make_template>` walks through ``dir_input`` and writes a cookiecutter template to ``dir_output``::

    dir_output/
    ├── cookiecutter.json          # parameters, prompts and settings
    ├── hooks/                     # copied from dir_hooks, if set
    └── <name of dir_input>/       # the seed project, parameterized
        └── ...

For every folder and file in the seed project:

1. Skip it if it is filtered out by ``include`` / ``exclude`` (see :ref:`filtering-files`).
2. Replace the parameters in its **name**.
3. For a file, process its **content**:

   - ``no_render`` files and files that are not valid UTF-8 are copied byte for byte, and listed in ``_copy_without_render`` so cookiecutter copies them as is too.
   - In text files, existing Jinja2 syntax is escaped (see `Existing Jinja2 Syntax Is Preserved`_) and the parameters are replaced, in a single pass. A parameter with ``include`` / ``exclude`` is only applied to the matched files (see `Where a Parameter Applies`_).

Finally, ``cookiecutter.json`` is written with the parameters in the order you define them.

.. important::

    Cookiecutter requires the project folder name in the template to contain a variable. So the name of ``dir_input`` must contain at least one ``selector[0]``, e.g. ``acme_tools-project`` with an ``acme_tools`` parameter. Otherwise ``make_template`` raises ``ValueError`` before writing anything.


Parameter
------------------------------------------------------------------------------
A :class:`~cookiecutter_maker.parameter.Parameter` maps a concrete string in the seed project to a cookiecutter variable:

.. code-block:: python

    Parameter(
        selector=["acme_tools"],     # the concrete string to find
        name="package_name",         # becomes {{ cookiecutter.package_name }}
        default="acme_tools",        # default value in cookiecutter.json
        prompt="Python package name" # optional, what cookiecutter asks the user
    )

Instead of ``default``, a parameter can define a list of ``choice``, the first one is the default (`cookiecutter choice variables <https://cookiecutter.readthedocs.io/en/stable/advanced/choice_variables.html>`_). A parameter must have exactly one of ``default`` and ``choice``.

Matching is a plain, case sensitive substring search. ``acme_tools`` also matches inside ``acme_tools_extra``, but not ``Acme_Tools``:

.. code-block:: text

    acme_tools acme_tools_extra Acme_Tools
    {{ cookiecutter.package_name }} {{ cookiecutter.package_name }}_extra Acme_Tools

This is usually what you want for a package name. When it is not, use a selector hierarchy.


Selector Hierarchy: Replace a Value Only in Its Context
------------------------------------------------------------------------------
Short values like a version ``0.1.1`` or a name ``Alice`` often appear in places that have nothing to do with your project. ``selector`` is a **list**, from the broadest context to the value itself:

.. code-block:: python

    Parameter(
        selector=['version = "0.1.1"', "0.1.1"],
        name="version",
        default="0.1.1",
    )

- Only ``selector[0]`` is searched: ``version = "0.1.1"``.
- Inside each match, the **last** selector ``0.1.1`` is replaced with the variable.

So the dependency version is left alone:

.. code-block:: text

    version = "0.1.1"
    dependencies = ["requests==0.1.1"]

.. code-block:: text

    version = "{{ cookiecutter.version }}"
    dependencies = ["requests==0.1.1"]

Each selector must be a substring of the previous one, otherwise a ``ValueError`` is raised. You can use as many levels as you need, and a selector can span multiple lines. For example, when the author and the maintainer are both ``Alice``, the surrounding text tells them apart:

.. code-block:: python

    Parameter(
        selector=['authors = [\n    { name = "Alice"', 'name = "Alice"', "Alice"],
        name="author",
        default="Alice",
    )
    Parameter(
        selector=['maintainers = [\n    { name = "Alice"', 'name = "Alice"', "Alice"],
        name="maintainer",
        default="Alice",
    )

.. note::

    Every occurrence of the last selector inside ``selector[0]`` is replaced. With ``selector=['v = "1.1"', "1"]``, both ``1`` in ``1.1`` are replaced. Make the last selector specific enough.



Where a Parameter Applies
------------------------------------------------------------------------------
By default, a parameter is applied to every file. When the same text means different things in different files, and the surrounding text can't tell them apart, use the parameter's own ``include`` / ``exclude`` patterns to limit which files' **content** it is applied to:

.. code-block:: python

    Parameter(
        selector=["0.1.0"],
        name="version",
        default="0.1.0",
        include=["pyproject.toml", "*/_version.py"],  # not CHANGELOG.md, uv.lock ...
    )

Folder and file **names** always use all parameters. See :ref:`parameter-include-exclude` for the details.


How Multiple Parameters Are Replaced
------------------------------------------------------------------------------
All parameters are replaced in a **single pass** over the text:

- **The longest match wins**, regardless of the order of the parameters. ``alice@acme.com`` is replaced as a whole, even if the ``alice`` parameter comes first:

  .. code-block:: text

      alice <alice@acme.com>
      {{ cookiecutter.author }} <{{ cookiecutter.email }}>

- **A replacement is never replaced again**, so a variable name can never be broken by another parameter.
- Two parameters can't have the same ``selector[0]``, and two parameters in ``cookiecutter.json`` can't have the same ``name``. Both raise ``ValueError``.


Names and Contents
------------------------------------------------------------------------------
Parameters are replaced in folder names, file names and file contents. A seed folder ``acme_tools/`` becomes ``{{ cookiecutter.package_name }}/``, and the name of ``dir_input`` itself becomes the name of the project folder in the template.


Existing Jinja2 Syntax Is Preserved
------------------------------------------------------------------------------
Cookiecutter renders every template file with `Jinja2 <https://jinja.palletsprojects.com>`_. If the seed project already contains Jinja2-like syntax, it would be rendered (and usually fail) when you generate a new project. Some common examples:

- ``${{ github.sha }}`` in GitHub Actions workflows
- ``{% if user %}`` in HTML templates
- ``${#array[@]}`` in shell scripts

``cookiecutter_maker`` wraps ``{{``, ``}}``, ``{%`` and ``{#`` in text files with ``{% raw %}...{% endraw %}``, so they come out of cookiecutter unchanged. It also handles the tricky cases: ``{}}`` in JSON (``{"a": {}}``), and a value inside braces like ``${acme_tools}`` or ``f"{acme_tools}"``, where the placeholder would otherwise merge with the braces into ``{{{``. You don't need to do anything. For files that are full of such syntax, such as Jinja2 templates, you can also copy them as is with ``no_render`` (see :ref:`filtering-files`).


Text and Binary Files
------------------------------------------------------------------------------
- Files that are valid UTF-8 are treated as text. Their line endings are normalized to LF (``\n``), and ``cookiecutter.json`` sets ``"_new_lines": "\n"``, so generated projects always use LF.
- Other files (images, archives, text in other encodings ...) are copied byte for byte, only their names are parameterized. They are listed in ``_copy_without_render``, so cookiecutter doesn't try to render them.


Derived Variables
------------------------------------------------------------------------------
Some values are derived from another one, for example the package name ``acme_tools`` and its URL slug ``acme-tools``. Instead of asking the user twice, use ``custom_placeholder`` with a `Jinja2 filter <https://cookiecutter.readthedocs.io/en/stable/advanced/template_extensions.html>`_, and ``in_cookiecutter_json=False`` so it is not a separate variable:

.. code-block:: python

    Parameter(
        selector=["acme_tools"],
        name="package_name",
        default="acme_tools",
    )
    Parameter(
        selector=['url = "https://acme-tools.readthedocs.io"', "acme-tools"],
        name="package_slug",
        custom_placeholder="{{ cookiecutter.package_name | slugify }}",
        in_cookiecutter_json=False,
    )

``custom_placeholder`` replaces the last selector, just like the default ``{{ cookiecutter.<name> }}``:

.. code-block:: text

    url = "https://acme-tools.readthedocs.io"
    url = "https://{{ cookiecutter.package_name | slugify }}.readthedocs.io"
