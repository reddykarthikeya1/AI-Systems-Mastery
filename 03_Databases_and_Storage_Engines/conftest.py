"""Global pytest root configuration for all 24 modules."""

from __future__ import annotations

import sys
from pathlib import Path

root_dir = Path(__file__).parent.resolve()
cwd = Path.cwd().resolve()

# If running from inside a starter directory, prioritize that starter above everything
if cwd.name == "starter" or "starter" in cwd.parts:
    starter_dir = cwd if cwd.name == "starter" else next(p for p in [cwd, *cwd.parents] if p.name == "starter")
    sys.path.insert(0, str(starter_dir))
    if (starter_dir / "src").is_dir():
        sys.path.insert(0, str(starter_dir / "src"))

    from importlib.abc import MetaPathFinder
    from importlib.util import spec_from_file_location

    class _StarterFinder(MetaPathFinder):
        def __init__(self, base_dir: Path) -> None:
            self.base_dir = base_dir

        def find_spec(self, fullname: str, path=None, target=None):
            search_dirs = [self.base_dir]
            if (self.base_dir / "src").is_dir():
                search_dirs.append(self.base_dir / "src")

            parts = fullname.split(".")
            for sdir in search_dirs:
                cand_file = sdir.joinpath(*parts).with_suffix(".py")
                if cand_file.is_file():
                    return spec_from_file_location(fullname, str(cand_file))
                cand_init = sdir.joinpath(*parts, "__init__.py")
                if cand_init.is_file():
                    return spec_from_file_location(
                        fullname, str(cand_init), submodule_search_locations=[str(cand_init.parent)]
                    )
            return None

    sys.meta_path.insert(0, _StarterFinder(starter_dir))
else:
    for p in root_dir.rglob("*"):
        if (
            p.is_dir()
            and (p.name in {"src", "project_solution"} or p.name.startswith("Module_"))
            and str(p) not in sys.path
        ):
            sys.path.insert(0, str(p))
