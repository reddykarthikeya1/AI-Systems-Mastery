# Beginner Playground - Consensus, Raft and Vector Clocks

> *"Raft is a committee with one chair and a rule that nothing passes without a majority. A vector clock is everyone keeping a tally of what they have heard from whom."*

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

## 1. The majority rule, and what it buys

A Raft leader needs votes from more than half the cluster. Two candidates cannot
both achieve that, because it would take more votes than there are members.

The same arithmetic protects committed data: any future majority shares at least
one member with the majority that accepted an entry, so a committed entry cannot
be forgotten by a new leader.

```python
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
```

---

## 2. Terms: a logical clock that needs no clock

Raft numbers time in **terms** - an integer that increases each election. Every
message carries its sender's term.

A server seeing a higher term immediately steps down and accepts the newer
authority. A server seeing a lower term ignores the message as stale. An old
leader that was network-partitioned and comes back cannot do damage, because
everything it says is stamped with a term nobody accepts any more.

```python
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
```

---

## 3. Wall clocks lie, and last-write-wins believes them

Two servers write to the same key. The one whose clock is 30 seconds fast wins the
comparison regardless of what actually happened first, and the other edit is
discarded silently.

The problem is not clock accuracy. It is that a timestamp cannot express "these
two edits did not know about each other".

```python
edit_from_correct_node = ("address: 12 Oak Street", 1_000)
edit_from_fast_node = ("address: 4 Elm Road", 1_030)      # clock 30s ahead

winner = max([edit_from_correct_node, edit_from_fast_node], key=lambda e: e[1])
print("last-write-wins keeps:", winner[0])
assert winner[0] == "address: 4 Elm Road"
print("The genuinely later edit was thrown away. Nothing logged it.")
```

---

## 4. Vector clocks record who knew what

Each node keeps a counter per node. Writing increments your own counter; receiving
takes the maximum of each position.

Now compare two versions position by position:

- every position less than or equal, and at least one strictly less -> it *happened
  before*; the newer one supersedes it safely.
- neither dominates -> the two edits are **concurrent**. Nobody saw the other, and
  the system must say so rather than pick one.

```python
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
```

---

## 5. What you do with a detected conflict

Detecting it is the hard part. Resolving it is a *product* decision, and the right
answer depends on the data:

| Data | Sensible resolution |
| :--- | :--- |
| Shopping cart | union the items - Amazon's Dynamo did exactly this |
| Counter | add the increments |
| Document text | keep both versions and ask the user |
| Config value | last-write-wins is genuinely fine |

The mistake is not choosing last-write-wins. It is choosing it without knowing you
had a conflict at all.

```python
cart_x = {"apple", "bread"}
cart_y = {"apple", "cheese"}

lww_result = cart_y
merged = cart_x | cart_y
print("last-write-wins gives:", sorted(lww_result))
print("merging concurrent edits gives:", sorted(merged))
assert "bread" not in lww_result, "the customer's item silently vanished"
assert merged == {"apple", "bread", "cheese"}, "nothing lost"
print("Same detection, different resolution. Pick it deliberately.")
```

---

## 6. Predict before you run

Two servers edit the same record. Their clocks differ by 30 seconds. Using
last-write-wins, which edit survives - the later one, or the one from the
server whose clock is ahead?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

etcd and Consul run Raft, so every Kubernetes cluster depends on it. Vector
clocks are how Dynamo-style stores tell 'this edit came after that one' from
'these two edits happened independently' - a distinction wall-clock timestamps
simply cannot make.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
