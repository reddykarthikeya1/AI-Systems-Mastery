import sys
from pathlib import Path

root_dir = Path(__file__).parent.resolve()
for p in root_dir.rglob("*"):
    if p.is_dir() and (p.name in {"src", "project_solution"} or p.name.startswith("Module_")) and "starter" not in p.parts:
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
