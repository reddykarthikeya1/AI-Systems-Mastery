"""Point the module's tests at YOUR code in starter/ instead of the solution."""
import sys
import types
from pathlib import Path

_here = Path(__file__).parent.resolve()
sys.path.insert(0, str(_here))
if (_here / "src").is_dir():
    sys.path.insert(0, str(_here / "src"))

# Package alias support for namespaced solutions
if (
    _here.parent.name == "Module_26_Final_Capstone_Project"
    and "capstone_platform" not in sys.modules
):
    pkg = types.ModuleType("capstone_platform")
    pkg.__path__ = [str(_here), str(_here.parent / "capstone_platform")]
    sys.modules["capstone_platform"] = pkg
