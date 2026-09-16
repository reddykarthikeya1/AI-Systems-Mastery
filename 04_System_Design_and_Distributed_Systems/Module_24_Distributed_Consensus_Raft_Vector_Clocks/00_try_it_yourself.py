"""Beginner playground for Module 24 - Consensus, Raft and Vector Clocks.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ------------------------------------- 1. The majority rule, and what it buys
CLUSTER = ["n1", "n2", "n3", "n4", "n5"]
MAJORITY = len(CLUSTER) // 2 + 1


def has_majority(members):
    return len(members) >= MAJORITY


partition_a = {"n1", "n2", "n3"}
partition_b = {"n4", "n5"}
print(f"cluster of {len(CLUSTER)}, majority is {MAJORITY}")
print("  partition of 3 can elect:", has_majority(partition_a))
print("  partition of 2 can elect:", has_majority(partition_b))
assert has_majority(partition_a) and not has_majority(partition_b)
assert not (has_majority(partition_a) and has_majority(partition_b))
print("At most one side ever proceeds. Split brain is arithmetically impossible.")


# ------------------------------ 2. Terms: a logical clock that needs no clock
class Node:
    def __init__(self, name):
        self.name = name
        self.term = 1
        self.role = "follower"

    def receive(self, message_term, sender):
        if message_term > self.term:
            self.term, self.role = message_term, "follower"
            return f"stepped down, now following {sender} in term {message_term}"
        if message_term < self.term:
            return f"ignored {sender}: term {message_term} is stale"
        return f"accepted from {sender}"


node = Node("n3")
node.term = 5
print(" ", node.receive(7, "n1"))
print(" ", node.receive(3, "old-leader"))
assert node.term == 7
assert "ignored" in node.receive(3, "old-leader")
print("The deposed leader cannot corrupt anything. Its term is in the past.")


# ---------------------- 3. Wall clocks lie, and last-write-wins believes them
edit_from_correct_node = ("address: 12 Oak Street", 1_000)
edit_from_fast_node = ("address: 4 Elm Road", 1_030)      # clock 30s ahead

winner = max([edit_from_correct_node, edit_from_fast_node], key=lambda e: e[1])
print("last-write-wins keeps:", winner[0])
assert winner[0] == "address: 4 Elm Road"
print("The genuinely later edit was thrown away. Nothing logged it.")


# -------------------------------------- 4. Vector clocks record who knew what
def happened_before(a, b):
    return all(a.get(k, 0) <= b.get(k, 0) for k in set(a) | set(b)) and a != b


def concurrent(a, b):
    return not happened_before(a, b) and not happened_before(b, a) and a != b


base = {"n1": 1}
sequential = {"n1": 2}
branch_x = {"n1": 1, "n2": 1}
branch_y = {"n1": 1, "n3": 1}

print("base -> sequential   :", "causal" if happened_before(base, sequential) else "?")
print("branch_x vs branch_y :", "CONCURRENT" if concurrent(branch_x, branch_y) else "?")
assert happened_before(base, sequential), "one clearly follows the other"
assert concurrent(branch_x, branch_y), "neither node saw the other's write"
print("A timestamp would have silently picked one. This reports a genuine conflict.")


# ------------------------------------ 5. What you do with a detected conflict
cart_x = {"apple", "bread"}
cart_y = {"apple", "cheese"}

lww_result = cart_y
merged = cart_x | cart_y
print("last-write-wins gives:", sorted(lww_result))
print("merging concurrent edits gives:", sorted(merged))
assert "bread" not in lww_result, "the customer's item silently vanished"
assert merged == {"apple", "bread", "cheese"}, "nothing lost"
print("Same detection, different resolution. Pick it deliberately.")


print()
print("All checks passed.")
