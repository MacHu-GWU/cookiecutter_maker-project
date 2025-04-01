.. _release_history:

Release and Version History
==============================================================================


Backlog (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.0.1 (2025-04-01)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**💥Breaking Changes**

- Rework the API:
    - now it uses more reliable ``pathspec`` to match files.
    - now it support using ``selector`` to precisely select the sub string you want to substitute.
- Drop Python3.8 support. Now only support Python3.9+.

**Features and Improvements**

- Add ``Parameter`` to the public API.

**Minor Improvements**

- Add a comprehensive integration test.


0.3.1 (2023-06-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- allow user to specify the default value of the parameter.
- add ``ignore_mapper_error`` and ``skip_mapper_prompt`` arguments to ``Maker.new(..)``.
- add ``cleanup_output_dir`` argument to ``Maker.templaterize(...)``.

**Miscellaneous**

- add test on Python3.7, 3.8, 3.9, 3.10


0.2.1 (2023-02-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- also generate the ``cookiecutter.json`` file.

**Minor Improvements**

- update documents.


0.1.1 (2023-02-14)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
