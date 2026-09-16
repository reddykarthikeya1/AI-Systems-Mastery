"""Broken evaluator with zero claim parsing or groundedness check."""

class BrokenEvaluator:
    def evaluate(self, answer, context):
        # BUG: Blind string contains check; passes if any word matches
        return 1.0 if answer[:5] in context else 0.0
