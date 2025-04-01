# -*- coding: utf-8 -*-

"""
Convert a seed repo into a project template.

This script demonstrates how to use
`cookiecutter_maker <https://github.com/MacHu-GWU/cookiecutter_maker-project>`_
to convert an existing project (in this case, the 'requests' library)
into a cookiecutter template. The template can then be used to generate
new projects with the same structure but customized parameters.
"""

import shutil
from pathlib import Path
from cookiecutter_maker.api import Parameter, Maker

# Get the current directory and create a temporary directory for output
dir_here: Path = Path(__file__).absolute().parent
dir_tmp = dir_here.joinpath("tmp")

# Clean up any existing temporary directory
if dir_tmp.exists():
    shutil.rmtree(dir_tmp)

# Create a Maker instance to convert the project into a template
maker = Maker(
    # The input concrete project directory - the seed project you want to templatize
    # In this case, we're using the 'requests' library as our seed
    dir_input=dir_here.joinpath("requests"),

    # The output template directory - where the generated template will be placed
    dir_output=dir_tmp,

    # Define parameters that will be customizable in the generated template
    # Each Parameter defines:
    #   - selector: The concrete string in the original project to be replaced
    #   - name: The parameter name in the cookiecutter template
    #   - default: The default value that will appear in cookiecutter.json,
    #       if you set "default", then don't set "choice".
    #   - choice: Optional list of choices for the user to select from,
    #       if you set "choice", then don't set "default".
    parameters=[
        # Replace all occurrences of "requests" with the parameter "package_name"
        Parameter(
            selector=["requests"],
            name="package_name",
            default="your_package_name",
        ),
        # Replace the version number
        Parameter(
            selector=["2.32.3"],
            name="package_version",
            default="0.1.1",
        ),
        # Replace the author name
        Parameter(
            selector=["Kenneth Reitz"],
            name="author",
            default="Firstname Lastname",
        ),
        # Replace the author email
        Parameter(
            selector=["me@kennethreitz.org"],
            name="author_email",
            default="firstname.lastname@email.com",
        ),
        # You can add more parameters as needed for your template
        # Examples:
        # - GitHub username
        # - Project description
        # - License type (with choices)
        # - Python version requirement
    ],
    # Define which files/directories to include in the template
    # Empty list means include everything not explicitly excluded
    # You can use patterns like "**/*.py" to include all Python files
    # The rule is 'explicit exclude' > 'explicit include' > 'default include'
    include=[],
    # Define which files/directories to exclude from the template
    # These files/directories will not be copied to the template
    exclude=[
        # Common directories to exclude
        ".git",           # Git repository data
        ".venv",          # Virtual environment
        "__pycache__",    # Python cache files
        "*.pyc",          # Compiled Python files
        "build",          # Build artifacts
        "dist",           # Distribution packages
        ".pytest_cache",  # Test cache
        ".tox",           # Tox testing environments
        ".coverage",      # Coverage data
        "htmlcov",        # HTML coverage reports
    ],
    # Files that should be copied without rendering (processing)
    # Useful for files that contain syntax that conflicts with Jinja2
    # For example, template files that already use {{ }} syntax
    no_render=[
        "*.jinja",        # Jinja template files
        "*.j2",           # Alternative Jinja extension
        "*.html",         # HTML files with {{ }} syntax
    ],
    # Print detailed information during processing
    verbose=True,
)

# Execute the template generation process
maker.make_template()

print("\n" + "="*80)
print("Template generation complete!")
print(f"The template is available at: {dir_tmp}")
print("\nTo create a new project from this template, run:")
print(f"    cookiecutter {dir_tmp}")
print("="*80 + "\n")
