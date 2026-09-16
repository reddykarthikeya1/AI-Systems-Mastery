# Module 17 Problem Bank - Network Flow

Six problems. Each has a stub here, a reference solution in `solutions/`, and a
test in `tests/`.

| # | Problem | Pattern | Difficulty |
| :-- | :--- | :--- | :--- |
| 01 | Maximum Flow | Edmonds-Karp | Medium |
| 02 | Which Edges Are the Bottleneck? | Max-flow min-cut | Hard |
| 03 | Maximum Bipartite Matching | Unit-capacity flow | Medium |
| 04 | Edge-Disjoint Paths | Unit-capacity flow | Medium |
| 05 | Vertex-Disjoint Paths | Node splitting | Hard |
| 06 | Workers Who Can Take Several Shifts | Non-unit capacities | Medium |

Only problem 01 is really about the algorithm. The other five are about
*recognising* a flow problem and building the right graph - which is the skill
that actually gets tested, because nobody asks you to implement Edmonds-Karp
from memory but plenty of people ask you to assign drivers to routes.

Problems 03 to 06 all reduce to the same function with different capacities.
Notice what each capacity forbids:

| Capacity | The rule it encodes |
| :--- | :--- |
| source -> worker = 1 | one job per worker |
| job -> sink = 1 | one worker per job |
| every edge = 1 | no edge reused (edge-disjoint) |
| v_in -> v_out = 1 | no node reused (vertex-disjoint) |
| source -> worker = k | up to k shifts per worker |

## Working on them

```bash
cd problems
python -m pytest tests -q              # grades YOUR stubs - must fail at first
python -m pytest tests -q -k p05       # just one problem
```

From the course root the same tests grade the reference solutions instead.
