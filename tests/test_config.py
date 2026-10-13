# -*- coding: utf-8 -*-

import json
from pathlib import Path

import pytest

from cookiecutter_maker.parameter import Parameter
from cookiecutter_maker.maker import Maker
from cookiecutter_maker.config import (
    CONFIG_FILENAME,
    SAMPLE_CONFIG,
    resolve_path,
    normalize_list,
    find_config,
    read_config,
    apply_overrides,
    load_maker,
    write_sample_config,
)


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


PARAMETERS = [{"selector": ["my_package"], "name": "package_name", "default": "x"}]


def test_parameter_from_dict():
    param = Parameter.from_dict(PARAMETERS[0])
    assert param.name == "package_name"

    with pytest.raises(ValueError, match="Unknown Parameter field"):
        Parameter.from_dict({**PARAMETERS[0], "defualt": "typo"})
    with pytest.raises(ValueError, match="Missing required Parameter field"):
        Parameter.from_dict({"selector": ["a"]})


def test_maker_from_dict():
    maker = Maker.from_dict(
        {
            "dir_input": "a",
            "dir_output": "b",
            "parameters": PARAMETERS + [Parameter(selector=["v"], name="v", default="v")],
            "dir_hooks": "c",
        }
    )
    assert maker.dir_input == Path("a")
    assert maker.dir_hooks == Path("c")
    assert all(isinstance(p, Parameter) for p in maker.parameters)
    assert maker.overwrite is False

    with pytest.raises(ValueError, match="Unknown Maker field"):
        Maker.from_dict({"dir_input": "a", "dir_output": "b", "parameters": [], "exculde": []})
    with pytest.raises(ValueError, match="Missing required Maker field"):
        Maker.from_dict({"dir_input": "a", "parameters": []})


def test_resolve_path(tmp_path: Path):
    assert resolve_path("a/../b", tmp_path) == tmp_path / "b"
    assert resolve_path("/abs", tmp_path) == Path("/abs")
    assert resolve_path("~", tmp_path) == Path.home()


def test_normalize_list():
    assert normalize_list(".git, .venv,") == [".git", ".venv"]
    assert normalize_list((".git", ".venv")) == [".git", ".venv"]
    assert normalize_list([]) == []


def test_find_config(tmp_path: Path):
    # no default config file
    assert find_config(cwd=tmp_path) is None
    # explicit config file that doesn't exist
    with pytest.raises(FileNotFoundError):
        find_config(config="missing.json", cwd=tmp_path)
    # default config file
    path = tmp_path / CONFIG_FILENAME
    write_json(path, {})
    assert find_config(cwd=tmp_path) == path
    # explicit config file, relative to cwd
    path = tmp_path / "sub" / "my.json"
    write_json(path, {})
    assert find_config(config="sub/my.json", cwd=tmp_path) == path


def test_read_config(tmp_path: Path):
    path = tmp_path / "sub" / CONFIG_FILENAME
    write_json(path, {"dir_input": "./seed", "dir_output": "/abs/out", "dir_hooks": None})
    data = read_config(path)
    # relative to the config file directory, not cwd
    assert data["dir_input"] == str(tmp_path / "sub" / "seed")
    assert data["dir_output"] == "/abs/out"
    assert data["dir_hooks"] is None

    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match="must be a JSON object"):
        read_config(path)


def test_apply_overrides(tmp_path: Path):
    data = {"dir_input": "/a", "exclude": [".git"], "verbose": True}
    new_data = apply_overrides(
        data,
        dict(dir_input="seed", exclude=".venv,dist", verbose=False, dir_output=None),
        cwd=tmp_path,
    )
    assert new_data == {
        "dir_input": str(tmp_path / "seed"),  # relative to cwd
        "exclude": [".venv", "dist"],  # replace, not extend
        "verbose": False,  # False is a real value, not "not provided"
    }
    assert data["dir_input"] == "/a"  # original dict is not mutated


def test_load_maker(tmp_path: Path):
    dir_project = tmp_path / "project"
    write_json(
        dir_project / CONFIG_FILENAME,
        {
            "dir_input": "./seed",
            "dir_output": "./out",
            "parameters": PARAMETERS,
            "exclude": [".git"],
        },
    )

    # config file only, found in cwd
    maker = load_maker(cwd=dir_project)
    assert maker.dir_input == dir_project / "seed"
    assert maker.dir_output == dir_project / "out"
    assert maker.exclude == [".git"]
    assert maker.verbose is True  # Maker default

    # cli overrides config file, config file path is relative to cwd
    maker = load_maker(
        config="project/cookiecutter-maker.json",
        cwd=tmp_path,
        dir_output="elsewhere",
        exclude=None,
        verbose=False,
    )
    assert maker.dir_input == dir_project / "seed"
    assert maker.dir_output == tmp_path / "elsewhere"
    assert maker.exclude == [".git"]
    assert maker.verbose is False

    # no config file, parameters can't come from cli
    with pytest.raises(ValueError, match="'parameters' is not defined"):
        load_maker(cwd=tmp_path, dir_input="a", dir_output="b")


def test_write_sample_config(tmp_path: Path):
    path = write_sample_config(cwd=tmp_path)
    assert path == tmp_path / CONFIG_FILENAME
    assert json.loads(path.read_text()) == SAMPLE_CONFIG
    with pytest.raises(FileExistsError):
        write_sample_config(cwd=tmp_path)
    write_sample_config(cwd=tmp_path, overwrite=True)

    path = write_sample_config(path="sub/x.json", cwd=tmp_path)
    assert path == tmp_path / "sub" / "x.json"

    # the sample config is a valid Maker config
    maker = load_maker(cwd=tmp_path)
    assert maker.dir_input == tmp_path / "my_project"


def test_overwrite(tmp_path: Path):
    dir_input = tmp_path / "my_package"
    dir_input.joinpath("my_package").mkdir(parents=True)
    dir_input.joinpath("my_package", "__init__.py").write_text("")
    dir_output = tmp_path / "out"
    dir_output.mkdir()
    dir_output.joinpath("stale.txt").write_text("")

    kwargs = dict(dir_input=dir_input, parameters=PARAMETERS, verbose=False)
    with pytest.raises(FileExistsError):
        Maker.from_dict({**kwargs, "dir_output": dir_output}).make_template()

    Maker.from_dict({**kwargs, "dir_output": dir_output, "overwrite": True}).make_template()
    assert dir_output.joinpath("stale.txt").exists() is False
    assert dir_output.joinpath("cookiecutter.json").exists()

    # never delete the seed project
    for dir_bad in [dir_input, tmp_path]:
        with pytest.raises(ValueError, match="refuse to overwrite"):
            Maker.from_dict({**kwargs, "dir_output": dir_bad, "overwrite": True}).make_template()
    assert dir_input.joinpath("my_package", "__init__.py").exists()


if __name__ == "__main__":
    from cookiecutter_maker.tests import run_cov_test

    run_cov_test(
        __file__,
        "cookiecutter_maker.config",
        preview=False,
    )
