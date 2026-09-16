import sys
from pathlib import Path

# Ensure starter/ directory is prioritized on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))
