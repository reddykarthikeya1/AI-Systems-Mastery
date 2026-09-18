"""Import resolution for this module's problem bank.

The learner's own file must be what gets graded, and an unimplemented stub
must fail. That cannot be left to sys.path ordering: the repo sets
`--import-mode=importlib`, under which pytest resolved `from p01_... import ...`
to `solutions/` and every stub reported green from the repo root.

So the file that answers the import is chosen here, explicitly, by loading it
from a known path and registering it in sys.modules before collection. Nothing
downstream gets a say.

    pytest tests/                          grades the learner   (stub -> fail)
    ACADEMY_GRADE_SOLUTION=1 pytest tests/ grades the reference (-> pass)
"""

import importlib.util
import os
import sys
from pathlib import Path

_problems = Path(__file__).resolve().parent.parent
_graded = _problems / "solutions" if os.environ.get("ACADEMY_GRADE_SOLUTION") == "1" else _problems

for _path in sorted(_graded.glob("p*.py")):
    _spec = importlib.util.spec_from_file_location(_path.stem, _path)
    if _spec is None or _spec.loader is None:
        continue
    _module = importlib.util.module_from_spec(_spec)
    # Registered before exec so a module that imports itself resolves.
    sys.modules[_path.stem] = _module
    _spec.loader.exec_module(_module)
