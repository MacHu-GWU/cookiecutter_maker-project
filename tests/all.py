# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from cookiecutter_maker.tests import run_cov_test

    run_cov_test(
        __file__,
        "cookiecutter_maker",
        is_folder=True,
        preview=False,
    )
