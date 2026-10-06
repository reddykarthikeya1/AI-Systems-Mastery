"""Chapter 16 - Event-driven systems: partitioning and consumer offsets (in-memory model of Kafka semantics).

1. partition_for: stable key -> partition mapping (must not use Python's randomised hash()).
2. Consumer: poll/commit with at-least-once delivery and a dedupe helper.
3. group_by_partition (debugging): per-key ordering is lost.
"""
import zlib

BUGGY = {
    "group_by_partition": '''def group_by_partition(events, n_partitions):
    """events: list of (key, value). Return {partition: [values...]} where each partition keeps events in arrival order
    and all events with the same key land in the same partition."""
    out = {}
    for key, value in events:
        out.setdefault(hash(key) % n_partitions, []).append(value)
    return out''',
}


def partition_for(key, n):
    """Return a partition in range(n) for a str key. The result must be identical across processes and runs (use zlib.crc32
    of the UTF-8 bytes). n < 1 raises ValueError. Same key -> same partition."""
    if n < 1:
        raise ValueError("n must be >= 1")
    return zlib.crc32(key.encode("utf-8")) % n


class Consumer:
    """Reads a log (list). poll(max_n) returns up to max_n (offset, record) pairs from the current position and advances it.
    commit() makes the current position durable. restart() resets the position to the last commit (simulating a crash),
    so uncommitted records are delivered again (at-least-once)."""

    def __init__(self, log):
        self.log = log
        self.position = 0
        self.committed = 0

    def poll(self, max_n):
        batch = [(i, self.log[i]) for i in range(self.position, min(len(self.log), self.position + max_n))]
        self.position += len(batch)
        return batch

    def commit(self):
        self.committed = self.position

    def restart(self):
        self.position = self.committed


def dedupe(batches, key=lambda x: x):
    """Given an iterable of records (possibly redelivered), yield each record whose key has not been seen before, in order."""
    seen = set()
    for r in batches:
        k = key(r)
        if k not in seen:
            seen.add(k)
            yield r


def group_by_partition(events, n_partitions):
    """events: list of (key, value). Return {partition: [values...]} where each partition keeps events in arrival order
    and all events with the same key land in the same partition."""
    out = {}
    for key, value in events:
        out.setdefault(partition_for(key, n_partitions), []).append(value)
    return out


def t_partition_is_stable(m):
    assert m.partition_for("user-42", 12) == zlib.crc32(b"user-42") % 12
    assert all(0 <= m.partition_for(f"k{i}", 7) < 7 for i in range(200))
    assert len({m.partition_for(f"k{i}", 8) for i in range(200)}) == 8
    try:
        m.partition_for("x", 0)
    except ValueError:
        return
    raise AssertionError("n=0 must raise")


def t_consumer_at_least_once(m):
    c = m.Consumer(["a", "b", "c", "d"])
    assert c.poll(2) == [(0, "a"), (1, "b")]
    c.commit()
    assert c.poll(5) == [(2, "c"), (3, "d")] and c.poll(5) == []
    c.restart()
    assert c.poll(1) == [(2, "c")]


def t_consumer_dedupe_makes_processing_idempotent(m):
    c = m.Consumer(["a", "b", "c"])
    seen = c.poll(3)
    c.restart()
    redelivered = c.poll(3)
    assert list(m.dedupe(seen + redelivered, key=lambda r: r[0])) == seen


def t_dedupe_order_and_key(m):
    assert list(m.dedupe([3, 1, 3, 2, 1])) == [3, 1, 2]
    assert list(m.dedupe(["A", "a", "b"], key=str.lower)) == ["A", "b"]


def t_group_by_partition_keeps_key_order(m):
    events = [(f"k{i % 3}", i) for i in range(30)]
    g = m.group_by_partition(events, 4)
    assert sorted(v for vs in g.values() for v in vs) == list(range(30))
    for vs in g.values():
        assert vs == sorted(vs)
    assert g == m.group_by_partition(events, 4)
    owners = {k: [p for p, vs in g.items() if any(events[v][0] == k for v in vs)] for k in ("k0", "k1", "k2")}
    assert all(len(o) == 1 for o in owners.values())
    # the mapping must be the stable crc32 one, so it is identical in every process (str hash() is randomised per process)
    assert all(owners[k] == [zlib.crc32(k.encode()) % 4] for k in owners)
