"""Broken benchmark calculating efficiency on failed tasks."""

class BrokenHarness:
    def score(self, optimal, actual, success):
        # BUG: Gives high efficiency score to immediate failures!
        return optimal / actual
