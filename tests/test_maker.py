# -*- coding: utf-8 -*-

import json
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter

from cookiecutter_maker.parameter import Parameter
from cookiecutter_maker.maker import Maker


def write_files(dir_root: Path, files: dict[str, str]):
    for relpath, content in files.items():
        path = dir_root.joinpath(relpath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def list_files(dir_root: Path) -> list[str]:
    return sorted(
        p.relative_to(dir_root).as_posix() for p in dir_root.rglob("*") if p.is_file()
    )


def new_maker(dir_input: Path, dir_output: Path, **kwargs) -> Maker:
    return Maker(
        dir_input=dir_input,
        dir_output=dir_output,
        parameters=[Parameter(selector=["my_pkg"], name="package_name", default="my_pkg")],
        verbose=False,
        **kwargs,
    )


def test_validate_parameters():
    p1 = Parameter(selector=["a"], name="x", default="a")
    p2 = Parameter(selector=["b"], name="x", default="b")
    with pytest.raises(ValueError, match="Duplicate parameter name"):
        Maker(dir_input=Path("a"), dir_output=Path("b"), parameters=[p1, p2])

    p3 = Parameter(selector=["a"], name="y", default="a")
    with pytest.raises(ValueError, match="Duplicate parameter selector"):
        Maker(dir_input=Path("a"), dir_output=Path("b"), parameters=[p1, p3])

    # a name not in cookiecutter.json can be reused by a custom placeholder
    p4 = Parameter(
        selector=["A"],
        name="x",
        custom_placeholder="{{ cookiecutter.x | upper }}",
        in_cookiecutter_json=False,
    )
    Maker(dir_input=Path("a"), dir_output=Path("b"), parameters=[p1, p4])


def test_include(tmp_path: Path):
    dir_input = tmp_path / "my_pkg"
    write_files(
        dir_input,
        {
            "README.md": "my_pkg",
            "my_pkg/__init__.py": "",
            "my_pkg/sub/impl.py": "",
            "my_pkg/sub/impl.txt": "",
            "docs/index.rst": "",
            "tests/test_impl.py": "",
        },
    )
    dir_output = tmp_path / "out"
    new_maker(
        dir_input,
        dir_output,
        include=["*.py"],
        exclude=["tests/"],
    ).make_template()

    # include patterns apply to files, directories are only filtered by exclude,
    # and directories without included files (docs) are not created
    dir_template = dir_output / "{{ cookiecutter.package_name }}"
    assert list_files(dir_template) == [
        "{{ cookiecutter.package_name }}/__init__.py",
        "{{ cookiecutter.package_name }}/sub/impl.py",
    ]
    assert dir_template.joinpath("docs").exists() is False


def test_exclude_directory(tmp_path: Path):
    dir_input = tmp_path / "my_pkg"
    write_files(dir_input, {"build/sub/a.txt": "", "dist/b.txt": "", "src/c.txt": ""})
    dir_output = tmp_path / "out"
    new_maker(dir_input, dir_output, exclude=["build/", "dist"]).make_template()
    # excluded directories are not created, with or without a trailing slash
    dir_template = dir_output / "{{ cookiecutter.package_name }}"
    assert sorted(p.name for p in dir_template.iterdir()) == ["src"]


def test_escape_jinja_syntax(tmp_path: Path):
    """
    Jinja2 syntax in the seed project is preserved in the generated project.
    """
    files = {
        "page.html": "{% if x %}{{ x }}{% endif %}{# comment #}\n",
        "data.json": '{"a": {}}\n',
        "run_my_pkg.sh": 'echo ${my_pkg} "{my_pkg}"\n',
        "run.sh": "arr=(1 2)\necho ${#arr[@]}\n",
        "ci.yml": "run: echo ${{ github.sha }}\n",
    }
    dir_input = tmp_path / "my_pkg"
    write_files(dir_input, files)
    dir_output = tmp_path / "template"
    new_maker(dir_input, dir_output).make_template()

    dir_generated = tmp_path / "generated"
    cookiecutter(str(dir_output), no_input=True, output_dir=str(dir_generated))
    for relpath, content in files.items():
        assert dir_generated.joinpath("my_pkg", relpath).read_text() == content


@pytest.mark.parametrize(
    "no_render",
    [
        ["vendor/"],
        ["/*.html", "*.py"],
        ["my_pkg/vendor/*", "index.html"],
        ["**/*.py", "*.html"],
    ],
)
def test_no_render(tmp_path: Path, no_render: list[str]):
    """
    cookiecutter must not render the files we copied without rendering,
    no matter how the git-style no_render patterns are written.
    """
    files = {
        "my_pkg/vendor/tpl.py": "T = '{{ name }}'\n",
        "my_pkg/vendor/[draft].py": "D = '{{ name }}'\n",
        "index.html": "<p>{{ title }}</p>\n",
    }
    dir_input = tmp_path / "my_pkg"
    write_files(dir_input, files)
    if "vendor/" in no_render:
        write_files(dir_input, {"index.html": "<p>title</p>\n"})
        files["index.html"] = "<p>title</p>\n"
    dir_output = tmp_path / "template"
    new_maker(dir_input, dir_output, no_render=no_render).make_template()

    dir_generated = tmp_path / "generated"
    cookiecutter(str(dir_output), no_input=True, output_dir=str(dir_generated))
    for relpath, content in files.items():
        assert dir_generated.joinpath("my_pkg", relpath).read_text() == content


def test_parameter_include_exclude(tmp_path: Path):
    dir_input = tmp_path / "my_pkg"
    write_files(
        dir_input,
        {
            "pyproject.toml": 'name = "my_pkg"\nversion = "0.1.1"\nauthor = "alice@email.com"\n',
            "uv.lock": 'name = "dep"\nversion = "0.1.1"\n',
            "LICENSE": "Copyright alice@email.com\n",
            "my_pkg/0.1.1/my_pkg.txt": "0.1.1 my_pkg\n",
        },
    )
    dir_output = tmp_path / "out"
    Maker(
        dir_input=dir_input,
        dir_output=dir_output,
        parameters=[
            Parameter(selector=["my_pkg"], name="package_name", default="my_pkg"),
            # only applied to pyproject.toml
            Parameter(selector=["0.1.1"], name="version", default="0.1.1", include=["pyproject.toml"]),
            # applied to everything but LICENSE
            Parameter(selector=["alice@email.com"], name="email", default="e", exclude=["LICENSE"]),
            Parameter(selector=["alice"], name="author", default="alice"),
        ],
        verbose=False,
    ).make_template()

    dir_template = dir_output / "{{ cookiecutter.package_name }}"

    def read(relpath: str) -> str:
        return dir_template.joinpath(relpath).read_text()

    assert read("pyproject.toml") == (
        'name = "{{ cookiecutter.package_name }}"\n'
        'version = "{{ cookiecutter.version }}"\n'
        'author = "{{ cookiecutter.email }}"\n'
    )
    assert read("uv.lock") == 'name = "dep"\nversion = "0.1.1"\n'
    # the shorter selector matches inside the excluded longer one
    assert read("LICENSE") == "Copyright {{ cookiecutter.author }}@email.com\n"
    # names always use all parameters, content follows include / exclude
    assert read(
        "{{ cookiecutter.package_name }}/{{ cookiecutter.version }}/{{ cookiecutter.package_name }}.txt"
    ) == "0.1.1 {{ cookiecutter.package_name }}\n"


def test_output_inside_input(tmp_path: Path):
    dir_input = tmp_path / "my_pkg"
    write_files(dir_input, {"my_pkg/__init__.py": ""})
    dir_output = dir_input / "tmp"
    new_maker(dir_input, dir_output).make_template()
    # the output directory is not copied into itself
    assert list_files(dir_output) == [
        "cookiecutter.json",
        "{{ cookiecutter.package_name }}/{{ cookiecutter.package_name }}/__init__.py",
    ]


def test_overwrite(tmp_path: Path):
    dir_input = tmp_path / "my_pkg"
    write_files(dir_input, {"my_pkg/__init__.py": ""})
    dir_output = tmp_path / "out"

    new_maker(dir_input, dir_output).make_template()
    dir_output.joinpath("stale.txt").write_text("")

    # without overwrite
    with pytest.raises(FileExistsError):
        new_maker(dir_input, dir_output).make_template()

    # overwrite a previously generated template
    new_maker(dir_input, dir_output, overwrite=True).make_template()
    assert dir_output.joinpath("stale.txt").exists() is False
    assert dir_output.joinpath("cookiecutter.json").exists()

    # overwrite an empty directory
    dir_empty = tmp_path / "empty"
    dir_empty.mkdir()
    new_maker(dir_input, dir_empty, overwrite=True).make_template()

    # never delete a directory that doesn't look like a generated template
    dir_other = tmp_path / "other"
    write_files(dir_other, {"important.txt": "data"})
    with pytest.raises(ValueError, match="doesn't look like a generated template"):
        new_maker(dir_input, dir_other, overwrite=True).make_template()
    assert dir_other.joinpath("important.txt").exists()

    # never delete the seed project or its parents
    dir_input.joinpath("cookiecutter.json").write_text("{}")
    for dir_bad in [dir_input, tmp_path]:
        with pytest.raises(ValueError, match="is the input directory"):
            new_maker(dir_input, dir_bad, overwrite=True).make_template()
    assert dir_input.joinpath("my_pkg", "__init__.py").exists()

    # never delete the hooks inside the output directory
    dir_template = tmp_path / "template"
    new_maker(dir_input, dir_template).make_template()
    write_files(dir_template, {"hooks/post_gen_project.py": "print('hi')"})
    with pytest.raises(ValueError, match="Hooks directory .* is inside the output"):
        new_maker(dir_input, dir_template, overwrite=True, dir_hooks=dir_template / "hooks").make_template()
    assert dir_template.joinpath("hooks", "post_gen_project.py").exists()

    # output path is a file
    path_file = tmp_path / "file.txt"
    path_file.write_text("")
    with pytest.raises(FileExistsError, match="not a directory"):
        new_maker(dir_input, path_file, overwrite=True).make_template()


def test_readiness_check(tmp_path: Path):
    dir_input = tmp_path / "my_pkg"
    dir_input.mkdir()
    with pytest.raises(FileNotFoundError, match="Input directory"):
        new_maker(tmp_path / "missing", tmp_path / "out").make_template()
    with pytest.raises(FileNotFoundError, match="Hooks directory"):
        new_maker(dir_input, tmp_path / "out", dir_hooks=tmp_path / "hooks").make_template()

    # cookiecutter needs a variable in the project directory name
    dir_plain = tmp_path / "plain"
    dir_plain.mkdir()
    with pytest.raises(ValueError, match="doesn't contain any parameter selector"):
        new_maker(dir_plain, tmp_path / "out").make_template()
    assert (tmp_path / "out").exists() is False


def test_validate_types():
    kwargs = dict(dir_input="my_pkg", dir_output="out", parameters=[])
    # str paths are accepted
    assert Maker(**kwargs).dir_input == Path("my_pkg")
    bad_values = [
        ("dir_hooks", 1, "must be a path"),
        ("parameters", None, "must be a list of Parameter"),
        ("parameters", [{"selector": ["a"]}], "must be a list of Parameter"),
        ("exclude", ".git", "must be a list of strings"),
        ("include", [1], "must be a list of strings"),
        ("overwrite", "false", "must be true or false"),
        ("verbose", "no", "must be true or false"),
    ]
    for key, value, message in bad_values:
        with pytest.raises(ValueError, match=message):
            Maker(**{**kwargs, key: value})

    # from the config file
    with pytest.raises(ValueError, match="'parameters' must be a list"):
        Maker.from_dict({**kwargs, "parameters": None})
    with pytest.raises(ValueError, match="must be an object"):
        Maker.from_dict({**kwargs, "parameters": ["my_pkg"]})
    for param, message in [
        ({"selector": "my_pkg", "name": "a", "default": "a"}, "'selector' must be a list of strings"),
        ({"selector": [""], "name": "a", "default": "a"}, "can't be an empty string"),
        ({"selector": ["a"], "name": "", "default": "a"}, "'name' must be a non-empty string"),
        ({"selector": ["a"], "name": "a", "choice": "a"}, "'choice' must be a list"),
        ({"selector": ["a"], "name": "a", "default": "a", "exclude": "x"}, "'exclude' must be a list of strings"),
        ({"selector": ["a"], "name": "a", "default": "a", "in_cookiecutter_json": "no"}, "must be true or false"),
    ]:
        with pytest.raises(ValueError, match=message):
            Maker.from_dict({**kwargs, "parameters": [param]})


def test_dir_input_dot(tmp_path: Path, monkeypatch):
    dir_input = tmp_path / "my_pkg"
    write_files(dir_input, {"a.txt": "my_pkg"})
    monkeypatch.chdir(dir_input)
    new_maker(Path("."), tmp_path / "out").make_template()
    assert list_files(tmp_path / "out") == [
        "cookiecutter.json",
        "{{ cookiecutter.package_name }}/a.txt",
    ]


def test_non_utf8_text(tmp_path: Path):
    """
    A non UTF-8 text file is copied as is, and cookiecutter must not render it.
    """
    dir_input = tmp_path / "my_pkg"
    dir_input.mkdir()
    dir_input.joinpath("latin1.txt").write_bytes(b"caf\xe9 {{ my_pkg }}\n")
    dir_output = tmp_path / "template"
    new_maker(dir_input, dir_output).make_template()
    dir_generated = tmp_path / "generated"
    cookiecutter(str(dir_output), no_input=True, output_dir=str(dir_generated))
    assert dir_generated.joinpath("my_pkg", "latin1.txt").read_bytes() == b"caf\xe9 {{ my_pkg }}\n"


def test_line_endings(tmp_path: Path):
    dir_input = tmp_path / "my_pkg"
    dir_input.mkdir()
    dir_input.joinpath("crlf.txt").write_bytes(b"my_pkg\r\nb\r\n")
    dir_output = tmp_path / "template"
    new_maker(dir_input, dir_output).make_template()
    path = dir_output / "{{ cookiecutter.package_name }}" / "crlf.txt"
    assert path.read_bytes() == b"{{ cookiecutter.package_name }}\nb\n"


def test_write_cookiecutter_json(tmp_path: Path):
    dir_input = tmp_path / "my_pkg"
    write_files(dir_input, {"logo.png": "", "README.md": "Alice"})
    maker = Maker(
        dir_input=dir_input,
        dir_output=tmp_path / "out",
        parameters=[
            Parameter(selector=["my_pkg"], name="package_name", default="my_pkg"),
            Parameter(selector=["Alice"], name="author", default="Alice", prompt="Author name"),
        ],
        no_render=["*.png"],
        verbose=False,
    )
    maker.make_template()
    assert json.loads(maker.path_cookiecutter_json.read_text()) == {
        "package_name": "my_pkg",
        "author": "Alice",
        "__prompts__": {"author": "Author name"},
        "_copy_without_render": ["logo.png"],
        "_new_lines": "\n",
    }


if __name__ == "__main__":
    from cookiecutter_maker.tests import run_cov_test

    run_cov_test(
        __file__,
        "cookiecutter_maker.maker",
        preview=False,
    )
