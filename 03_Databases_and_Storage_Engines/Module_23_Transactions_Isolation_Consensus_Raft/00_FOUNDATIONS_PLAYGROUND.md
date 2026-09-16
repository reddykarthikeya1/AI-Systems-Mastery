# Beginner Playground - Isolation Levels and Consensus (Raft)

> *"Isolation is how much you are allowed to peek into other people's shopping trolleys. Raft is five friends choosing a restaurant: whatever three of them agree on is where everyone goes."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no
server, no `pip install`, no account to sign up for. You can read it in ten
minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints
`All checks passed`, every claim below just proved itself on your machine.

---

## 1. Two transactions, one counter, one lost update

Both transactions read 100. Both add 1. Both write 101. One of the two increments
simply disappeared, and nothing anywhere recorded that it happened.

This is a **lost update**, and it is what weak isolation permits.

```python
row = {"stock": 100}

read_by_a = row["stock"]
read_by_b = row["stock"]        # B reads before A has written

row["stock"] = read_by_a - 1    # A writes 99
row["stock"] = read_by_b - 1    # B writes 99, using its own stale read

print("two sales, starting from 100 ->", row["stock"])
assert row["stock"] == 99, "two items sold, stock fell by one"
print("One sale vanished. No error, no log line, no way to notice later.")
```

---

## 2. What each isolation level actually stops

| Level | Stops | Still allows |
| :--- | :--- | :--- |
| Read uncommitted | nothing | reading data that gets rolled back |
| Read committed | dirty reads | the same query returning different rows twice |
| Repeatable read | non-repeatable reads | phantom rows appearing in a range |
| Serializable | everything | nothing - but it costs, and it can abort you |

Higher is not automatically better. `SERIALIZABLE` means the database may kill
your transaction and expect you to retry, so choosing it is also a commitment to
writing retry logic.

The fix for the bug above does not need the strongest level - just an atomic
update that reads and writes in one step.

```python
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
```

---

## 3. Raft: five friends choosing dinner

Five friends must agree on one restaurant. The rules are deliberately simple:

1. Anyone may **stand as candidate** for a given round (a **term**).
2. Everyone gets **one vote per round**, and gives it to the first candidate who
   asks.
3. A candidate needs **more than half** - three of five - to become the leader.
4. Only the leader proposes, and everyone follows the leader's list.

Rule 3 is the load-bearing one. Two candidates cannot both collect three votes
out of five, because that would need six votes and only five exist.

```python
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
```

---

## 4. Why the network cannot split the group in two

Now the group splits: three friends in one room, two in another, unable to hear
each other. The room of three has a majority and carries on. The room of two does
not, and must refuse to decide anything.

That refusal is the feature. A minority that kept serving writes would be a second
leader, and the two halves would diverge irreconcilably. Raft would rather be
unavailable than wrong.

```python
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
```

---

## 5. Committing an entry

The leader appends to its log and sends it out. An entry is **committed** once a
majority have stored it - at which point it is safe forever, because any future
leader must also win a majority, and two majorities always share a member who has
the entry.

Note what commitment is *not*: it is not "everyone has it". Waiting for everyone
means one slow friend stops dinner.

```python
log_stored_by = {"ana"}          # the leader has written it
print("stored by", sorted(log_stored_by), "- committed:", len(log_stored_by) >= MAJORITY)

log_stored_by |= {"bo", "cy"}
print("stored by", sorted(log_stored_by), "- committed:", len(log_stored_by) >= MAJORITY)
assert len(log_stored_by) >= MAJORITY

future_leader_voters = {"cy", "di", "ed"}
assert log_stored_by & future_leader_voters, (
    "any future majority overlaps this one, so the entry cannot be lost")
print("Overlap between majorities is why a committed entry survives every failover.")
```

---

## 6. Predict before you run

Five friends, and the group splits: three in one room, two in another. Can
both rooms pick a restaurant? Can either? What if the split is 4 and 1?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

etcd, Consul and CockroachDB all run Raft, which means every Kubernetes
cluster you touch depends on it. And the lost-update bug in section 2 is the
reason 'read, modify, write' is a code review red flag.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
