"""Reference Solution — Problem 01: solve_systems_task

Topic: Decorators Generators Context Managers
"""

from __future__ import annotations

def solve_systems_task(data: list[int | str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in data:
        key = str(item).strip()
        if key:
            counts[key] = counts.get(key, 0) + 1
    return counts

