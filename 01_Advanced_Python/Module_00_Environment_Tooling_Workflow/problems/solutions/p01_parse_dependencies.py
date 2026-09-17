"""Problem 01 — Parse pyproject.toml Dependencies

Target: Production-grade implementation

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases and type checks.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def parse_dependencies(spec_lines: list[str]) -> dict[str, str]:
    res = {}
    for line in spec_lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        for op in ['>=', '<=', '==', '!=', '~=', '>', '<']:
            if op in line:
                p, v = line.split(op, 1)
                res[p.strip().lower()] = f"{op}{v.strip()}"
                break
        else:
            res[line.lower()] = '*'
    return res
