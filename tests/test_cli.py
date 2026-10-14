# -*- coding: utf-8 -*-

import sys
import json
from pathlib import Path

import pytest

from cookiecutter_maker import __version__
from cookiecutter_maker.config import CONFIG_FILENAME
from cookiecutter_maker.cli import main

pytest.importorskip("fire")


def run_cli(monkeypatch, cwd: Path, *args: str):
    monkeypatch.chdir(cwd)
    monkeypatch.setattr(sys, "argv", ["cookiecutter-maker", *args])
    main()


def test_cli(tmp_path: Path, monkeypatch, capsys):
    run_cli(monkeypatch, tmp_path, "version")
    assert capsys.readouterr().out.strip() == __version__

    # init
    run_cli(monkeypatch, tmp_path, "init")
    path_config = tmp_path / CONFIG_FILENAME
    assert path_config.exists()

    # init again, error without traceback
    with pytest.raises(SystemExit) as e:
        run_cli(monkeypatch, tmp_path, "init")
    assert e.value.code == 1
    assert "already exists" in capsys.readouterr().err
    run_cli(monkeypatch, tmp_path, "init", "--overwrite")

    # make, the seed project doesn't exist yet
    with pytest.raises(SystemExit):
        run_cli(monkeypatch, tmp_path, "make")
    assert "does not exist" in capsys.readouterr().err

    # make, cli arguments override the config file
    dir_seed = tmp_path / "my_project-seed"
    dir_seed.joinpath("my_project").mkdir(parents=True)
    dir_seed.joinpath("my_project", "README.txt").write_text("my_project 0.1.1")
    dir_seed.joinpath(".venv").mkdir()
    dir_seed.joinpath(".venv", "x.txt").write_text("")
    for _ in range(2):  # second run needs --overwrite
        run_cli(
            monkeypatch,
            tmp_path,
            "make",
            "--dir-input=my_project-seed",
            "--dir_output=out",
            "--exclude=.git,.venv",
            "--noverbose",
            "--overwrite",
        )
    dir_out = tmp_path / "out"
    assert "Template is generated at" in capsys.readouterr().out
    assert dir_out.joinpath("{{ cookiecutter.project_name }}-seed", "{{ cookiecutter.project_name }}", "README.txt").read_text() == (
        "{{ cookiecutter.project_name }} {{ cookiecutter.version }}"
    )
    assert dir_out.joinpath("{{ cookiecutter.project_name }}-seed", ".venv").exists() is False
    assert json.loads(dir_out.joinpath("cookiecutter.json").read_text())["license"] == [
        "MIT",
        "Apache-2.0",
        "Proprietary",
    ]


if __name__ == "__main__":
    from cookiecutter_maker.tests import run_cov_test

    run_cov_test(
        __file__,
        "cookiecutter_maker.cli",
        preview=False,
    )
