import shutil
import difflib
from pathlib import Path
from cookiecutter.main import cookiecutter

from ..vendor.better_pathlib import temp_cwd

from ..maker import Maker


def display_diff(
    path_1: Path,
    path_2: Path,
):
    with path_1.open("r", encoding="utf-8") as f1:
        f1_lines = f1.readlines()
    with path_2.open("r", encoding="utf-8") as f2:
        f2_lines = f2.readlines()

    # Get unified diff
    diff = difflib.unified_diff(
        f1_lines,
        f2_lines,
        fromfile="file1.txt",
        tofile="file2.txt",
        lineterm="",
    )
    # Print diff
    for line in diff:
        print(line)


def compare_directory(
    dir_1: Path,
    dir_2: Path,
):
    """
    Compare two directories recursively.

    :param dir_1: The first directory.
    :param dir_2: The second directory.
    """
    path_list_1 = list(dir_1.glob("**/*.*"))
    path_list_2 = list(dir_2.glob("**/*.*"))
    relpath_list_1 = [str(p.relative_to(dir_1)) for p in path_list_1]
    relpath_list_2 = [str(p.relative_to(dir_2)) for p in path_list_2]
    relpath_list_1.sort()
    relpath_list_2.sort()
    if (len(relpath_list_1) == len(relpath_list_2)) is False:
        raise ValueError("The number of files in the two directories are different.")
    if relpath_list_1 != relpath_list_2:
        raise ValueError("The files in the two directories are different.")

    for p_1 in path_list_1:
        if p_1.is_file():
            p_2 = dir_2.joinpath(p_1.relative_to(dir_1))
            b_1 = p_1.read_bytes()
            try:
                s_1 = b_1.decode("utf-8")
            except UnicodeDecodeError:
                b_2 = p_2.read_bytes()
                if b_1 != b_2:
                    raise ValueError(f"The binary content of {p_1} and {p_2} are different.")
                continue

            with p_1.open("r", encoding="utf-8") as f_1:
                lines_1 = f_1.readlines()
            with p_2.open("r", encoding="utf-8") as f_2:
                lines_2 = f_2.readlines()
            if lines_1 != lines_2:
                display_diff(p_1, p_2)
                raise ValueError(f"The text content of {p_1} and {p_2} are different.")


def run_case(
    maker: Maker,
    dir_expected_template: Path,
    dir_expected_project: Path,
):
    # clean up output (temp) folder
    if maker.dir_output.exists():
        shutil.rmtree(maker.dir_output)

    # seed -> template
    maker.make_template()

    # check template dir
    compare_directory(
        dir_1=dir_expected_template,
        dir_2=maker.dir_template,
    )

    # template -> concrete
    with temp_cwd(maker.dir_output):
        # ref: https://cookiecutter.readthedocs.io/en/stable/advanced/calling_from_python.html
        cookiecutter(
            template=f"{maker.dir_output}",
            no_input=True,
            output_dir=f"{maker.dir_output}",
        )

    # check concrete dir
    compare_directory(
        dir_1=dir_expected_project,
        dir_2=maker.dir_input,
    )
