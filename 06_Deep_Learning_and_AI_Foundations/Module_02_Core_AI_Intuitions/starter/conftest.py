"""Point the module's tests at YOUR code in starter/ instead of the solution."""
import sys
from pathlib import Path

_here = Path(__file__).parent.resolve()
sys.path.insert(0, str(_here))
if (_here / "src").is_dir():
    sys.path.insert(0, str(_here / "src"))
