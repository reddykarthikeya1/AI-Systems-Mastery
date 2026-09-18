"""Broken benchmark calculating efficiency on failed tasks."""

class BrokenHarness:
    def score(self, optimal, actual, success):
        return optimal / actual


def reproduce_defect():
    print("Scoring a successful-but-slow task against a fast-but-failed task...")
    harness = BrokenHarness()

    # Task A: the agent SUCCEEDED, but took 40 steps against an optimal 10-step plan.
    success_score = harness.score(optimal=10, actual=40, success=True)

    # Task B: the agent FAILED (gave up / crashed) after just 2 steps.
    failure_score = harness.score(optimal=10, actual=2, success=False)

    print(f"Task A -- SUCCEEDED in 40 steps (optimal=10): efficiency score = {success_score}")
    print(f"Task B -- FAILED after only 2 steps (optimal=10): efficiency score = {failure_score}")
    print("Expected: a failed task should never outscore a successful one (failure_score <= success_score)")
    print(f"Actual:   Failed task scores higher than the successful one: {failure_score > success_score}")


if __name__ == "__main__":
    reproduce_defect()
