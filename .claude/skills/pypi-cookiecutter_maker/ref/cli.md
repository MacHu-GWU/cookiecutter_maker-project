# cookiecutter-maker CLI reference (v1.1.0)

Entry point `cookiecutter-maker = cookiecutter_maker.cli:main` (Python Fire). Requires the `cli` extra: `pip install "cookiecutter-maker[cli]"`, or `uvx --from "cookiecutter-maker[cli]" cookiecutter-maker ...`. Both `--dir_input` and `--dir-input` work. `FileNotFoundError` / `FileExistsError` / `ValueError` (incl. bad JSON) print `Error: ...` and exit 1.

## `make` — generate the template

Precedence: CLI flag (non-`None`) > config file > `Maker` defaults. Relative paths in the config resolve against the config file's dir; relative paths on the CLI resolve against cwd. `parameters` can only come from the config file (missing → error).

| Flag | Type | Default | Notes |
|---|---|---|---|
| `--config` | path | `./cookiecutter-maker.json` if it exists | explicit path must exist |
| `--dir_input` | path | from config | seed project |
| `--dir_output` | path | from config | template destination |
| `--dir_hooks` | path | from config / none | copied to `<dir_output>/hooks` |
| `--include` | patterns | from config / `[]` | `"a,b"` or `'["a","b"]'`; **replaces** config list |
| `--exclude` | patterns | from config / `[]` | same format |
| `--no_render` | patterns | from config / `[]` | same format |
| `--verbose` / `--noverbose` | bool | from config / true | print params and files |
| `--overwrite` / `--nooverwrite` | bool | from config / false | safe delete of old output |

```bash
cookiecutter-maker make --config path/to/cookiecutter-maker.json --overwrite --exclude ".git,.venv,uv.lock" --noverbose
```

## `init` — write a sample config

| Flag | Type | Default | Notes |
|---|---|---|---|
| `--path` | path | `./cookiecutter-maker.json` | parent dirs created |
| `--overwrite` | bool | false | else `FileExistsError` if file exists |

```bash
cookiecutter-maker init --path ./cookiecutter-maker.json
```

## `version` — print installed version

```bash
cookiecutter-maker version
```

## Config file `cookiecutter-maker.json`

JSON object whose keys are `Maker` fields; each `parameters` item has `Parameter` fields (see `public-api.md`). Unknown keys raise an error; no comments allowed.

```json
{
    "dir_input": "./my_project",
    "dir_output": "./tmp",
    "parameters": [
        {"selector": ["my_project"], "name": "project_name", "default": "my_project", "prompt": "Your project name"},
        {"selector": ["version = \"0.1.1\"", "0.1.1"], "name": "version", "default": "0.1.1"},
        {"selector": ["MIT"], "name": "license", "choice": ["MIT", "Apache-2.0", "Proprietary"]}
    ],
    "include": [],
    "exclude": [".git", ".venv", "__pycache__", "*.pyc", "build", "dist"],
    "no_render": ["*.jinja", "*.j2"],
    "dir_hooks": null,
    "verbose": true,
    "overwrite": false
}
```

Then build a project from the result with `uvx cookiecutter ./tmp`.
