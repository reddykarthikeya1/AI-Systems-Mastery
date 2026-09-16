"""Global pytest root configuration for all 27 System Design modules.

Two distinct import modes, and the distinction is the whole point:

**Running from the course root** — every ``project_solution`` directory goes on
``sys.path`` so the shipped tests exercise the reference implementations. This is
the maintainer's mode, and it is what ``pytest -q`` from here does.

**Running from inside a ``starter/`` directory** — imports must resolve to the
*learner's* code instead. A plain ``sys.path.insert`` in ``starter/conftest.py``
is not enough: pytest loads conftest files along the **test file's** path, and
the test lives in ``project_solution/``, so a conftest sitting in ``starter/`` is
never imported at all. Worse, pytest's default ``prepend`` import mode puts the
test file's own directory at ``sys.path[0]``, which is exactly the solution
directory we are trying to shadow.

The fix is a ``MetaPathFinder``, which is consulted *before* ``sys.path`` and
therefore wins unconditionally. Without it a learner runs the tests against an
unimplemented stub, sees green, and concludes they are done - the single worst
failure mode a course can have, because it certifies non-work.
"""

from __future__ import annotations

import sys
from pathlib import Path

root_dir = Path(__file__).parent.resolve()
cwd = Path.cwd().resolve()

if cwd.name == "starter" or "starter" in cwd.parts:
    starter_dir = (
        cwd if cwd.name == "starter" else next(p for p in [cwd, *cwd.parents] if p.name == "starter")
    )
    sys.path.insert(0, str(starter_dir))
    if (starter_dir / "src").is_dir():
        sys.path.insert(0, str(starter_dir / "src"))

    from importlib.abc import MetaPathFinder
    from importlib.util import spec_from_file_location

    class _StarterFinder(MetaPathFinder):
        """Resolve any importable name to the learner's starter file when one exists.

        Sits on ``sys.meta_path`` ahead of the standard path finder, so it takes
        precedence over whatever pytest prepends to ``sys.path``.
        """

        def __init__(self, base_dir: Path) -> None:
            self.base_dir = base_dir

        def find_spec(self, fullname: str, path=None, target=None):
            search_dirs = [self.base_dir]
            if (self.base_dir / "src").is_dir():
                search_dirs.append(self.base_dir / "src")

            parts = fullname.split(".")
            for sdir in search_dirs:
                candidate = sdir.joinpath(*parts).with_suffix(".py")
                if candidate.is_file():
                    return spec_from_file_location(fullname, str(candidate))
                package_init = sdir.joinpath(*parts, "__init__.py")
                if package_init.is_file():
                    return spec_from_file_location(
                        fullname,
                        str(package_init),
                        submodule_search_locations=[str(package_init.parent)],
                    )
            return None

    sys.meta_path.insert(0, _StarterFinder(starter_dir))
else:
    for p in root_dir.rglob("*"):
        if (
            p.is_dir()
            and (p.name in {"src", "project_solution"} or p.name.startswith("Module_"))
            and "starter" not in p.parts
            and "debug_lab" not in p.parts
            and str(p) not in sys.path
        ):
            sys.path.insert(0, str(p))
