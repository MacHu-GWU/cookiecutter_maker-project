# -*- coding: utf-8 -*-

import shutil
from pathlib import Path

from ..maker import Maker

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
        p_2 = dir_2.joinpath(p_1.relative_to(dir_1))
        if p_1.read_bytes() != p_2.read_bytes():
            raise ValueError(f"The content of {p_1} and {p_2} are different.")

def run_case(
    maker: Maker,
    dir_expected: Path,
):
    if maker.dir_output.exists():
        shutil.rmtree(maker.dir_output)
    maker.make_template()
    # compare_directory(
    #     dir_1=maker.dir_template,
    #     dir_2=dir_expected,
    # )
