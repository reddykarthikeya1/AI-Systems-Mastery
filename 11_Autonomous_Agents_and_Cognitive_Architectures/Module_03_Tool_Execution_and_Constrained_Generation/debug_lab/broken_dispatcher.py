"""Broken tool dispatcher with zero argument validation or timeout."""

class BrokenToolDispatcher:
    def __init__(self):
        self.tools = {}

    def dispatch(self, name, args):
        # BUG: Directly executes without checking missing parameters or enforcing timeouts!
        return self.tools[name](**args)
