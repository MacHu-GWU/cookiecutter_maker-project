.. _examples:

Examples
==============================================================================


A Full Featured Example
------------------------------------------------------------------------------
`examples/example1 <https://github.com/MacHu-GWU/cookiecutter_maker-project/tree/main/examples/example1>`_ uses almost every feature. It is also a unit test: the generated template is compared with the expected one, and a project generated from it is compared with the seed project.

The seed project is a small Python package::

    my_package-project/
    ├── LICENSE.txt
    ├── README.rst
    ├── pyproject.toml
    ├── _static/
    │   └── my_package-favicon.ico
    ├── my_package/
    │   ├── __init__.py
    │   ├── impl.py
    │   ├── sub_package/
    │   │   └── __init__.py
    │   ├── template/
    │   │   └── index.html.jinja
    │   └── vendor/
    │       ├── __init__.py
    │       └── another_package.py
    └── tests/
        └── test_impl.py

.. literalinclude:: ../../../examples/example1/my_package-project/pyproject.toml
   :language: toml
   :caption: my_package-project/pyproject.toml

The config file:

.. literalinclude:: ../../../examples/example1/cookiecutter-maker.json
   :language: json
   :caption: cookiecutter-maker.json

Generate the template with ``cookiecutter-maker make`` in ``examples/example1``. Here is what each part does.


Author and Maintainer: Same Value, Different Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Both the author and the maintainer are ``Alice`` with ``alice@email.com``. A :ref:`selector hierarchy <core-concepts>` uses the surrounding text, including the ``# author`` / ``# maintainer`` comments, to tell them apart:

.. code-block:: toml

    authors = [
        { name = "{{ cookiecutter.author }}", email = "{{ cookiecutter.author_email }}" }, # author
    ]
    maintainers = [
        { name = "{{ cookiecutter.maintainer }}", email = "{{ cookiecutter.maintainer_email }}" }, # maintainer
    ]

The version uses ``['version = "0.1.1"', "0.1.1"]`` in the same way, so that only the project version is replaced.


Derived Variable: the URL Slug
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The README links to ``https://my-package.readthedocs.io``. ``my-package`` is not asked separately: the ``package_name_slug`` parameter has ``in_cookiecutter_json: false`` and a ``custom_placeholder`` that derives it from the package name:

.. code-block:: rst

    `Documentation <https://{{ cookiecutter.package_name | slugify }}.readthedocs.io/en/latest/>`_


Choice and Hooks: Generate the License
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``license`` is a choice of ``MIT``, ``AGPL-3.0-or-later`` and ``Proprietary``. The seed's ``LICENSE.txt`` is excluded, because its content depends on the choice. Instead, a `post generation hook <https://cookiecutter.readthedocs.io/en/stable/advanced/hooks.html>`_ in ``dir_hooks`` writes it. The hook is a template too, so it can read the choice:

.. literalinclude:: ../../../examples/example1/template/hooks/post_gen_project.py
   :language: python
   :caption: hooks/post_gen_project.py (beginning)
   :end-at: license = "{{ cookiecutter.license }}"

.. literalinclude:: ../../../examples/example1/template/hooks/post_gen_project.py
   :language: python
   :caption: hooks/post_gen_project.py (end)
   :start-at: license_mapping = {


Files That Must Not Change
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- ``my_package/template/index.html.jinja`` is a Jinja2 template of the package itself, matched by ``*.jinja`` in ``no_render``.
- ``my_package/vendor/another_package.py`` says ``This is NOT "my_package"``, which must not become a variable. The whole ``vendor`` folder is in ``no_render``.
- ``_static/my_package-favicon.ico`` is a binary file. It is copied as is, only its name becomes ``{{ cookiecutter.package_name }}-favicon.ico``.
- The README contains ``{{ this is a jinja template syntax }}``. It is not in ``no_render``, it is escaped automatically and comes out unchanged.

The generated ``cookiecutter.json``:

.. literalinclude:: ../../../examples/example1/template/cookiecutter.json
   :language: json
   :caption: template/cookiecutter.json


Template From an Open Source Project
------------------------------------------------------------------------------
Found a well organized open source project and want to start yours with the same structure? This script turns `python requests <https://github.com/psf/requests>`_ into a template, with the Python API.

**Step 1. Clone the repository**:

.. code-block:: bash

    git clone --branch v2.32.3 --depth 1 https://github.com/psf/requests

**Step 2. Run the script next to it**:

.. literalinclude:: ./new_project_like_python_requests.py
   :language: python
   :linenos:

**Step 3. Create a new project**:

.. code-block:: bash

    cookiecutter ./tmp
