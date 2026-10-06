"""Chapter 00 - Mental model: names, objects, mutability.

1. same_object_groups: find which names point at the same object.
2. snapshot: copy nested lists/dicts so later mutation of the original cannot leak in.
3. add_tag (debugging): this function shares state between calls. Find out why and fix it.
"""

BUGGY = {
    "add_tag": '''def add_tag(tag, tags=[]):
    """Return a list containing `tag` appended to `tags` (a new list when `tags` is omitted)."""
    tags.append(tag)
    return tags''',
}


def same_object_groups(objs):
    """Return a list of index lists, one per group of 2+ positions in `objs` holding the *same object* (identity, not equality).
    Groups ordered by first index; indices ascending. [a, b, a] -> [[0, 2]] when a is not b."""
    seen = {}
    for i, o in enumerate(objs):
        seen.setdefault(id(o), []).append(i)
    return sorted((v for v in seen.values() if len(v) > 1), key=lambda v: v[0])


def snapshot(value):
    """Return a deep copy of nested lists, dicts and tuples without using the `copy` module. Other values are returned as is."""
    if isinstance(value, list):
        return [snapshot(v) for v in value]
    if isinstance(value, dict):
        return {k: snapshot(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return tuple(snapshot(v) for v in value)
    return value


def add_tag(tag, tags=None):
    """Return a list containing `tag` appended to `tags` (a new list when `tags` is omitted)."""
    if tags is None:
        tags = []
    tags.append(tag)
    return tags


def t_same_object_groups_identity(m):
    a, b = [1], [1]
    assert m.same_object_groups([a, b, a]) == [[0, 2]]
    assert m.same_object_groups([a, b]) == []
    x = object()
    assert m.same_object_groups([x, a, x, a, x]) == [[0, 2, 4], [1, 3]]


def t_snapshot_is_independent(m):
    src = {"a": [1, {"b": [2, 3]}], "t": ([4], 5)}
    snap = m.snapshot(src)
    assert snap == src and snap is not src
    src["a"][1]["b"].append(99)
    src["t"][0].append(7)
    assert snap["a"][1]["b"] == [2, 3] and snap["t"][0] == [4]


def t_snapshot_keeps_scalars(m):
    assert m.snapshot(5) == 5 and m.snapshot("x") == "x" and m.snapshot(None) is None


def t_add_tag_no_shared_state(m):
    assert m.add_tag("a") == ["a"]
    assert m.add_tag("b") == ["b"]
    mine = ["x"]
    assert m.add_tag("y", mine) is mine and mine == ["x", "y"]
