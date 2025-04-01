# -*- coding: utf-8 -*-

"""
A utility for file path filtering using Git-style pattern matching with configurable include and exclude rules.
"""

import typing as T
import dataclasses
import pathspec


@dataclasses.dataclass
class PathMatcher:
    """
    PathMatcher is a utility class that provides file and directory path matching functionality
    using ``GitWildMatchPattern`` syntax from the `pathspec <https://pypi.org/project/pathspec/>`_ Python library.

    This class allows you to:

    - Define include and exclude patterns for paths
    - Check if a specific path matches your criteria
    - Filter collections of paths based on your patterns

    The pattern matching follows Git's wildcard pattern syntax, which is similar to but not
    identical to standard glob patterns. The patterns are matched against the relative path
    using forward slash (/) as the directory separator.

    **Pattern Syntax Examples**

    Basic Patterns

    - ``*.py``: Matches any Python file, regardless of location
        - Matches: ``test.py``, ``folder/test.py``, ``folder/subfolder/test.py``
        - Does not match: ``folder``, ``test.txt``

    Root-level Patterns

    - ``/*.py``: Matches any Python file, but ONLY at the root level
        - Matches: ``test.py``
        - Does not match: ``folder/test.py``, ``folder/subfolder/test.py``

    Directory-specific Patterns

    - ``folder/*.py``: Matches any Python file in the root level of ``folder/`` only
        - Matches: ``folder/test.py``
        - Does not match: ``test.py``, ``folder/subfolder/test.py``

    Directory Pattern Variations

    - ``folder*``: Matches the folder itself and anything inside it recursively
        - Matches: ``folder``, ``folder/test.py``, ``folder/subfolder``, ``folder/subfolder/test.py``
        - Does not match: ``test.py``

    - ``folder/*``: Matches anything inside ``folder/`` recursively, but NOT the folder itself
        - Matches: ``folder/test.py``, ``folder/subfolder``, ``folder/subfolder/test.py``
        - Does not match: ``folder``, ``test.py``

    - ``folder/*.*``: Matches any FILE in the root level of ``folder/`` only
        - Matches: ``folder/test.py``, ``folder/doc.txt``
        - Does not match: ``folder``, ``folder/subfolder``, ``folder/subfolder/test.py``

    Recursive Patterns

    - ``folder/**/*.*``: Matches any FILE in ``folder/`` RECURSIVELY
        - Matches: ``folder/test.py``, ``folder/subfolder/test.py``
        - Does not match: ``folder``, ``folder/subfolder``, ``test.py``

    - ``folder/*.py``: Matches Python files in the root level of ``folder/`` only
        - Matches: ``folder/test.py``
        - Does not match: ``folder``, ``test.py``, ``folder/subfolder/test.py``

    - ``folder/**/*.py``: Matches Python files in ``folder/`` RECURSIVELY
        - Matches: ``folder/test.py``, ``folder/subfolder/test.py``
        - Does not match: ``folder``, ``folder/subfolder``, ``test.py``

    Multiple Patterns

    You can specify multiple patterns as a list. A path will match if it matches ANY of the patterns:

    - ``["folder1/*.py", "folder2/*.py"]``: Matches Python files in either ``folder1`` or ``folder2``
        - Matches: ``folder1/test.py``, ``folder2/test.py``
        - Does not match: ``folder3/test.py``, ``test.py``

    **Usage Examples**

    .. code-block:: python

        # Create a matcher that includes Python files but excludes test files
        matcher = PathMatcher.new(
           include=["**/*.py"],
           exclude=["**/test_*.py", "**/tests/*"]
        )

        # Check if a path matches
        matcher.is_match("src/module.py")  # True
        matcher.is_match("tests/test_module.py")  # False

        # Filter a list of paths
        paths = ["src/module.py", "src/main.py", "tests/test_module.py"]
        filtered = [p for p in paths if matcher.is_match(p)]  # ["src/module.py", "src/main.py"]

    **Common Pattern Use Cases**

    1. Include all files in a directory (recursively):
        - ``["directory/**/*"]``

    2. Include specific file types in all directories:
        - ``["**/*.py", "**/*.md"]``

    3. Exclude specific directories:
        - ``exclude=["**/temp/*", "**/logs/*"]``

    4. Include everything except specific file types:
        - ``include=["**/*"]``
        - ``exclude=["**/*.log", "**/*.tmp"]``

    5. Include only root level files:
        - ``["/*.*"]``

    Note: This class uses the `pathspec <https://pypi.org/project/pathspec/>`_ Python library under the hood, which provides
    the implementation of Git's wildcard pattern matching. For more advanced pattern
    matching details, refer to the pathspec documentation or Git's documentation on
    gitignore patterns.
    """

    include_spec: T.Optional[pathspec.PathSpec] = dataclasses.field()
    exclude_spec: T.Optional[pathspec.PathSpec] = dataclasses.field()
    no_render_spec: T.Optional[pathspec.PathSpec] = dataclasses.field()

    @classmethod
    def new(
        cls,
        include: list[str],
        exclude: list[str],
        no_render: list[str] = None,
    ) -> "PathMatcher":
        """
        Create a new :class:`PathMatcher` instance with the given include and exclude patterns.
        """
        if include:
            include_spec = pathspec.PathSpec.from_lines(
                pathspec.patterns.GitWildMatchPattern, include
            )
        else:
            include_spec = None

        if exclude:
            exclude_spec = pathspec.PathSpec.from_lines(
                pathspec.patterns.GitWildMatchPattern, exclude
            )
        else:
            exclude_spec = None

        if no_render:
            no_render_spec = pathspec.PathSpec.from_lines(
                pathspec.patterns.GitWildMatchPattern, no_render
            )
        else:
            no_render_spec = None

        return cls(
            include_spec=include_spec,
            exclude_spec=exclude_spec,
            no_render_spec=no_render_spec,
        )

    def is_match(self, path: str) -> bool:
        """
        Determines if a path should be included based on include/exclude patterns.

        The matching logic follows these rules:

        1. If no include patterns are specified, all paths are eligible for inclusion
        2. If include patterns exist, the path must match at least one include pattern
        3. If the path matches any exclude pattern, it is rejected regardless of include matches

        :param path: A path string using forward slash (/) as directory separator.
            Should not start or end with slash.

        Examples:

        - ``file.txt``
        - ``folder``
        - ``folder/file.txt``
        - ``folder/subfolder/file.txt``

        :returns: True if the path should be included, False otherwise
        """
        # Check include patterns (if any)

        if self.include_spec is not None:
            if self.include_spec.match_file(path) is False:
                return False

        # Check exclude patterns (if any)
        if self.exclude_spec is None:
            return True
        else:
            return self.exclude_spec.match_file(path) is False

    def is_render(self, path: str) -> bool:  # pragma: no cover
        """
        Determines if a path should be rendered based on no_render patterns.
        """
        if self.no_render_spec is None:
            return True
        return not self.no_render_spec.match_file(path)
