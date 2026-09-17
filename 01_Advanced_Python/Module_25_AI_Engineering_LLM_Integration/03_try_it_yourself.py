"""Beginner playground for Module 25 - AI Engineering: LLM Integration Patterns.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import json
import re

# -------------------------------------------- 1. Prompt Template String Interpolation
prompt_template = "System: You are an assistant.\nUser: Explain {concept} in {num_words} words."
rendered = prompt_template.format(concept="MapReduce", num_words=20)
assert "Explain MapReduce in 20 words" in rendered
assert "System:" in rendered
print("Prompt template rendered successfully.")

# -------------------------------------------- 2. Structured JSON Extraction from Model Outputs
llm_raw_response = 'Here is the extracted data:\n<json>\n{"entity": "AcmeCorp", "confidence": 0.98}\n</json>\nDone.'
pattern = re.compile(r"<json>\n(.*?)\n</json>", re.DOTALL)
match = pattern.search(llm_raw_response)
assert match is not None
parsed = json.loads(match.group(1))
assert parsed["entity"] == "AcmeCorp"
assert parsed["confidence"] == 0.98
print(f"Extracted structured JSON: {parsed}")

# -------------------------------------------- 3. Simulating Streaming Token Generators
def mock_llm_stream(response_text):
    tokens = response_text.split(" ")
    for tok in tokens:
        yield tok + " "

stream_tokens = list(mock_llm_stream("Python agents reason in iterative loops"))
full_text = "".join(stream_tokens).strip()
assert len(stream_tokens) == 6
assert full_text == "Python agents reason in iterative loops"
print(f"Streaming generated {len(stream_tokens)} tokens.")

print()
print("All checks passed.")
