"""Problem-bank suite for Module_08_Graph_Algorithms_Traversals_and_DAGs.

Run from the course root and these grade the reference solutions.
Run from ``problems/`` and they grade YOUR stubs — which must fail until you
implement them. If they pass on an untouched stub, the grading loop is broken;
see ``tools/check_integrity.py``.
"""

from __future__ import annotations

from p01_num_islands import num_islands
from p02_count_components import count_components
from p03_topological_order import topological_order
from p04_has_cycle_directed import has_cycle_directed
from p05_can_finish_courses import can_finish_courses
from p06_rotting_oranges import rotting_oranges
from p07_shortest_path_grid import shortest_path_grid
from p08_word_ladder import word_ladder


def test_p01_num_islands():
    """Number Of Islands — DFS flood fill (Medium)."""
    assert num_islands([["1", "1", "0"], ["1", "0", "0"], ["0", "0", "1"]]) == 2
    assert num_islands([]) == 0
    assert num_islands([[]]) == 0
    assert num_islands([["0"]]) == 0
    assert num_islands([["1"]]) == 1
    # All land is one island.
    assert num_islands([["1", "1"], ["1", "1"]]) == 1
    # Diagonal cells are NOT connected.
    assert num_islands([["1", "0"], ["0", "1"]]) == 2
    # A checkerboard is all singletons.
    grid = [["1" if (r + c) % 2 == 0 else "0" for c in range(4)] for r in range(4)]
    assert num_islands(grid) == 8
    # The input must not be mutated.
    original = [["1", "1"], ["0", "1"]]
    snapshot = [row[:] for row in original]
    num_islands(original)
    assert original == snapshot, "num_islands must not destroy its argument"
    # Scale: 300x300 of solid land must not recurse to death.
    big = [["1"] * 300 for _ in range(300)]
    assert num_islands(big) == 1

def test_p02_count_components():
    """Count Connected Components — BFS/DFS over an adjacency list (Medium)."""
    assert count_components(5, [(0, 1), (1, 2), (3, 4)]) == 2
    assert count_components(5, [(0, 1), (1, 2), (2, 3), (3, 4)]) == 1
    assert count_components(0, []) == 0
    # No edges at all: every node is its own component.
    assert count_components(4, []) == 4
    assert count_components(1, []) == 1
    # A self-loop does not connect anything new.
    assert count_components(3, [(0, 0)]) == 3
    # Duplicate edges must not change the count.
    assert count_components(3, [(0, 1), (0, 1), (1, 0)]) == 2
    # A cycle is still one component.
    assert count_components(3, [(0, 1), (1, 2), (2, 0)]) == 1
    # Scale.
    chain = [(i, i + 1) for i in range(99_999)]
    assert count_components(100_000, chain) == 1

def test_p03_topological_order():
    """Topological Sort — Kahn's algorithm (Medium)."""
    assert topological_order(4, [(0, 1), (1, 2), (2, 3)]) == [0, 1, 2, 3]
    # A cycle yields the empty list.
    assert topological_order(2, [(0, 1), (1, 0)]) == []
    assert topological_order(3, [(0, 1), (1, 2), (2, 0)]) == []
    # A self-loop is a cycle.
    assert topological_order(1, [(0, 0)]) == []
    # No edges: smallest-first gives sorted order.
    assert topological_order(3, []) == [0, 1, 2]
    assert topological_order(0, []) == []
    # A diamond is a valid DAG, not a cycle - this is the case a, # two-state visited check wrongly rejects.
    assert topological_order(4, [(0, 1), (0, 2), (1, 3), (2, 3)]) == [0, 1, 2, 3]
    # Any returned order must respect every edge.
    edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    order = topological_order(6, edges)
    assert len(order) == 6
    pos = {node: i for i, node in enumerate(order)}
    assert all(pos[u] < pos[v] for u, v in edges)

def test_p04_has_cycle_directed():
    """Detect A Cycle In A Directed Graph — DFS with three colours (Medium)."""
    assert has_cycle_directed(2, [(0, 1), (1, 0)]) is True
    # The diamond: a valid DAG that a two-state check wrongly rejects.
    assert has_cycle_directed(4, [(0, 1), (0, 2), (1, 3), (2, 3)]) is False
    assert has_cycle_directed(0, []) is False
    assert has_cycle_directed(3, []) is False
    # A self-loop is a cycle.
    assert has_cycle_directed(1, [(0, 0)]) is True
    # A chain is acyclic, closing it makes a cycle.
    assert has_cycle_directed(4, [(0, 1), (1, 2), (2, 3)]) is False
    assert has_cycle_directed(4, [(0, 1), (1, 2), (2, 3), (3, 0)]) is True
    # Direction matters: two edges the same way are not a cycle.
    assert has_cycle_directed(2, [(0, 1), (0, 1)]) is False
    # A cycle in one component, reached from another.
    assert has_cycle_directed(5, [(0, 1), (2, 3), (3, 4), (4, 2)]) is True
    # Cross-check against topological sort, which detects cycles too.
    for n_nodes, es in (
        (4, [(0, 1), (1, 2), (2, 3)]),
        (4, [(0, 1), (1, 2), (2, 3), (3, 1)]),
        (5, [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]),
        (3, [(0, 1), (1, 2), (2, 0)]),
    ):
        assert has_cycle_directed(n_nodes, es) is (topological_order(n_nodes, es) == []), es
    # Scale: a long chain must not recurse.
    long_chain = [(i, i + 1) for i in range(99_999)]
    assert has_cycle_directed(100_000, long_chain) is False

def test_p05_can_finish_courses():
    """Course Schedule — Cycle detection on prerequisites (Medium)."""
    assert can_finish_courses(2, [(1, 0)]) is True
    assert can_finish_courses(2, [(1, 0), (0, 1)]) is False
    assert can_finish_courses(1, []) is True
    assert can_finish_courses(5, []) is True
    # A long prerequisite chain is fine.
    assert can_finish_courses(4, [(1, 0), (2, 1), (3, 2)]) is True
    # Closing the chain makes it impossible.
    assert can_finish_courses(4, [(1, 0), (2, 1), (3, 2), (0, 3)]) is False
    # A diamond of prerequisites is satisfiable.
    assert can_finish_courses(4, [(1, 0), (2, 0), (3, 1), (3, 2)]) is True
    # A course that is its own prerequisite.
    assert can_finish_courses(2, [(0, 0)]) is False
    # Duplicated prerequisites must not create a false cycle.
    assert can_finish_courses(2, [(1, 0), (1, 0)]) is True

def test_p06_rotting_oranges():
    """Rotting Oranges — Multi-source BFS (Medium)."""
    assert rotting_oranges([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    # An unreachable fresh orange.
    assert rotting_oranges([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
    # No fresh oranges: zero minutes, not -1.
    assert rotting_oranges([[0, 2]]) == 0
    assert rotting_oranges([[0]]) == 0
    assert rotting_oranges([[2]]) == 0
    # A fresh orange with no rotten neighbour anywhere.
    assert rotting_oranges([[1]]) == -1
    assert rotting_oranges([[1, 0, 2]]) == -1
    # Adjacent: one minute.
    assert rotting_oranges([[2, 1]]) == 1
    # Multi-source really is simultaneous - two sources halve the time.
    assert rotting_oranges([[2, 1, 1, 1, 2]]) == 2
    assert rotting_oranges([[2, 1, 1, 1, 1]]) == 4
    # The input must not be mutated.
    original = [[2, 1], [1, 1]]
    snapshot = [row[:] for row in original]
    rotting_oranges(original)
    assert original == snapshot

def test_p07_shortest_path_grid():
    """Shortest Path In A Binary Matrix — BFS with 8-directional moves (Medium)."""
    # Diagonal movement makes this 2, not -1.
    assert shortest_path_grid([[0, 1], [1, 0]]) == 2
    assert shortest_path_grid([[0, 0, 0], [1, 1, 0], [1, 1, 0]]) == 4
    # Blocked start.
    assert shortest_path_grid([[1, 0], [0, 0]]) == -1
    # Blocked end.
    assert shortest_path_grid([[0, 0], [0, 1]]) == -1
    # A single open cell is a path of length 1.
    assert shortest_path_grid([[0]]) == 1
    assert shortest_path_grid([[1]]) == -1
    # Fully open grid: the diagonal is the shortest route.
    assert shortest_path_grid([[0] * 5 for _ in range(5)]) == 5
    # A wall with no gap.
    blocked = [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    assert shortest_path_grid(blocked) == -1
    # Scale: 100x100 open grid.
    assert shortest_path_grid([[0] * 100 for _ in range(100)]) == 100

def test_p08_word_ladder():
    """Word Ladder Length — BFS over an implicit graph (Hard)."""
    assert word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
    # No "cog" in the list, so the target is unreachable.
    assert word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
    # One-step transformation.
    assert word_ladder("a", "c", ["a", "b", "c"]) == 2
    # Begin equals end, and end is in the list.
    assert word_ladder("hot", "hot", ["hot"]) == 1
    # Empty word list.
    assert word_ladder("hit", "cog", []) == 0
    # No possible intermediate.
    assert word_ladder("hit", "hot", ["dog"]) == 0
    assert word_ladder("hit", "hot", ["hot"]) == 2
    # A longer chain.
    words = ["hot", "dot", "dog", "lot", "log", "cog", "cot"]
    assert word_ladder("hit", "cog", words) == 4
    # begin need not be in the list, and a direct one-letter change, # needs no intermediate: aaa -> aac is 2 words, not 3.
    assert word_ladder("aaa", "aac", ["aab", "aac"]) == 2
    # Now force an intermediate by removing the direct target letter path.
    assert word_ladder("aaa", "abc", ["aab", "abb", "abc"]) == 4
