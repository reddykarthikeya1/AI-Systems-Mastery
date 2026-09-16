"""Root pytest configuration for all 15 DSA modules.

Two distinct import modes, and the distinction is the whole point.

**Running from the course root** — every ``project_solution`` and ``problems``
directory goes on ``sys.path`` so the shipped tests exercise the reference
implementations. This is the maintainer's mode, and it is what ``pytest -q``
from here does.

**Running from inside a ``starter/`` or ``problems/`` directory** — imports must
resolve to the *learner's* code instead. A plain ``sys.path.insert`` in a
``starter/conftest.py`` is not enough: pytest loads conftest files along the
**test file's** path, and the test lives in ``project_solution/``, so a conftest
sitting in ``starter/`` is never imported at all. Worse, pytest's default
``prepend`` import mode puts the test file's own directory at ``sys.path[0]``,
which is exactly the directory we are trying to shadow.

The fix is a ``MetaPathFinder``, which is consulted *before* ``sys.path`` and
therefore wins unconditionally.

Why this matters more than it sounds: without it a learner runs the shipped
tests against a stub full of ``NotImplementedError``, sees green, and concludes
they are done. That is the single worst failure mode a course can have, because
it certifies non-work. ``tools/check_integrity.py`` asserts the property across
all 15 modules so it cannot regress silently.
"""

from __future__ import annotations

import sys
from pathlib import Path

root_dir = Path(__file__).parent.resolve()
cwd = Path.cwd().resolve()

_LEARNER_DIRS = ("starter", "problems")


def _learner_root(path: Path) -> Path | None:
    """The nearest enclosing starter/ or problems/ directory, if any."""
    for candidate in [path, *path.parents]:
        if candidate.name in _LEARNER_DIRS:
            return candidate
    return None


_base = _learner_root(cwd)

if _base is not None:
    sys.path.insert(0, str(_base))
    if (_base / "src").is_dir():
        sys.path.insert(0, str(_base / "src"))

    from importlib.abc import MetaPathFinder
    from importlib.util import spec_from_file_location

    class _LearnerFinder(MetaPathFinder):
        """Resolve any importable name to the learner's file when one exists.

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

    sys.meta_path.insert(0, _LearnerFinder(_base))
else:
    # Note which directories are deliberately EXCLUDED here.
    #
    # ``problems/`` holds the learner's stubs, and ``problems/solutions/`` holds
    # the reference implementations under the *same module names*. Putting both
    # on sys.path would make resolution depend on rglob ordering, so a root-mode
    # run would sometimes verify the stubs and sometimes the solutions. Only
    # ``solutions`` goes on the path; the stubs are reachable only in learner
    # mode, via the MetaPathFinder above.
    for p in root_dir.rglob("*"):
        if (
            p.is_dir()
            and (
                p.name in {"src", "project_solution", "solutions"}
                or p.name.startswith("Module_")
            )
            and "starter" not in p.parts
            and "debug_lab" not in p.parts
            and str(p) not in sys.path
        ):
            sys.path.insert(0, str(p))
