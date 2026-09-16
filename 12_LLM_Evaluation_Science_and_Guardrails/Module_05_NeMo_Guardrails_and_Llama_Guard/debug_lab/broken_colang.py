"""Broken Colang engine with no safety audit or intent categorization."""

class BrokenColang:
    def process(self, text):
        # BUG: Blindly passes all text to LLM without safety rails
        return "DELEGATE_LLM"
