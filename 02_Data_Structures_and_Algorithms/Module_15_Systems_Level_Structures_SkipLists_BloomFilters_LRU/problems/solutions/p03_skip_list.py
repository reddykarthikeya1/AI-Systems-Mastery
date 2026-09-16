"""Reference solution — Problem 03: Skip List: Insert, Search, Delete

Pattern:    Skip list
Complexity: Expected O(log n) per operation, Space O(n)
"""

from __future__ import annotations


def simulate_skip_list(ops: list[tuple[str, int]]) -> list[bool | list[int]]:
    import random

    MAX_LEVEL = 16
    # A fixed seed: the structure is randomised by design, but a test failure
    # you cannot reproduce is not a test failure you can fix.
    rng = random.Random(0xC0FFEE)

    head: dict = {"value": None, "next": [None] * MAX_LEVEL}
    out: list[bool | list[int]] = []

    def random_level() -> int:
        level = 1
        while level < MAX_LEVEL and rng.random() < 0.5:
            level += 1
        return level

    def find_path(value: int) -> list[dict]:
        # The last node before `value` on each level - the insertion path.
        path: list[dict] = [head] * MAX_LEVEL
        node = head
        for lvl in range(MAX_LEVEL - 1, -1, -1):
            nxt = node["next"][lvl]
            while nxt is not None and nxt["value"] < value:
                node = nxt
                nxt = node["next"][lvl]
            path[lvl] = node
        return path

    for name, value in ops:
        if name == "insert":
            path = find_path(value)
            after = path[0]["next"][0]
            if after is not None and after["value"] == value:
                continue                    # already present: idempotent
            lvl = random_level()
            node = {"value": value, "next": [None] * MAX_LEVEL}
            for i in range(lvl):
                node["next"][i] = path[i]["next"][i]
                path[i]["next"][i] = node
        elif name == "search":
            path = find_path(value)
            after = path[0]["next"][0]
            out.append(after is not None and after["value"] == value)
        elif name == "delete":
            path = find_path(value)
            target = path[0]["next"][0]
            if target is None or target["value"] != value:
                out.append(False)
            else:
                for i in range(MAX_LEVEL):
                    if path[i]["next"][i] is target:
                        path[i]["next"][i] = target["next"][i]
                out.append(True)
        elif name == "items":
            values: list[int] = []
            node = head["next"][0]
            while node is not None:
                values.append(node["value"])
                node = node["next"][0]
            out.append(values)
        else:
            raise ValueError(f"unknown operation: {name!r}")

    return out
