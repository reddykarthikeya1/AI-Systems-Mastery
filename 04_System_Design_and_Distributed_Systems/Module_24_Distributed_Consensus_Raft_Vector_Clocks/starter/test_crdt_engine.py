"""Tests for the CRDT engine.

The important tests are the algebraic ones. A CRDT is correct because its merge
is commutative, associative and idempotent - so rather than testing a handful
of scenarios, these check the laws directly over every permutation of updates.
If the laws hold, convergence under any network behaviour follows.
"""

from __future__ import annotations

import itertools
import random

import pytest
from crdt_engine import (
    GCounter,
    GSet,
    LWWRegister,
    OperationLog,
    ORSet,
    PNCounter,
    TextCRDT,
    TwoPhaseSet,
    converge,
    position_between,
)


def readable(state):
    value = state.value() if hasattr(state, "value") else state.text()
    return frozenset(value) if isinstance(value, set) else value


def merge_all(replicas, order):
    state = replicas[order[0]].copy()
    for index in order[1:]:
        state = state.merge(replicas[index])
    return state


# ---------------------------------------------------------------------------
# the three laws, checked directly on every type
# ---------------------------------------------------------------------------


def build_counters():
    a, b, c = GCounter(), GCounter(), GCounter()
    a.increment("a", 3)
    b.increment("b", 5)
    c.increment("c", 2)
    b.increment("a", 1)
    return [a, b, c]


def build_pn_counters():
    a, b, c = PNCounter(), PNCounter(), PNCounter()
    a.increment("a", 10)
    b.decrement("b", 3)
    c.increment("c", 7)
    c.decrement("c", 2)
    return [a, b, c]


def build_gsets():
    a, b, c = GSet(), GSet(), GSet()
    a.add("x")
    b.add("y")
    c.add("z")
    b.add("x")
    return [a, b, c]


def build_or_sets():
    a, b, c = ORSet(), ORSet(), ORSet()
    a.add("apple", "t1")
    b.add("bread", "t2")
    c.add("apple", "t3")
    return [a, b, c]


def build_registers():
    a = LWWRegister()
    b = LWWRegister()
    c = LWWRegister()
    a.write("first", 1, "a")
    b.write("second", 2, "b")
    c.write("third", 2, "c")          # same timestamp as b: tie-break on id
    return [a, b, c]


BUILDERS = [
    ("GCounter", build_counters),
    ("PNCounter", build_pn_counters),
    ("GSet", build_gsets),
    ("ORSet", build_or_sets),
    ("LWWRegister", build_registers),
]


@pytest.mark.parametrize("name,build", BUILDERS)
def test_merge_is_commutative(name, build):
    a, b, _ = build()
    assert readable(a.merge(b)) == readable(b.merge(a)), f"{name} merge is order-dependent"


@pytest.mark.parametrize("name,build", BUILDERS)
def test_merge_is_associative(name, build):
    a, b, c = build()
    left = a.merge(b).merge(c)
    right = a.merge(b.merge(c))
    assert readable(left) == readable(right), f"{name} merge depends on grouping"


@pytest.mark.parametrize("name,build", BUILDERS)
def test_merge_is_idempotent(name, build):
    a, b, _ = build()
    once = a.merge(b)
    twice = once.merge(b)
    assert readable(once) == readable(twice), f"{name} breaks on a redelivered update"


@pytest.mark.parametrize("name,build", BUILDERS)
def test_replicas_converge_in_every_delivery_order(name, build):
    replicas = build()
    assert converge(replicas), f"{name} does not converge under some delivery order"


@pytest.mark.parametrize("name,build", BUILDERS)
def test_convergence_survives_duplicates_and_batching(name, build):
    """The network is allowed to duplicate, reorder and batch. None may matter."""
    replicas = build()
    results = set()
    for order in itertools.permutations(range(len(replicas))):
        doubled = list(order) + list(reversed(order))     # every update twice
        results.add(readable(merge_all(replicas, doubled)))
    assert len(results) == 1, f"{name} diverges when updates arrive twice"


# ---------------------------------------------------------------------------
# counters
# ---------------------------------------------------------------------------


def test_gcounter_sums_across_replicas():
    a, b = GCounter(), GCounter()
    a.increment("a", 3)
    b.increment("b", 4)
    assert a.merge(b).value() == 7


def test_gcounter_does_not_double_count_a_redelivered_state():
    a, b = GCounter(), GCounter()
    a.increment("a", 3)
    b.increment("b", 4)
    merged = a.merge(b).merge(b).merge(b)
    assert merged.value() == 7, "max, not sum - that is why redelivery is safe"


def test_gcounter_refuses_to_decrement():
    counter = GCounter()
    with pytest.raises(ValueError):
        counter.increment("a", -1)


def test_pncounter_handles_concurrent_increment_and_decrement():
    a, b = PNCounter(), PNCounter()
    a.increment("a", 10)
    b.decrement("b", 4)
    assert a.merge(b).value() == 6
    assert b.merge(a).value() == 6


def test_pncounter_is_two_monotonic_halves():
    """Why not one counter with negative values?

    Because merge takes a maximum, and a maximum over a value that can fall
    would silently discard decrements. Both halves only ever grow.
    """
    a, b = PNCounter(), PNCounter()
    a.increment("shared", 5)
    a.decrement("shared", 5)
    b.increment("shared", 5)
    merged = a.merge(b)
    assert merged.ups.value() == 5
    assert merged.downs.value() == 5
    assert merged.value() == 0


# ---------------------------------------------------------------------------
# sets: where 2P-Set and OR-Set disagree
# ---------------------------------------------------------------------------


def test_two_phase_set_cannot_re_add_a_removed_item():
    """The flaw, pinned down."""
    cart = TwoPhaseSet()
    cart.add("milk")
    cart.remove("milk")
    cart.add("milk")                       # the customer changed their mind
    assert cart.value() == set(), "the tombstone is permanent - milk is gone forever"


def test_or_set_allows_re_adding():
    cart = ORSet()
    cart.add("milk", "tag1")
    cart.remove("milk")
    cart.add("milk", "tag2")               # a FRESH tag, so it survives
    assert cart.value() == {"milk"}


def test_or_set_concurrent_add_beats_concurrent_remove():
    """Two replicas, no communication: one removes, the other adds.

    The remover never saw the new tag, so it cannot have removed it. Add wins -
    and for a shopping cart that is the failure you want.
    """
    replica_a = ORSet()
    replica_a.add("milk", "tag-original")
    replica_b = replica_a.copy()

    replica_a.remove("milk")               # A removes the tag it has seen
    replica_b.add("milk", "tag-new")       # B concurrently re-adds

    assert replica_a.merge(replica_b).value() == {"milk"}
    assert replica_b.merge(replica_a).value() == {"milk"}


def test_two_phase_set_loses_the_same_edit_or_set_keeps():
    """Side by side on identical histories."""
    two_phase = TwoPhaseSet()
    two_phase.add("milk")
    before = two_phase.copy()
    two_phase.remove("milk")
    before.add("milk")
    assert two_phase.merge(before).value() == set()

    or_set = ORSet()
    or_set.add("milk", "t1")
    or_before = or_set.copy()
    or_set.remove("milk")
    or_before.add("milk", "t2")
    assert or_set.merge(or_before).value() == {"milk"}


def test_gset_is_union():
    a, b = GSet(), GSet()
    a.add(1)
    b.add(2)
    assert a.merge(b).value() == {1, 2}


# ---------------------------------------------------------------------------
# LWW register
# ---------------------------------------------------------------------------


def test_lww_later_timestamp_wins():
    register = LWWRegister()
    register.write("old", 1, "a")
    register.write("new", 2, "b")
    assert register.value() == "new"


def test_lww_ignores_an_older_write_arriving_late():
    register = LWWRegister()
    register.write("new", 5, "b")
    register.write("old", 1, "a")
    assert register.value() == "new", "arrival order must not matter"


def test_lww_tie_breaks_consistently_on_replica_id():
    """Two writes, identical timestamp. Both replicas must pick the same one."""
    a, b = LWWRegister(), LWWRegister()
    a.write("from-a", 10, "a")
    b.write("from-b", 10, "b")
    assert a.merge(b).value() == b.merge(a).value() == "from-b"


def test_lww_discards_the_losing_write_entirely():
    """Honest about the cost: there is no record the other write happened."""
    a, b = LWWRegister(), LWWRegister()
    a.write("alice-edit", 10, "a")
    b.write("bob-edit", 11, "b")
    merged = a.merge(b)
    assert merged.value() == "bob-edit"
    assert "alice-edit" not in str(merged.__dict__.values())


# ---------------------------------------------------------------------------
# the collaborative editor
# ---------------------------------------------------------------------------


def test_position_between_is_strictly_between():
    rng = random.Random(0)
    left: tuple[int, ...] = ()
    right: tuple[int, ...] = (1 << 16,)
    for _ in range(200):
        middle = position_between(left, right, rng)
        assert left < middle < right, f"{left} < {middle} < {right} failed"
        left = middle


def test_position_between_always_finds_room():
    """A dense order never runs out of space between two points.

    This is why concurrent inserts never need renumbering, and renumbering is
    exactly what would require coordination.
    """
    rng = random.Random(1)
    low: tuple[int, ...] = (5,)
    high: tuple[int, ...] = (6,)
    for _ in range(50):
        middle = position_between(low, high, rng)
        assert low < middle < high
        high = middle


def naive_run(label, left, right, text, seed):
    """The Logoot-style scheme: each character gets its own random position."""
    rng = random.Random(seed)
    out, cursor = [], left
    for character in text:
        position = position_between(cursor, right, rng)
        out.append((position, label, character))
        cursor = position
    return out


def contiguous_blocks(labels: str) -> int:
    return 1 + sum(1 for i in range(1, len(labels)) if labels[i] != labels[i - 1])


def test_naive_positions_interleave_concurrent_runs():
    """Why `TextCRDT` uses RGA and not the dense positions above.

    Independent random positions converge perfectly - every replica agrees -
    and shred both people's typing into each other. Convergence is necessary
    and nowhere near sufficient.
    """
    alice = naive_run("A", (1000,), (2000,), "AAAA", seed=0)
    bob = naive_run("B", (1000,), (2000,), "BBBB", seed=0)
    labels = "".join(label for _, label, _ in sorted(alice + bob))
    assert labels == "ABABABAB", "perfectly shuffled, and both replicas agree on it"

    # And it is the normal case, not a contrived seed.
    interleaved = sum(
        1
        for sa in range(40)
        for sb in range(40)
        if contiguous_blocks("".join(
            label for _, label, _ in sorted(
                naive_run("A", (1000,), (2000,), "AAAA", sa)
                + naive_run("B", (1000,), (2000,), "BBBB", sb)))) > 2)
    assert interleaved / 1600 > 0.8, (
        f"only {interleaved}/1600 seed pairs interleaved - if this ever drops, "
        f"the demonstration needs restating")


def test_rga_keeps_each_typed_run_together():
    """The same two runs under RGA: both survive intact."""
    alice = TextCRDT("alice", seed=1)
    alice.insert_text(0, "Hello")
    bob = alice.copy()
    bob.replica = "bob"

    alice.insert_text(5, "AAAA")
    bob.insert_text(5, "BBBB")

    merged = alice.merge(bob).text()
    assert merged == bob.merge(alice).text(), "still converges"
    assert "AAAA" in merged and "BBBB" in merged, "neither run is broken up"
    assert contiguous_blocks(merged[5:].replace("A", "A").replace("B", "B")) <= 2


def test_single_replica_typing():
    doc = TextCRDT("a", seed=1)
    doc.insert_text(0, "hello")
    assert doc.text() == "hello"
    doc.insert_text(5, " world")
    assert doc.text() == "hello world"
    doc.delete(0)
    assert doc.text() == "ello world"


def test_insert_index_is_validated():
    doc = TextCRDT("a", seed=1)
    with pytest.raises(IndexError):
        doc.insert(1, "x")
    with pytest.raises(IndexError):
        doc.delete(0)


def test_concurrent_edits_converge_to_the_same_text():
    """Two people typing at once, with no coordination.

    Both replicas end up with the identical document - and crucially, neither
    edit is lost, which is what last-write-wins on the whole document would do.
    """
    alice = TextCRDT("alice", seed=1)
    alice.insert_text(0, "Hello")
    bob = alice.copy()
    bob.replica = "bob"

    alice.insert_text(5, " from Alice")
    bob.insert_text(5, " from Bob")

    alice_view = alice.merge(bob)
    bob_view = bob.merge(alice)

    assert alice_view.text() == bob_view.text(), "replicas must converge"
    assert "Alice" in alice_view.text() and "Bob" in alice_view.text(), (
        "neither edit may be lost")
    assert alice_view.text().startswith("Hello")


def test_concurrent_edit_at_the_same_index_converges():
    alice = TextCRDT("alice", seed=2)
    alice.insert_text(0, "AC")
    bob = alice.copy()
    bob.replica = "bob"

    alice.insert(1, "B")                 # A B C
    bob.insert(1, "X")                   # A X C

    assert alice.merge(bob).text() == bob.merge(alice).text()
    assert set(alice.merge(bob).text()) == set("ABCX")


def test_delete_on_one_replica_while_the_other_types():
    alice = TextCRDT("alice", seed=3)
    alice.insert_text(0, "abcd")
    bob = alice.copy()
    bob.replica = "bob"

    alice.delete(1)                      # removes 'b'
    bob.insert(4, "e")                   # appends 'e'

    merged_a = alice.merge(bob)
    merged_b = bob.merge(alice)
    assert merged_a.text() == merged_b.text() == "acde"


def test_text_merge_is_idempotent():
    alice = TextCRDT("alice", seed=4)
    alice.insert_text(0, "hi")
    bob = alice.copy()
    bob.replica = "bob"
    bob.insert_text(2, " there")
    once = alice.merge(bob)
    assert once.merge(bob).text() == once.text()


# ---------------------------------------------------------------------------
# state-based versus operation-based
# ---------------------------------------------------------------------------


def test_operation_based_breaks_on_a_duplicate_without_deduplication():
    """The trade: smaller messages, stricter delivery requirement."""
    log = OperationLog()
    log.apply("op1", 5, deduplicate=False)
    log.apply("op1", 5, deduplicate=False)          # the network retried
    assert log.total == 10, "an op-based CRDT double-counts a redelivered op"


def test_operation_based_is_safe_once_delivery_deduplicates():
    log = OperationLog()
    assert log.apply("op1", 5)
    assert not log.apply("op1", 5), "second delivery is ignored"
    assert log.total == 5


def test_state_based_needs_no_such_guarantee():
    """Contrast: the G-Counter absorbs redelivery by construction."""
    a, b = GCounter(), GCounter()
    a.increment("a", 5)
    b.increment("b", 5)
    merged = a.merge(b)
    for _ in range(10):
        merged = merged.merge(a).merge(b)
    assert merged.value() == 10
