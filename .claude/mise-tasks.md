# Available Mise Tasks

This document lists all available mise tasks for this project.

## Quick Reference

| Command | Description |
|---------|-------------|
| `mise run build` | 🏗️ Build Python package wheel and source distribution using uv (outputs to dist/) |
| `mise run build-doc` | 📚 Build Sphinx documentation using sphinx-build (generates HTML in docs/build/html/) |
| `mise run cov` | 🧪📊 Run unit tests with code coverage using pytest (generates HTML report in htmlcov/) |
| `mise run export` | 📋 Export Python dependencies to requirements*.txt files using uv (for legacy compatibility) |
| `mise run inst` | 💾 Install all Python dependencies using uv (syncs from pyproject.toml and uv.lock) |
| `mise run list-tasks` | 📝 Generate .claude/mise-tasks.md listing all mise tasks (for AI assistants) |
| `mise run notebook-to-markdown` | 📓 Convert Jupyter notebooks to Markdown for AI knowledge base (processes .ipynb files) |
| `mise run publish` | 🚀 Publish Python package to PyPI using uv (prints PyPI URL after success) |
| `mise run release` | 🏷 Create GitHub release using PyGithub (idempotent: skips if release exists) |
| `mise run setup-codecov` | ⚙️ Setup Codecov upload token on GitHub Actions secrets using PyGithub and httpx |
| `mise run setup-readthedocs` | ⚙️ Setup ReadTheDocs project and GitHub webhook using httpx API client |
| `mise run test` | 🧪 Run unit tests using pytest (scans test files automatically) |
| `mise run update-github-metadata` | 🔧 Update GitHub repository description and homepage using PyGithub |
| `mise run venv-create` | 🐍 Create Python virtual environment using uv (creates .venv directory) |
| `mise run venv-remove` | 🗑️ Remove Python virtual environment (deletes .venv directory) |
| `mise run view-cov` | 👀📊 Open code coverage HTML report in browser (requires 'cov' task to run first) |
| `mise run view-doc` | 👀📚 Open built Sphinx documentation in browser (requires 'build-doc' task to run first) |

## Tasks by Category

### Environment Management

**`mise run venv-create`**
- 🐍 Create Python virtual environment using uv (creates .venv directory)
- Command: `uv venv --allow-existing`

**`mise run venv-remove`**
- 🗑️ Remove Python virtual environment (deletes .venv directory)
- Command: `rm -r .venv`

### Dependency Management

**`mise run export`**
- 📋 Export Python dependencies to requirements*.txt files using uv (for legacy compatibility)

**`mise run inst`**
- 💾 Install all Python dependencies using uv (syncs from pyproject.toml and uv.lock)
- Dependencies: `venv-create`
- Command: `uv sync --all-extras`

### Testing

**`mise run cov`**
- 🧪📊 Run unit tests with code coverage using pytest (generates HTML report in htmlcov/)
- Dependencies: `inst`

**`mise run test`**
- 🧪 Run unit tests using pytest (scans test files automatically)
- Dependencies: `inst`
- Command: `.venv/bin/pytest tests`

**`mise run view-cov`**
- 👀📊 Open code coverage HTML report in browser (requires 'cov' task to run first)
- Command: `open htmlcov/index.html`

### Documentation

**`mise run build-doc`**
- 📚 Build Sphinx documentation using sphinx-build (generates HTML in docs/build/html/)
- Dependencies: `inst`
- Command: `rm -rf docs/build
.venv/bin/sphinx-build -b html docs/source docs/build/html
`

**`mise run view-doc`**
- 👀📚 Open built Sphinx documentation in browser (requires 'build-doc' task to run first)
- Command: `open docs/build/html/index.html`

### Building & Publishing

**`mise run build`**
- 🏗️ Build Python package wheel and source distribution using uv (outputs to dist/)
- Command: `rm -rf dist
uv build
`

**`mise run publish`**
- 🚀 Publish Python package to PyPI using uv (prints PyPI URL after success)
- Dependencies: `build`
- Command: `.venv/bin/python .mise/tasks/publish.py
uv publish --token $PYPI_TOKEN
`

### GitHub Release Management

**`mise run release`**
- 🏷 Create GitHub release using PyGithub (idempotent: skips if release exists)
- Dependencies: `inst`
- Command: `.venv/bin/python .mise/tasks/release.py`

### CI/CD Setup

**`mise run setup-codecov`**
- ⚙️ Setup Codecov upload token on GitHub Actions secrets using PyGithub and httpx
- Dependencies: `inst`
- Command: `.venv/bin/python .mise/tasks/setup-codecov.py`

**`mise run setup-readthedocs`**
- ⚙️ Setup ReadTheDocs project and GitHub webhook using httpx API client
- Dependencies: `inst`
- Command: `.venv/bin/python .mise/tasks/setup-readthedocs.py`

**`mise run update-github-metadata`**
- 🔧 Update GitHub repository description and homepage using PyGithub
- Dependencies: `inst`
- Command: `.venv/bin/python .mise/tasks/update-github-metadata.py`

### Documentation Tools

**`mise run notebook-to-markdown`**
- 📓 Convert Jupyter notebooks to Markdown for AI knowledge base (processes .ipynb files)
- Dependencies: `inst`
- Command: `.venv/bin/python .mise/tasks/notebook-to-markdown.py`
