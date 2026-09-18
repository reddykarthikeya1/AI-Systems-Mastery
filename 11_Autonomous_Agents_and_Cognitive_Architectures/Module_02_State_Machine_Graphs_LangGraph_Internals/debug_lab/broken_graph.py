"""Broken state machine with race condition and missing reducers."""

class BrokenGraphEngine:
    def __init__(self):
        self.nodes = {}

    def run(self, state, start):
        curr = start
        while curr != "END":
            state.update(self.nodes[curr](state))
            curr = "END"
        return state


def reproduce_defect():
    print("Wiring a 3-node graph A -> B -> C -> END and running it once...")

    def node_a(state):
        return {"path": state["path"] + ["A"], "next": "B"}

    def node_b(state):
        return {"path": state["path"] + ["B"], "next": "C"}

    def node_c(state):
        return {"path": state["path"] + ["C"], "next": "END"}

    engine = BrokenGraphEngine()
    engine.nodes = {"A": node_a, "B": node_b, "C": node_c}

    state = {"path": []}
    checkpoint = state  # a caller holding a reference to the "before" state, e.g. for undo/replay

    result = engine.run(state, "A")

    print("Graph defined as: A -> B -> C -> END (3 nodes before END)")
    print("Expected path executed: ['A', 'B', 'C']")
    print(f"Actual path executed:   {result['path']}")
    print("Node the graph stopped at after one run() call: END (graph engine says done)")
    print(f"Checkpoint captured BEFORE run() was called still reads: {checkpoint['path']}")
    print(f"Is the pre-run checkpoint the exact same object as the post-run state? {checkpoint is result}")


if __name__ == "__main__":
    reproduce_defect()
