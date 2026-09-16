#!/usr/bin/env python3
"""Fail the build on any broken internal link.

The course is a hypertext: 27 module READMEs, a master syllabus, project guides
and troubleshooting files all cross-reference each other. A renamed file silently
breaks navigation, and nobody notices until a learner hits a 404.

This runs in CI (see .github/workflows/ci.yml) so a broken link cannot merge.

Usage::

    python tools/check_links.py            # check, print a report
    python tools/check_links.py --quiet    # only print failures
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"__pycache__", ".pytest_cache", ".ruff_cache", ".hypothesis",
             "target", ".git", ".venv", "node_modules"}

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "#", "tel:")


def iter_docs() -> list[Path]:
    return sorted(
        path
        for pattern in ("*.md", "*.txt")
        for path in ROOT.rglob(pattern)
        if not (set(path.parts) & SKIP_DIRS)
    )


def check() -> tuple[int, int, list[str]]:
    broken: list[str] = []
    total = 0
    absolute: list[str] = []

    for doc in iter_docs():
        try:
            text = doc.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        rel_doc = doc.relative_to(ROOT)

        # Hard-coded machine paths make the course non-portable.
        if "file:///" in text or "OneDrive" in text:
            for lineno, line in enumerate(text.splitlines(), 1):
                if "file:///" in line or "OneDrive - " in line:
                    absolute.append(f"{rel_doc}:{lineno}: hard-coded absolute path")

        for match in LINK_RE.finditer(text):
            target = match.group(2)
            if target.startswith(EXTERNAL_PREFIXES):
                continue
            total += 1
            path_part = urllib.parse.unquote(target.split("#", 1)[0])
            if not path_part:
                continue
            resolved = (doc.parent / path_part).resolve()
            if not resolved.exists():
                broken.append(f"{rel_doc}: [{match.group(1)}]({target})")

    return total, len(broken), broken + absolute


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    total, _n_broken, problems = check()

    if problems:
        print(f"LINK CHECK FAILED: {len(problems)} problem(s) across {total} internal links\n")
        for problem in problems:
            print(f"  {problem}")
        return 1

    if not args.quiet:
        print(f"LINK CHECK PASSED: {total} internal links, 0 broken, 0 absolute paths")
    return 0


if __name__ == "__main__":
    sys.exit(main())
