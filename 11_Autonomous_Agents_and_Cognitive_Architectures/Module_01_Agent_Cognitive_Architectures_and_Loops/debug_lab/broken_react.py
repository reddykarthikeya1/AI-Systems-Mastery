"""Broken ReAct implementation with action loop vulnerability."""

class BrokenReActEngine:
    def __init__(self, tools):
        self.tools = tools

    def run(self, goal, llm_fn):
        while True:
            response = llm_fn(goal)
            if "Final Answer:" in response:
                return response.split("Final Answer:")[1].strip()


def reproduce_defect():
    print("Running BrokenReActEngine against an LLM that never emits 'Final Answer:'...")
    calls = {"n": 0}
    SAFETY_CAP = 5000

    def llm_fn(goal):
        calls["n"] += 1
        if calls["n"] > SAFETY_CAP:
            raise RuntimeError(
                f"harness force-stopped the run after {calls['n']} LLM calls -- "
                "BrokenReActEngine.run() never returned on its own"
            )
        return "Thought: I should look that up again before answering."

    engine = BrokenReActEngine(tools={})
    try:
        engine.run("What is the capital of France?", llm_fn)
    except RuntimeError as e:
        print(f"HARNESS ABORT: {e}")

    print("Expected: run() returns a Final Answer within a small, bounded number of steps")
    print(f"Actual:   Total llm_fn calls before the forced abort: {calls['n']}")
    print("The goal string never changed and 'Final Answer:' was never produced.")


if __name__ == "__main__":
    reproduce_defect()
