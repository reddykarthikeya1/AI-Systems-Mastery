"""Broken tool dispatcher with zero argument validation or timeout."""

class BrokenToolDispatcher:
    def __init__(self):
        self.tools = {}

    def dispatch(self, name, args):
        return self.tools[name](**args)


def reproduce_defect():
    import time

    print("Dispatching tool calls through BrokenToolDispatcher...")
    dispatcher = BrokenToolDispatcher()
    dispatcher.tools = {
        "add": lambda a, b: a + b,
        "hang": lambda seconds: time.sleep(seconds) or "done",
    }

    print("Expected: a missing tool or a missing argument returns a structured error, never an unhandled exception")
    try:
        dispatcher.dispatch("add", {"a": 5})
    except TypeError as e:
        print(f"Actual:   dispatch('add', {{'a': 5}}) crashed instead of reporting a tool error: {type(e).__name__}: {e}")

    try:
        dispatcher.dispatch("subtract", {"a": 5, "b": 2})
    except KeyError as e:
        print(f"Actual:   dispatch('subtract', ...) crashed the whole process: {type(e).__name__}: {e}")

    start = time.time()
    dispatcher.dispatch("hang", {"seconds": 2})
    elapsed = time.time() - start
    print(f"Actual:   dispatch('hang', {{'seconds': 2}}) blocked the caller for {elapsed:.1f}s with no timeout enforced")


if __name__ == "__main__":
    reproduce_defect()
