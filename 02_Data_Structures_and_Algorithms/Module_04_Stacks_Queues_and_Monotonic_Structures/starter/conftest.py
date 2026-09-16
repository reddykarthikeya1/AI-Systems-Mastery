"""Point the module's tests at YOUR code in starter/ instead of the solution.

This alone is not sufficient - pytest loads conftest files along the *test
file's* path, and the shipped tests live in project_solution/. The root
conftest.py installs a MetaPathFinder that actually wins the resolution. This
file exists so that running pytest from here also works when the root conftest
is bypassed.
"""
import sys
from pathlib import Path

_here = Path(__file__).parent.resolve()
sys.path.insert(0, str(_here))
if (_here / "src").is_dir():
    sys.path.insert(0, str(_here / "src"))
