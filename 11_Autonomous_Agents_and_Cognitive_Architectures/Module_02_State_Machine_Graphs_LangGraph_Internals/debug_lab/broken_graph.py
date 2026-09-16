"""Broken state machine with race condition and missing reducers."""

class BrokenGraphEngine:
    def __init__(self):
        self.nodes = {}

    def run(self, state, start):
        curr = start
        while curr != "END":
            # BUG: In-place mutation breaks immutability & concurrent state guarantees
            state.update(self.nodes[curr](state))
            curr = "END"
        return state
