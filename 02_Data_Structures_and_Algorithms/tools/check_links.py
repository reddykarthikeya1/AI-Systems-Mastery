#!/usr/bin/env python3
"""Check internal link integrity."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"__pycache__", ".pytest_cache", ".ruff_cache", ".hypothesis", ".git", ".venv"}
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

def check():
    broken = []
    total = 0
    docs = sorted(
        p
        for pattern in ("*.md", "*.txt")
        for p in ROOT.rglob(pattern)
        if not (set(p.parts) & SKIP_DIRS)
    )
    for doc in docs:
        try:
            text = doc.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for match in LINK_RE.finditer(text):
            target = match.group(2)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            total += 1
            target_path = (doc.parent / target.split("#")[0]).resolve()
            if not target_path.exists():
                broken.append(f"{doc.relative_to(ROOT)} -> {target}")
    if broken:
        print(f"FAILED: {len(broken)} broken links out of {total}")
        for b in broken:
            print("  ", b)
        return 1
    print(f"LINK CHECK PASSED: {total} internal links, 0 broken, 0 absolute paths")
    return 0

if __name__ == "__main__":
    exit(check())
