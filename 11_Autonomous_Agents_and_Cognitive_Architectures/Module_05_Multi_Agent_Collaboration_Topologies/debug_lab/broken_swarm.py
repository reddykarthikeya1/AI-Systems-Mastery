"""Broken Swarm engine with circular delegation and context loss."""

class BrokenSwarm:
    def __init__(self, agents):
        self.agents = agents

    def run(self, start, msg):
        curr = start
        while True:
            target = self.agents[curr].get_next()
            if not target:
                return "Done"
            curr = target


def reproduce_defect():
    print("Running a 3-agent swarm wired as planner -> researcher -> critic -> planner (a cycle)...")
    calls = {"n": 0}
    SAFETY_CAP = 5000

    class Agent:
        def __init__(self, name, next_name):
            self.name = name
            self.next_name = next_name

        def get_next(self):
            calls["n"] += 1
            if calls["n"] > SAFETY_CAP:
                raise RuntimeError(
                    f"harness force-stopped the run after {calls['n']} handoffs -- "
                    "BrokenSwarm.run() never reached 'Done'"
                )
            return self.next_name

    swarm = BrokenSwarm({
        "planner": Agent("planner", "researcher"),
        "researcher": Agent("researcher", "critic"),
        "critic": Agent("critic", "planner"),  # hands back to planner
    })

    print("Delegation topology: planner -> researcher -> critic -> planner -> ...")
    print("Expected: run() detects the cycle and terminates quickly instead of looping forever")
    try:
        swarm.run("planner", "draft a market analysis")
    except RuntimeError as e:
        print(f"Actual:   HARNESS ABORT: {e}")
    print(f"Actual:   Total handoffs before the forced abort: {calls['n']}")


if __name__ == "__main__":
    reproduce_defect()
