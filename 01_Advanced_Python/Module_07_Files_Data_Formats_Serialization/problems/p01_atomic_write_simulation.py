"""Problem 01 — Atomic File Write Commit

Target: Production-grade implementation

Example:
    >>> d = {}
    >>> atomic_commit_payload(d, 'config.json', '{"port": 8080}')
    True
    >>> d
    {'config.json': '{"port": 8080}'}

Hints:
    Hint 1: The point of "atomic" is that an observer of `staging_dir` should
        never see a half-written `target_file` — write the payload somewhere
        else first, then swap it into place in one step.
    Hint 2: Write the payload to a temporary key (e.g. `f"{target_file}.tmp"`)
        in `staging_dir`, then use `dict.pop` to move that value onto
        `target_file` and remove the temporary key in the same operation.
    Hint 3: After the commit, `target_file` must hold `payload` exactly and
        the `.tmp` key must no longer exist in `staging_dir` — the tests
        check both conditions, plus that the function returns `True`.
"""

from __future__ import annotations


def atomic_commit_payload(staging_dir: dict, target_file: str, payload: str) -> bool:
    raise NotImplementedError('Implement atomic_commit_payload')
