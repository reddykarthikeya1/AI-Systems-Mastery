"""Broken Swarm engine with circular delegation and context loss."""

class BrokenSwarm:
    def __init__(self, agents):
        self.agents = agents

    def run(self, start, msg):
        curr = start
        # BUG: Unlimited while loop with zero cycle detection
        while True:
            target = self.agents[curr].get_next()
            if not target:
                return "Done"
            curr = target
