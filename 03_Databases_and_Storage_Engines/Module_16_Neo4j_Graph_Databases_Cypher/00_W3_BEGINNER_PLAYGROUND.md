# Beginner Playground - Neo4j and Graph Databases

> *"A relational join asks 'which rows match?' every single hop. A graph already holds the answer as a pointer, so it just walks."*

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

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
from collections import deque
```

---

## 1. Relationships as first-class things

In SQL a relationship is a row in a join table, and following it means searching
an index. In a graph database the relationship is a pointer stored on the node
itself, so following it is just dereferencing - no search at all.

The phrase for this is **index-free adjacency**, and it is why graph query cost
scales with the size of the *answer* rather than the size of the database.

```python
friends = {
    "ana": ["bo", "cy"],
    "bo": ["ana", "di"],
    "cy": ["ana", "di", "ed"],
    "di": ["bo", "cy", "fay"],
    "ed": ["cy"],
    "fay": ["di"],
}

print("ana's direct friends:", friends["ana"])
assert friends["ana"] == ["bo", "cy"]
```

---

## 2. Walking, not joining

Friends-of-friends is one step further along the same pointers. The traversal
touches only the people it actually reaches - nothing else in the database is
examined at all.

```python
def n_hops(start, hops):
    seen = {start}
    frontier = {start}
    visited_nodes = 0
    for _ in range(hops):
        nxt = set()
        for person in frontier:
            visited_nodes += 1
            nxt.update(friends[person])
        frontier = nxt - seen
        seen |= nxt
    return seen - {start}, visited_nodes


reach_2, touched = n_hops("ana", 2)
print("within 2 hops of ana:", sorted(reach_2), f"(visited {touched} nodes)")
assert sorted(reach_2) == ["bo", "cy", "di", "ed"]
assert touched <= len(friends), "never more work than there are people"
```

---

## 3. Shortest path in one traversal

"How is ana connected to fay?" is a breadth-first search - and it is the query
that sells graph databases. The relational version is a recursive CTE that
re-joins the whole edge table at every level.

```python
def shortest_path(start, goal):
    queue = deque([[start]])
    seen = {start}
    while queue:
        path = queue.popleft()
        if path[-1] == goal:
            return path
        for neighbour in friends[path[-1]]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(path + [neighbour])
    return None


route = shortest_path("ana", "fay")
print("ana -> fay:", " -> ".join(route))
assert route is not None and route[0] == "ana" and route[-1] == "fay"
assert len(route) == 4, "ana, one friend, di, fay"
```

---

## 4. Where the relational version falls over

Each extra hop is another join, and a join considers rows proportional to the
*whole* relationship table, not just the ones you reach. At depth 1 nobody
notices. At depth 4 the difference is the difference between a dashboard and an
outage.

```python
people = 1_000_000
friends_each = 100
edges = people * friends_each

graph_work = [friends_each ** d for d in (1, 2, 3)]
join_work = [edges * d for d in (1, 2, 3)]

for depth in (1, 2, 3):
    print(f"  depth {depth}: graph walks ~{graph_work[depth - 1]:>9,} "
          f"| join considers ~{join_work[depth - 1]:>12,}")

assert graph_work[2] < join_work[2] / 100, "at depth 3 it is not a close contest"
print("The graph's cost follows the answer. The join's cost follows the database.")
```

---

## 5. Predict before you run

Finding friends-of-friends-of-friends in SQL needs three joins. If each
person has 100 friends, how many rows does the third join consider? Does the
graph traversal consider the same number?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Fraud rings, recommendation engines and access-control hierarchies are all
'how is A connected to B' questions. They are the queries where relational
databases go from fine to unusable as the depth increases by one.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
