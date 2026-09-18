"""Broken evaluator with zero claim parsing or groundedness check."""

class BrokenEvaluator:
    def evaluate(self, answer, context):
        return 1.0 if answer[:5] in context else 0.0


def reproduce_defect():
    print("Scoring a hallucinated answer and an accurate paraphrase against the same context...")
    evaluator = BrokenEvaluator()
    context = "The Eiffel Tower was completed in 1889 and stands 330 meters tall."

    hallucinated_answer = "The Eiffel Tower was designed by Michelangelo and completed in 1750."
    paraphrased_answer = "Standing 330 meters tall, the tower was finished in 1889."

    score_hallucinated = evaluator.evaluate(hallucinated_answer, context)
    score_paraphrase = evaluator.evaluate(paraphrased_answer, context)

    print(f"Context: {context!r}")
    print(f"Hallucinated answer (wrong architect, wrong century): {hallucinated_answer!r}")
    print(f"  -> Expected groundedness score: 0.0 | Actual: {score_hallucinated}")
    print(f"Accurate, paraphrased answer: {paraphrased_answer!r}")
    print(f"  -> Expected groundedness score: 1.0 | Actual: {score_paraphrase}")


if __name__ == "__main__":
    reproduce_defect()
