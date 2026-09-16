"""Broken judge evaluator with zero position bias mitigation."""

class BrokenJudge:
    def evaluate(self, c1, c2, judge_fn):
        # BUG: Single evaluation pass; vulnerable to 100% position bias
        return judge_fn(c1, c2)
