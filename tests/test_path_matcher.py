# -*- coding: utf-8 -*-

from cookiecutter_maker.path_matcher import PathMatcher


class TestPathMatcher:
    def test_include_exclude_interaction(self):
        # Case 1: Empty include, empty exclude (matches everything)
        matcher = PathMatcher.new(include=[], exclude=[])
        assert matcher.is_match("file.txt") is True
        assert matcher.is_match("folder/file.py") is True

        # Case 2: Empty include, with exclude (matches everything except excluded)
        matcher = PathMatcher.new(include=[], exclude=["*.txt"])
        assert matcher.is_match("file.txt") is False
        assert matcher.is_match("file.py") is True

        # Case 3: With include, empty exclude (matches only included)
        matcher = PathMatcher.new(include=["*.py"], exclude=[])
        assert matcher.is_match("file.txt") is False
        assert matcher.is_match("file.py") is True

        # Case 4: With include, with exclude (exclude takes precedence)
        matcher = PathMatcher.new(include=["*.py"], exclude=["test_*.py"])
        assert matcher.is_match("file.py") is True
        assert matcher.is_match("test_file.py") is False

        # Case 5: With include, with overlapping exclude (exclude takes precedence)
        matcher = PathMatcher.new(include=["**/*.py"], exclude=["folder/*.py"])
        assert matcher.is_match("file.py") is True
        assert matcher.is_match("folder/file.py") is False
        assert matcher.is_match("other/file.py") is True

        # Case 6: Multiple includes, multiple excludes
        matcher = PathMatcher.new(
            include=["**/*.py", "**/*.md"], exclude=["**/test_*.py", "**/temp/*"]
        )
        assert matcher.is_match("file.py") is True
        assert matcher.is_match("docs/file.md") is True
        assert matcher.is_match("test_file.py") is False
        assert matcher.is_match("temp/file.py") is False
        assert matcher.is_match("folder/temp/file.md") is False


if __name__ == "__main__":
    from cookiecutter_maker.tests import run_cov_test

    run_cov_test(__file__, "cookiecutter_maker.path_matcher", preview=False)