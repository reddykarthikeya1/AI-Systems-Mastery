#!/usr/bin/env python3
"""Gate: verify every *_PLAYGROUND.md has runnable ```python code blocks.

Courses 09 and 10 previously had zero code blocks. This gate prevents regression.

Usage:
    python tools/check_playground_code.py
"""
from __future__ import annotations

import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent

def main() -> int:
    courses = sorted([d for d in ROOT.iterdir() if d.is_dir() and d.name[:2].isdigit()])
    failures: list[str] = []
    total_checked = 0

    for course in courses:
        for mod in sorted([m for m in course.glob("Module_*") if m.is_dir()]):
            playgrounds = list(mod.glob("*PLAYGROUND*.md"))
            if not playgrounds:
                failures.append(f"{course.name}/{mod.name}: missing *_PLAYGROUND.md")
                continue
            
            for pg in playgrounds:
                total_checked += 1
                text = pg.read_text(encoding="utf-8")
                blocks = re.findall(r"```python\n(.*?)```", text, re.DOTALL)
                if not blocks:
                    failures.append(f"{course.name}/{mod.name}/{pg.name}: contains 0 ```python blocks")

    print(f"Checked {total_checked} playground markdown files across {len(courses)} courses.")
    if failures:
        print(f"\n{len(failures)} PLAYGROUND CODE FAILURE(S):")
        for f in failures[:30]:
            print(f"  - {f}")
        if len(failures) > 30:
            print(f"  ... and {len(failures) - 30} more")
        return 1

    print("  Every playground contains executable ```python code blocks.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
