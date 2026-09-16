"""CRDTs: convergence without consensus.

This is an **in-process model**. The replicas are objects in one Python process
and "sending an update" is a method call, so there is no network and nothing is
ever actually concurrent. What is real is the algebra, and the algebra is the
entire subject.

Where this sits next to the rest of the module
----------------------------------------------
Vector clocks (see `raft_cluster_engine.py`) *detect* that two edits were
concurrent. Raft *avoids* concurrent edits by forcing everything through one
leader. CRDTs take the third option: design the data type so that concurrent
edits cannot conflict in the first place, and no coordination is needed at all.

| Approach | Needs a leader? | Available during a partition? | Cost |
| :--- | :--- | :--- | :--- |
| Raft | yes | no - the minority stops | strong consistency |
| Last-write-wins | no | yes | silently discards an edit |
| CRDT | no | yes | the merge rule is fixed at design time |

The price is real: you do not get to choose the resolution per conflict, you
choose it once when you pick the type. A counter that merges by taking the
maximum cannot also support decrement, which is why `PNCounter` is two counters
rather than one with negative numbers.

The three laws
--------------
A state-based CRDT (a **CvRDT**) needs `merge` to be:

1. **commutative** - `merge(a, b) == merge(b, a)`, so delivery order is free
2. **associative** - grouping does not matter, so batching is free
3. **idempotent** - `merge(a, a) == a`, so redelivery is free

Get all three and replicas converge no matter how the network behaves: any
order, any duplication, any batching. That is the whole theorem, and every type
below is checked against all three by the test suite rather than asserted.

An operation-based CRDT (a **CmRDT**) ships operations instead of state. It
needs less bandwidth and more from the network: exactly-once, causally ordered
delivery. `OperationLog` at the bottom models that difference.
"""

from __future__ import annotations

import itertools
import random
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# counters
# ---------------------------------------------------------------------------


@dataclass
class GCounter:
    """Grow-only counter. Merge takes the per-replica maximum.

    Each replica only ever increments *its own* slot, so two replicas can never
    disagree about the same slot. The maximum is then safe: it cannot lose an
    increment, and applying it twice changes nothing.
    """

    counts: dict[str, int] = field(default_factory=dict)

    def increment(self, replica: str, amount: int = 1) -> None:
        if amount < 0:
            raise ValueError("a G-Counter cannot go down; use a PN-Counter")
        self.counts[replica] = self.counts.get(replica, 0) + amount

    def value(self) -> int:
        return sum(self.counts.values())

    def merge(self, other: GCounter) -> GCounter:
        merged = dict(self.counts)
        for replica, count in other.counts.items():
            merged[replica] = max(merged.get(replica, 0), count)
        return GCounter(merged)

    def copy(self) -> GCounter:
        return GCounter(dict(self.counts))


@dataclass
class PNCounter:
    """Increment and decrement, as two grow-only counters.

    The obvious design - one counter with negative increments - breaks the
    merge rule, because taking a maximum over values that can fall would lose
    decrements. Splitting into "up" and "down" restores monotonicity: both
    halves only grow, and the value is their difference.
    """

    ups: GCounter = field(default_factory=GCounter)
    downs: GCounter = field(default_factory=GCounter)

    def increment(self, replica: str, amount: int = 1) -> None:
        self.ups.increment(replica, amount)

    def decrement(self, replica: str, amount: int = 1) -> None:
        self.downs.increment(replica, amount)

    def value(self) -> int:
        return self.ups.value() - self.downs.value()

    def merge(self, other: PNCounter) -> PNCounter:
        return PNCounter(self.ups.merge(other.ups), self.downs.merge(other.downs))

    def copy(self) -> PNCounter:
        return PNCounter(self.ups.copy(), self.downs.copy())


# ---------------------------------------------------------------------------
# sets
# ---------------------------------------------------------------------------


@dataclass
class GSet:
    """Grow-only set. Merge is union. Nothing can ever be removed."""

    items: set = field(default_factory=set)

    def add(self, item) -> None:
        self.items.add(item)

    def value(self) -> set:
        return set(self.items)

    def merge(self, other: GSet) -> GSet:
        return GSet(self.items | other.items)

    def copy(self) -> GSet:
        return GSet(set(self.items))


@dataclass
class TwoPhaseSet:
    """Add, then remove - but never add again. Included because it is wrong.

    Removal is recorded in a tombstone set, and a tombstone is permanent. So an
    item that is removed once can never come back, even if a later add was
    clearly intended.

    That is a legitimate design for some data (a revoked key) and a bug for most
    (a shopping cart, a set of tags). `ORSet` fixes it, and the test suite pins
    down the exact case where the two disagree.
    """

    added: set = field(default_factory=set)
    removed: set = field(default_factory=set)

    def add(self, item) -> None:
        self.added.add(item)

    def remove(self, item) -> None:
        if item in self.added:
            self.removed.add(item)

    def value(self) -> set:
        return self.added - self.removed

    def merge(self, other: TwoPhaseSet) -> TwoPhaseSet:
        return TwoPhaseSet(self.added | other.added, self.removed | other.removed)

    def copy(self) -> TwoPhaseSet:
        return TwoPhaseSet(set(self.added), set(self.removed))


@dataclass
class ORSet:
    """Observed-Remove Set: add wins, and re-adding works.

    Every add attaches a unique tag. A remove deletes only the tags it has
    actually *observed*, so a concurrent add - whose tag the remover never saw -
    survives. Re-adding after a remove mints a fresh tag and therefore works.

    This is the set type behind Riak's and Redis's replicated sets, and the
    "add wins" bias is a deliberate choice: in a shopping cart, wrongly keeping
    an item is a better failure than wrongly dropping one.
    """

    tags: dict = field(default_factory=dict)          # item -> set of tags

    def add(self, item, tag: str | None = None) -> str:
        tag = tag if tag is not None else f"{item}:{len(self.tags.get(item, ()))}"
        self.tags.setdefault(item, set()).add(tag)
        return tag

    def remove(self, item) -> None:
        # Only the tags this replica has seen. A concurrent add is untouched.
        self.tags.pop(item, None)

    def value(self) -> set:
        return {item for item, tags in self.tags.items() if tags}

    def merge(self, other: ORSet) -> ORSet:
        merged: dict = {item: set(tags) for item, tags in self.tags.items()}
        for item, tags in other.tags.items():
            merged.setdefault(item, set()).update(tags)
        return ORSet({item: tags for item, tags in merged.items() if tags})

    def copy(self) -> ORSet:
        return ORSet({item: set(tags) for item, tags in self.tags.items()})


# ---------------------------------------------------------------------------
# registers
# ---------------------------------------------------------------------------


@dataclass
class LWWRegister:
    """Last-write-wins on a single value.

    The tie-break is what makes this a CRDT rather than a coin flip. Two writes
    with the same timestamp must resolve the same way on every replica, so ties
    are broken by replica id - arbitrary, but *consistently* arbitrary, which is
    the only property that matters.

    It still loses data by design: the losing write is gone, with no record that
    it happened. Use it when the value is a setting; do not use it for a
    shopping cart.
    """

    value_: object = None
    timestamp: int = -1
    replica: str = ""

    def write(self, value, timestamp: int, replica: str) -> None:
        if (timestamp, replica) > (self.timestamp, self.replica):
            self.value_ = value
            self.timestamp = timestamp
            self.replica = replica

    def value(self):
        return self.value_

    def merge(self, other: LWWRegister) -> LWWRegister:
        if (other.timestamp, other.replica) > (self.timestamp, self.replica):
            return LWWRegister(other.value_, other.timestamp, other.replica)
        return LWWRegister(self.value_, self.timestamp, self.replica)

    def copy(self) -> LWWRegister:
        return LWWRegister(self.value_, self.timestamp, self.replica)


# ---------------------------------------------------------------------------
# a collaborative text document
# ---------------------------------------------------------------------------

BASE = 1 << 16
START: tuple[int, ...] = ()
END: tuple[int, ...] = (BASE,)


def position_between(left: tuple[int, ...], right: tuple[int, ...],
                     rng: random.Random) -> tuple[int, ...]:
    """A position strictly between two others, in a densely ordered space.

    Ordinary list indices cannot work for concurrent editing: if you insert at
    index 3 and I insert at index 3, one of us has to be renumbered, and
    renumbering requires coordination.

    Identifiers from a *dense* order do not have that problem - there is always
    room between any two, so an insert never disturbs anything else. This is
    the idea behind Logoot and LSEQ.
    """
    out: list[int] = []
    depth = 0
    while True:
        low = left[depth] if depth < len(left) else 0
        high = right[depth] if depth < len(right) else BASE
        if high - low > 1:
            out.append(rng.randrange(low + 1, high))
            return tuple(out)
        out.append(low)
        depth += 1


@dataclass(frozen=True)
class Character:
    """One character, identified by who typed it and the character it follows.

    `after` is the identity of the character this one was inserted *behind* -
    not a numeric position. That indirection is what keeps a typed run together
    when two people type at the same spot; see `TextCRDT` for why a position
    is not enough.
    """

    element_id: tuple[int, str]                  # (counter, replica)
    after: tuple[int, str] | None                # None means "start of document"
    value: str


@dataclass
class TextCRDT:
    """A replicated text document, ordered the way RGA orders one.

    **Why not the dense positions above?** They converge, and they produce
    nonsense. Give every character an independent random position and two
    people typing simultaneously at the same spot get their runs shuffled
    together character by character:

        Alice types " from Alice", Bob types " from Bob"
        both replicas agree on:  "Hello  frfomro m ABolbice"

    Every replica shows the identical string, so the CRDT laws hold perfectly -
    and the document is ruined. This is the **interleaving anomaly**, and it is
    the reason Logoot-style position schemes lost to RGA in practice.
    `test_naive_positions_interleave_concurrent_runs` demonstrates it.

    **What RGA does instead.** A character records the *identity* of the
    character it follows. Typing a run therefore builds a chain - each
    character is the child of the one before it - so the run is a subtree and
    can only be inserted somewhere as a whole. Two concurrent runs are siblings
    of the same predecessor, and siblings are ordered by id, newest first. Both
    replicas apply the same rule to the same set, so both render the same text,
    and neither run is broken up.

    Deletion is a tombstone: the character stays so that anything inserted
    after it still has a place to attach. A real implementation collects
    tombstones once every replica has acknowledged the delete.
    """

    replica: str
    seed: int = 0
    characters: set = field(default_factory=set)
    tombstones: set = field(default_factory=set)
    counter: int = 0

    def _ordered(self) -> list[Character]:
        """Depth-first over the "inserted after" tree.

        Siblings sort by id descending, so a later insert at the same point
        appears first. Any total, deterministic rule would converge; this one
        is RGA's.
        """
        children: dict[tuple[int, str] | None, list[Character]] = {}
        for character in self.characters:
            children.setdefault(character.after, []).append(character)
        for group in children.values():
            group.sort(key=lambda c: c.element_id, reverse=True)

        out: list[Character] = []
        stack = list(reversed(children.get(None, [])))
        while stack:
            character = stack.pop()
            out.append(character)
            kids = children.get(character.element_id)
            if kids:
                stack.extend(reversed(kids))     # the run stays together
        return out

    def _visible(self) -> list[Character]:
        return [c for c in self._ordered() if c.element_id not in self.tombstones]

    def text(self) -> str:
        return "".join(c.value for c in self._visible())

    def insert(self, index: int, value: str) -> Character:
        visible = self._visible()
        if not 0 <= index <= len(visible):
            raise IndexError(f"index {index} outside 0..{len(visible)}")
        after = visible[index - 1].element_id if index > 0 else None
        self.counter += 1
        character = Character((self.counter, self.replica), after, value)
        self.characters.add(character)
        return character

    def insert_text(self, index: int, text: str) -> None:
        for offset, value in enumerate(text):
            self.insert(index + offset, value)

    def delete(self, index: int) -> Character:
        visible = self._visible()
        if not 0 <= index < len(visible):
            raise IndexError(f"index {index} outside 0..{len(visible) - 1}")
        character = visible[index]
        self.tombstones.add(character.element_id)
        return character

    def merge(self, other: TextCRDT) -> TextCRDT:
        merged = TextCRDT(self.replica, self.seed)
        merged.characters = self.characters | other.characters
        merged.tombstones = self.tombstones | other.tombstones
        # Never reissue an id that already exists anywhere in the merged state.
        merged.counter = max(
            [self.counter, other.counter]
            + [c.element_id[0] for c in merged.characters])
        return merged

    def copy(self) -> TextCRDT:
        clone = TextCRDT(self.replica, self.seed)
        clone.characters = set(self.characters)
        clone.tombstones = set(self.tombstones)
        clone.counter = self.counter
        return clone


# ---------------------------------------------------------------------------
# state-based versus operation-based
# ---------------------------------------------------------------------------


@dataclass
class OperationLog:
    """An operation-based CRDT (CmRDT), for contrast with everything above.

    State-based replication ships the whole value and merges it. That is robust
    to anything the network does - duplicates and reordering are absorbed by the
    three laws - but it ships the whole value.

    Operation-based replication ships just the operation, which is far smaller,
    and in exchange demands that the network deliver each operation **exactly
    once**. Deliver an "increment by 1" twice and the counter is simply wrong,
    with no way to notice.

    This class shows the difference by tracking applied operation ids, which is
    the deduplication that an op-based CRDT's delivery layer has to provide.
    """

    total: int = 0
    applied: set = field(default_factory=set)

    def apply(self, operation_id: str, delta: int, deduplicate: bool = True) -> bool:
        """Returns True if the operation changed the state."""
        if deduplicate and operation_id in self.applied:
            return False
        self.applied.add(operation_id)
        self.total += delta
        return True


def converge(replicas: list) -> bool:
    """True if every replica, merged with every other, reports the same value.

    The property that matters, checked directly rather than assumed.
    """
    values = set()
    for order in itertools.permutations(range(len(replicas))):
        state = replicas[order[0]].copy()
        for index in order[1:]:
            state = state.merge(replicas[index])
        value = state.value() if hasattr(state, "value") else state.text()
        values.add(frozenset(value) if isinstance(value, set) else value)
    return len(values) == 1
