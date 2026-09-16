"""Beginner playground for Module 23 - Isolation Levels and Consensus (Raft).

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# -------------------------- 1. Two transactions, one counter, one lost update
row = {"stock": 100}

read_by_a = row["stock"]
read_by_b = row["stock"]        # B reads before A has written

row["stock"] = read_by_a - 1    # A writes 99
row["stock"] = read_by_b - 1    # B writes 99, using its own stale read

print("two sales, starting from 100 ->", row["stock"])
assert row["stock"] == 99, "two items sold, stock fell by one"
print("One sale vanished. No error, no log line, no way to notice later.")


# -------------------------------- 2. What each isolation level actually stops
row = {"stock": 100}


def sell_atomically(quantity):
    # One statement: UPDATE stock SET stock = stock - ? WHERE stock >= ?
    if row["stock"] >= quantity:
        row["stock"] -= quantity
        return True
    return False


assert sell_atomically(1) and sell_atomically(1)
print("two sales, atomically ->", row["stock"])
assert row["stock"] == 98, "both decrements survived"


# -------------------------------------- 3. Raft: five friends choosing dinner
friends = ["ana", "bo", "cy", "di", "ed"]
MAJORITY = len(friends) // 2 + 1


def election(votes_by_candidate):
    assert sum(len(v) for v in votes_by_candidate.values()) <= len(friends), (
        "nobody may vote twice in one term")
    winners = [c for c, v in votes_by_candidate.items() if len(v) >= MAJORITY]
    return winners[0] if winners else None


print("majority of", len(friends), "friends is", MAJORITY)
print("pizza {ana,bo} vs sushi {cy,di,ed} ->",
      election({"pizza": {"ana", "bo"}, "sushi": {"cy", "di", "ed"}}))
print("pizza {ana,bo} vs sushi {cy,di}    ->",
      election({"pizza": {"ana", "bo"}, "sushi": {"cy", "di"}}))
assert election({"pizza": {"ana", "bo"}, "sushi": {"cy", "di", "ed"}}) == "sushi"
assert election({"pizza": {"ana", "bo"}, "sushi": {"cy", "di"}}) is None
print("A tied term elects nobody. Everyone waits and tries again. That is fine.")


# --------------------------- 4. Why the network cannot split the group in two
def partition_can_proceed(members):
    return len(members) >= MAJORITY


room_of_three = {"ana", "bo", "cy"}
room_of_two = {"di", "ed"}

print("room of three can elect a leader:", partition_can_proceed(room_of_three))
print("room of two can elect a leader:  ", partition_can_proceed(room_of_two))
assert partition_can_proceed(room_of_three)
assert not partition_can_proceed(room_of_two), "the minority must stop, not guess"
assert not (partition_can_proceed(room_of_three) and partition_can_proceed(room_of_two))
print("At most one side can ever proceed. Split brain is arithmetically impossible.")


# ----------------------------------------------------- 5. Committing an entry
log_stored_by = {"ana"}          # the leader has written it
print("stored by", sorted(log_stored_by), "- committed:", len(log_stored_by) >= MAJORITY)

log_stored_by |= {"bo", "cy"}
print("stored by", sorted(log_stored_by), "- committed:", len(log_stored_by) >= MAJORITY)
assert len(log_stored_by) >= MAJORITY

future_leader_voters = {"cy", "di", "ed"}
assert log_stored_by & future_leader_voters, (
    "any future majority overlaps this one, so the entry cannot be lost")
print("Overlap between majorities is why a committed entry survives every failover.")


print()
print("All checks passed.")
