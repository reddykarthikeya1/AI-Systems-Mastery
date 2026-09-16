"""Broken ReAct implementation with action loop vulnerability."""

class BrokenReActEngine:
    def __init__(self, tools):
        self.tools = tools

    def run(self, goal, llm_fn):
        # BUG: No cycle detection or max step ceiling!
        while True:
            response = llm_fn(goal)
            if "Final Answer:" in response:
                return response.split("Final Answer:")[1].strip()
            # Executes without checking repetition
