# -*- coding: utf-8 -*-

from pathlib import Path
from rich.console import Console
from rich.table import Table

p_root = Path("/tmp")


class PatternMatchExample:
    def __init__(self):
        self.console = Console()
        self.table = Table()
        self.table.add_column("Relpath", no_wrap=True)
        self.table.add_column("Pattern", no_wrap=True)
        self.table.add_column("Match")

    def debug_pattern(self, relpath: Path, pattern: str):
        flag = relpath.match(pattern)
        self.table.add_row(str(relpath), pattern, str(flag))

    def show(self):
        self.console.print(self.table)

pe = PatternMatchExample()

# ------------------------------------------------------------------------------
# p1 = Path("/tmp/test.py").relative_to(p_root)
# p2 = Path("/tmp/cookiecutter_maker/test.py").relative_to(p_root)
# p3 = Path("/tmp/cookiecutter_maker/tests/test.py").relative_to(p_root)

# pattern = "cookiecutter_maker/test.py"
# print(p1.match(pattern))
# print(p2.match(pattern))
# print(p3.match(pattern))

# pe.debug_pattern(p2, "cookiecutter_maker/test.py")
# pe.debug_pattern(p2, "cookiecutter_maker/*")
# pe.debug_pattern(p2, "./cookiecutter_maker/test.py")
# pe.debug_pattern(p2, "./cookiecutter_maker/*")
# print(p2.match("cookiecutter_maker/*"))


# ------------------------------------------------------------------------------
# p1 = Path("/tmp/cookiecutter_maker").relative_to(p_root)
# pattern = "cookiecutter_maker/test.py"
# print(p1.match("cookiecutter_maker/*"))
# print(p2.match("test.py"))
# print(p2.match("cookiecutter_maker/test.py"))



# ------------------------------------------------------------------------------
p1 = Path("/tmp/build").relative_to(p_root)
p2 = Path("/tmp/my_package/build").relative_to(p_root)
p3 = Path("/tmp/my_package/build.py").relative_to(p_root)

# pe.debug_pattern(p1, "**/*build")
# pe.debug_pattern(p2, "**/*build")

# pattern = "**/build"
# pe.debug_pattern(p1, pattern)
# pe.debug_pattern(p2, pattern)

pattern = "build/"
pe.debug_pattern(p1, pattern)
pe.debug_pattern(p2, pattern)
pe.debug_pattern(p3, pattern)

# ------------------------------------------------------------------------------
pe.show()
