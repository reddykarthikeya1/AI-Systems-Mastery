"""Broken judge evaluator with zero position bias mitigation."""

class BrokenJudge:
    def evaluate(self, c1, c2, judge_fn):
        return judge_fn(c1, c2)


def reproduce_defect():
    print("Comparing two equally-correct responses with argument order swapped...")

    def position_biased_judge_fn(candidate_a, candidate_b):
        # Simulates a real LLM judge's documented tendency to prefer whichever
        # response occupies the first slot of the prompt, regardless of content.
        return "A"

    judge = BrokenJudge()
    response_x = "Paris is the capital of France."
    response_y = "The capital of France is Paris."

    verdict_xy = judge.evaluate(response_x, response_y, position_biased_judge_fn)
    verdict_yx = judge.evaluate(response_y, response_x, position_biased_judge_fn)

    print(f"Response X: {response_x!r}")
    print(f"Response Y: {response_y!r}")
    print(f"evaluate(X, Y, judge_fn) -> winner slot: {verdict_xy!r}")
    print(f"evaluate(Y, X, judge_fn) -> winner slot: {verdict_yx!r}")
    print("Expected: swapping the slots should not make slot 'A' win both times")
    print(f"Actual:   Slot 'A' wins both times regardless of which response sits there: {verdict_xy == verdict_yx == 'A'}")


if __name__ == "__main__":
    reproduce_defect()
