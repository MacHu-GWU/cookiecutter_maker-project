Quick Start
==============================================================================
`cookiecutter_maker <https://github.com/MacHu-GWU/cookiecutter_maker-project>`_ is a tool that converts existing projects into reusable cookiecutter templates. This is the reverse of the traditional cookiecutter workflow - instead of starting with a template, you start with a concrete project and transform it into a template.


Example: Creating a Template from an Existing Project
------------------------------------------------------------------------------
Let's say we've found a project with a well-organized folder structure that we want to follow. Suppose we want to build our own open-source project using `python requests <https://github.com/psf/requests>`_ as a starting point.

**Step 1. Clone the repository**:

.. code-block:: bash

    git clone --branch v2.32.3 --depth 1 https://github.com/psf/requests

**Step 2. Create and run a script to generate the template**:

Create a Python script like the one below to convert the project into a cookiecutter template:

.. literalinclude:: ./new_project_like_python_requests.py
   :language: python
   :linenos:

In enterprise project, can be close source, private project, can be any programming language project, you may develop a nicely designed "seed" project, and use ``cookiecutter_maker`` to generate template project from it, then use ``cookiecutter`` to generate more project like this.


.. dropdown:: Console Logs

    .. code-block::

        ---------- parameters ----------
        - 'requests' -> '{{ cookiecutter.package_name }}'
        - '2.32.3' -> '{{ cookiecutter.package_version }}'
        - 'Kenneth Reitz' -> '{{ cookiecutter.author }}'
        - 'me@kennethreitz.org' -> '{{ cookiecutter.author_email }}'
        ---------- make template ----------
        from: .
          to: {{ cookiecutter.package_name }}
        from: .git-blame-ignore-revs
          to: {{ cookiecutter.package_name }}/.git-blame-ignore-revs
        from: LICENSE
          to: {{ cookiecutter.package_name }}/LICENSE
        from: .pre-commit-config.yaml
          to: {{ cookiecutter.package_name }}/.pre-commit-config.yaml
        from: Makefile
          to: {{ cookiecutter.package_name }}/Makefile
        from: HISTORY.md
          to: {{ cookiecutter.package_name }}/HISTORY.md
        from: ext
          to: {{ cookiecutter.package_name }}/ext
        from: ext/requests-logo.png
          to: {{ cookiecutter.package_name }}/ext/{{ cookiecutter.package_name }}-logo.png
        from: ext/requests-logo.ai
          to: {{ cookiecutter.package_name }}/ext/{{ cookiecutter.package_name }}-logo.ai
        from: ext/psf.png
          to: {{ cookiecutter.package_name }}/ext/psf.png
        from: ext/kr-compressed.png
          to: {{ cookiecutter.package_name }}/ext/kr-compressed.png
        from: ext/LICENSE
          to: {{ cookiecutter.package_name }}/ext/LICENSE
        from: ext/kr.png
          to: {{ cookiecutter.package_name }}/ext/kr.png
        from: ext/requests-logo.svg
          to: {{ cookiecutter.package_name }}/ext/{{ cookiecutter.package_name }}-logo.svg
        from: ext/flower-of-life.jpg
          to: {{ cookiecutter.package_name }}/ext/flower-of-life.jpg
        from: ext/ss.png
          to: {{ cookiecutter.package_name }}/ext/ss.png
        from: ext/ss-compressed.png
          to: {{ cookiecutter.package_name }}/ext/ss-compressed.png
        from: ext/psf-compressed.png
          to: {{ cookiecutter.package_name }}/ext/psf-compressed.png
        from: ext/requests-logo-compressed.png
          to: {{ cookiecutter.package_name }}/ext/{{ cookiecutter.package_name }}-logo-compressed.png
        from: pyproject.toml
          to: {{ cookiecutter.package_name }}/pyproject.toml
        from: tests
          to: {{ cookiecutter.package_name }}/tests
        from: tests/test_utils.py
          to: {{ cookiecutter.package_name }}/tests/test_utils.py
        from: tests/conftest.py
          to: {{ cookiecutter.package_name }}/tests/conftest.py
        from: tests/test_structures.py
          to: {{ cookiecutter.package_name }}/tests/test_structures.py
        from: tests/test_packages.py
          to: {{ cookiecutter.package_name }}/tests/test_packages.py
        from: tests/testserver
          to: {{ cookiecutter.package_name }}/tests/testserver
        from: tests/testserver/server.py
          to: {{ cookiecutter.package_name }}/tests/testserver/server.py
        from: tests/testserver/__init__.py
          to: {{ cookiecutter.package_name }}/tests/testserver/__init__.py
        from: tests/test_testserver.py
          to: {{ cookiecutter.package_name }}/tests/test_testserver.py
        from: tests/compat.py
          to: {{ cookiecutter.package_name }}/tests/compat.py
        from: tests/__init__.py
          to: {{ cookiecutter.package_name }}/tests/__init__.py
        from: tests/test_hooks.py
          to: {{ cookiecutter.package_name }}/tests/test_hooks.py
        from: tests/certs
          to: {{ cookiecutter.package_name }}/tests/certs
        from: tests/certs/valid
          to: {{ cookiecutter.package_name }}/tests/certs/valid
        from: tests/certs/valid/ca
          to: {{ cookiecutter.package_name }}/tests/certs/valid/ca
        from: tests/certs/valid/ca/ca.cnf
          to: {{ cookiecutter.package_name }}/tests/certs/valid/ca/ca.cnf
        from: tests/certs/valid/ca/ca-private.key
          to: {{ cookiecutter.package_name }}/tests/certs/valid/ca/ca-private.key
        from: tests/certs/valid/ca/Makefile
          to: {{ cookiecutter.package_name }}/tests/certs/valid/ca/Makefile
        from: tests/certs/valid/ca/ca.crt
          to: {{ cookiecutter.package_name }}/tests/certs/valid/ca/ca.crt
        from: tests/certs/valid/ca/ca.srl
          to: {{ cookiecutter.package_name }}/tests/certs/valid/ca/ca.srl
        from: tests/certs/valid/server
          to: {{ cookiecutter.package_name }}/tests/certs/valid/server
        from: tests/certs/valid/server/server.key
          to: {{ cookiecutter.package_name }}/tests/certs/valid/server/server.key
        from: tests/certs/valid/server/Makefile
          to: {{ cookiecutter.package_name }}/tests/certs/valid/server/Makefile
        from: tests/certs/valid/server/server.pem
          to: {{ cookiecutter.package_name }}/tests/certs/valid/server/server.pem
        from: tests/certs/valid/server/server.csr
          to: {{ cookiecutter.package_name }}/tests/certs/valid/server/server.csr
        from: tests/certs/valid/server/cert.cnf
          to: {{ cookiecutter.package_name }}/tests/certs/valid/server/cert.cnf
        from: tests/certs/mtls
          to: {{ cookiecutter.package_name }}/tests/certs/mtls
        from: tests/certs/mtls/Makefile
          to: {{ cookiecutter.package_name }}/tests/certs/mtls/Makefile
        from: tests/certs/mtls/README.md
          to: {{ cookiecutter.package_name }}/tests/certs/mtls/README.md
        from: tests/certs/mtls/client
          to: {{ cookiecutter.package_name }}/tests/certs/mtls/client
        from: tests/certs/mtls/client/Makefile
          to: {{ cookiecutter.package_name }}/tests/certs/mtls/client/Makefile
        from: tests/certs/mtls/client/ca
          to: {{ cookiecutter.package_name }}/tests/certs/mtls/client/ca
        from: tests/certs/mtls/client/ca/ca.cnf
          to: {{ cookiecutter.package_name }}/tests/certs/mtls/client/ca/ca.cnf
        from: tests/certs/mtls/client/ca/ca-private.key
          to: {{ cookiecutter.package_name }}/tests/certs/mtls/client/ca/ca-private.key
        from: tests/certs/mtls/client/ca/Makefile
          to: {{ cookiecutter.package_name }}/tests/certs/mtls/client/ca/Makefile
        from: tests/certs/mtls/client/ca/ca.crt
          to: {{ cookiecutter.package_name }}/tests/certs/mtls/client/ca/ca.crt
        from: tests/certs/mtls/client/ca/ca.srl
          to: {{ cookiecutter.package_name }}/tests/certs/mtls/client/ca/ca.srl
        from: tests/certs/mtls/client/client.pem
          to: {{ cookiecutter.package_name }}/tests/certs/mtls/client/client.pem
        from: tests/certs/mtls/client/client.csr
          to: {{ cookiecutter.package_name }}/tests/certs/mtls/client/client.csr
        from: tests/certs/mtls/client/cert.cnf
          to: {{ cookiecutter.package_name }}/tests/certs/mtls/client/cert.cnf
        from: tests/certs/mtls/client/client.key
          to: {{ cookiecutter.package_name }}/tests/certs/mtls/client/client.key
        from: tests/certs/README.md
          to: {{ cookiecutter.package_name }}/tests/certs/README.md
        from: tests/certs/expired
          to: {{ cookiecutter.package_name }}/tests/certs/expired
        from: tests/certs/expired/Makefile
          to: {{ cookiecutter.package_name }}/tests/certs/expired/Makefile
        from: tests/certs/expired/ca
          to: {{ cookiecutter.package_name }}/tests/certs/expired/ca
        from: tests/certs/expired/ca/ca.cnf
          to: {{ cookiecutter.package_name }}/tests/certs/expired/ca/ca.cnf
        from: tests/certs/expired/ca/ca-private.key
          to: {{ cookiecutter.package_name }}/tests/certs/expired/ca/ca-private.key
        from: tests/certs/expired/ca/Makefile
          to: {{ cookiecutter.package_name }}/tests/certs/expired/ca/Makefile
        from: tests/certs/expired/ca/ca.crt
          to: {{ cookiecutter.package_name }}/tests/certs/expired/ca/ca.crt
        from: tests/certs/expired/ca/ca.srl
          to: {{ cookiecutter.package_name }}/tests/certs/expired/ca/ca.srl
        from: tests/certs/expired/server
          to: {{ cookiecutter.package_name }}/tests/certs/expired/server
        from: tests/certs/expired/server/server.key
          to: {{ cookiecutter.package_name }}/tests/certs/expired/server/server.key
        from: tests/certs/expired/server/Makefile
          to: {{ cookiecutter.package_name }}/tests/certs/expired/server/Makefile
        from: tests/certs/expired/server/server.pem
          to: {{ cookiecutter.package_name }}/tests/certs/expired/server/server.pem
        from: tests/certs/expired/server/server.csr
          to: {{ cookiecutter.package_name }}/tests/certs/expired/server/server.csr
        from: tests/certs/expired/server/cert.cnf
          to: {{ cookiecutter.package_name }}/tests/certs/expired/server/cert.cnf
        from: tests/certs/expired/README.md
          to: {{ cookiecutter.package_name }}/tests/certs/expired/README.md
        from: tests/test_requests.py
          to: {{ cookiecutter.package_name }}/tests/test_{{ cookiecutter.package_name }}.py
        from: tests/utils.py
          to: {{ cookiecutter.package_name }}/tests/utils.py
        from: tests/test_adapters.py
          to: {{ cookiecutter.package_name }}/tests/test_adapters.py
        from: tests/test_help.py
          to: {{ cookiecutter.package_name }}/tests/test_help.py
        from: tests/test_lowlevel.py
          to: {{ cookiecutter.package_name }}/tests/test_lowlevel.py
        from: MANIFEST.in
          to: {{ cookiecutter.package_name }}/MANIFEST.in
        from: .coveragerc
          to: {{ cookiecutter.package_name }}/.coveragerc
        from: docs
          to: {{ cookiecutter.package_name }}/docs
        from: docs/index.rst
          to: {{ cookiecutter.package_name }}/docs/index.rst
        from: docs/_themes
          to: {{ cookiecutter.package_name }}/docs/_themes
        from: docs/_themes/LICENSE
          to: {{ cookiecutter.package_name }}/docs/_themes/LICENSE
        from: docs/_themes/flask_theme_support.py
          to: {{ cookiecutter.package_name }}/docs/_themes/flask_theme_support.py
        from: docs/_themes/.gitignore
          to: {{ cookiecutter.package_name }}/docs/_themes/.gitignore
        from: docs/requirements.txt
          to: {{ cookiecutter.package_name }}/docs/requirements.txt
        from: docs/_templates
          to: {{ cookiecutter.package_name }}/docs/_templates
        from: docs/_templates/sidebarintro.html
          to: {{ cookiecutter.package_name }}/docs/_templates/sidebarintro.html
        from: docs/_templates/sidebarlogo.html
          to: {{ cookiecutter.package_name }}/docs/_templates/sidebarlogo.html
        from: docs/_templates/hacks.html
          to: {{ cookiecutter.package_name }}/docs/_templates/hacks.html
        from: docs/Makefile
          to: {{ cookiecutter.package_name }}/docs/Makefile
        from: docs/conf.py
          to: {{ cookiecutter.package_name }}/docs/conf.py
        from: docs/_static
          to: {{ cookiecutter.package_name }}/docs/_static
        from: docs/_static/custom.css
          to: {{ cookiecutter.package_name }}/docs/_static/custom.css
        from: docs/_static/requests-sidebar.png
          to: {{ cookiecutter.package_name }}/docs/_static/{{ cookiecutter.package_name }}-sidebar.png
        from: docs/user
          to: {{ cookiecutter.package_name }}/docs/user
        from: docs/user/install.rst
          to: {{ cookiecutter.package_name }}/docs/user/install.rst
        from: docs/user/authentication.rst
          to: {{ cookiecutter.package_name }}/docs/user/authentication.rst
        from: docs/user/quickstart.rst
          to: {{ cookiecutter.package_name }}/docs/user/quickstart.rst
        from: docs/user/advanced.rst
          to: {{ cookiecutter.package_name }}/docs/user/advanced.rst
        from: docs/.nojekyll
          to: {{ cookiecutter.package_name }}/docs/.nojekyll
        from: docs/make.bat
          to: {{ cookiecutter.package_name }}/docs/make.bat
        from: docs/dev
          to: {{ cookiecutter.package_name }}/docs/dev
        from: docs/dev/contributing.rst
          to: {{ cookiecutter.package_name }}/docs/dev/contributing.rst
        from: docs/dev/authors.rst
          to: {{ cookiecutter.package_name }}/docs/dev/authors.rst
        from: docs/community
          to: {{ cookiecutter.package_name }}/docs/community
        from: docs/community/support.rst
          to: {{ cookiecutter.package_name }}/docs/community/support.rst
        from: docs/community/release-process.rst
          to: {{ cookiecutter.package_name }}/docs/community/release-process.rst
        from: docs/community/out-there.rst
          to: {{ cookiecutter.package_name }}/docs/community/out-there.rst
        from: docs/community/vulnerabilities.rst
          to: {{ cookiecutter.package_name }}/docs/community/vulnerabilities.rst
        from: docs/community/recommended.rst
          to: {{ cookiecutter.package_name }}/docs/community/recommended.rst
        from: docs/community/faq.rst
          to: {{ cookiecutter.package_name }}/docs/community/faq.rst
        from: docs/community/updates.rst
          to: {{ cookiecutter.package_name }}/docs/community/updates.rst
        from: docs/api.rst
          to: {{ cookiecutter.package_name }}/docs/api.rst
        from: NOTICE
          to: {{ cookiecutter.package_name }}/NOTICE
        from: README.md
          to: {{ cookiecutter.package_name }}/README.md
        from: setup.py
          to: {{ cookiecutter.package_name }}/setup.py
        from: requirements-dev.txt
          to: {{ cookiecutter.package_name }}/requirements-dev.txt
        from: .gitignore
          to: {{ cookiecutter.package_name }}/.gitignore
        from: .github
          to: {{ cookiecutter.package_name }}/.github
        from: .github/FUNDING.yml
          to: {{ cookiecutter.package_name }}/.github/FUNDING.yml
        from: .github/CODE_OF_CONDUCT.md
          to: {{ cookiecutter.package_name }}/.github/CODE_OF_CONDUCT.md
        from: .github/workflows
          to: {{ cookiecutter.package_name }}/.github/workflows
        from: .github/workflows/codeql-analysis.yml
          to: {{ cookiecutter.package_name }}/.github/workflows/codeql-analysis.yml
        from: .github/workflows/lint.yml
          to: {{ cookiecutter.package_name }}/.github/workflows/lint.yml
        from: .github/workflows/run-tests.yml
          to: {{ cookiecutter.package_name }}/.github/workflows/run-tests.yml
        from: .github/workflows/lock-issues.yml
          to: {{ cookiecutter.package_name }}/.github/workflows/lock-issues.yml
        from: .github/workflows/close-issues.yml
          to: {{ cookiecutter.package_name }}/.github/workflows/close-issues.yml
        from: .github/ISSUE_TEMPLATE.md
          to: {{ cookiecutter.package_name }}/.github/ISSUE_TEMPLATE.md
        from: .github/CONTRIBUTING.md
          to: {{ cookiecutter.package_name }}/.github/CONTRIBUTING.md
        from: .github/ISSUE_TEMPLATE
          to: {{ cookiecutter.package_name }}/.github/ISSUE_TEMPLATE
        from: .github/ISSUE_TEMPLATE/Feature_request.md
          to: {{ cookiecutter.package_name }}/.github/ISSUE_TEMPLATE/Feature_request.md
        from: .github/ISSUE_TEMPLATE/Bug_report.md
          to: {{ cookiecutter.package_name }}/.github/ISSUE_TEMPLATE/Bug_report.md
        from: .github/ISSUE_TEMPLATE/Custom.md
          to: {{ cookiecutter.package_name }}/.github/ISSUE_TEMPLATE/Custom.md
        from: .github/dependabot.yml
          to: {{ cookiecutter.package_name }}/.github/dependabot.yml
        from: .github/SECURITY.md
          to: {{ cookiecutter.package_name }}/.github/SECURITY.md
        from: tox.ini
          to: {{ cookiecutter.package_name }}/tox.ini
        from: AUTHORS.rst
          to: {{ cookiecutter.package_name }}/AUTHORS.rst
        from: setup.cfg
          to: {{ cookiecutter.package_name }}/setup.cfg
        from: .readthedocs.yaml
          to: {{ cookiecutter.package_name }}/.readthedocs.yaml
        from: src
          to: {{ cookiecutter.package_name }}/src
        from: src/requests
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}
        from: src/requests/cookies.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/cookies.py
        from: src/requests/auth.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/auth.py
        from: src/requests/sessions.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/sessions.py
        from: src/requests/hooks.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/hooks.py
        from: src/requests/compat.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/compat.py
        from: src/requests/models.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/models.py
        from: src/requests/certs.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/certs.py
        from: src/requests/__init__.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/__init__.py
        from: src/requests/status_codes.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/status_codes.py
        from: src/requests/packages.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/packages.py
        from: src/requests/__version__.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/__version__.py
        from: src/requests/api.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/api.py
        from: src/requests/_internal_utils.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/_internal_utils.py
        from: src/requests/utils.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/utils.py
        from: src/requests/exceptions.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/exceptions.py
        from: src/requests/structures.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/structures.py
        from: src/requests/help.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/help.py
        from: src/requests/adapters.py
          to: {{ cookiecutter.package_name }}/src/{{ cookiecutter.package_name }}/adapters.py

**Step 3. Use the generated template with cookiecutter**:

Once the template is generated, you can create new projects with:

.. code-block:: bash

    cookiecutter path/to/generated/template


More Examples
------------------------------------------------------------------------------
- Example 1:
    - `seed project <https://github.com/MacHu-GWU/cookiecutter_maker-project/tree/main/examples/example1/my_package-project>`_
    - `template directory <https://github.com/MacHu-GWU/cookiecutter_maker-project/tree/main/examples/example1/template>`_
    - `cookiecutter.json <https://github.com/MacHu-GWU/cookiecutter_maker-project/blob/main/examples/example1/template/cookiecutter.json>`_
    - `hooks <https://github.com/MacHu-GWU/cookiecutter_maker-project/tree/main/examples/example1/hooks>`_


Enterprise Applications
------------------------------------------------------------------------------
In enterprise environments, this tool is particularly valuable for:

- Internal frameworks and libraries with consistent structure
- Microservice templates that follow company standards
- Domain-specific applications with similar patterns
- Closed-source or private repositories that need standardization
- Projects in any programming language (not limited to Python)

You can develop a well-designed "seed" project according to your organization's best practices, then:

- Use `cookiecutter_maker <https://github.com/MacHu-GWU/cookiecutter_maker-project>`_ to generate a template from your seed project
- Share the template within your organization
- Use `cookiecutter <https://github.com/cookiecutter/cookiecutter>`_ to consistently generate new projects based on this template
- Maintain standards and reduce setup time for new initiatives

Each generated project will have the same structure and patterns, but with customized parameters (names, versions, etc.) based on your specifications.
