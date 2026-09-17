# 🐣 Interactive Foundations Playground: AI Engineering: LLM Integration Patterns

> *"LLM integrations structure unpredictable text generation into deterministic typed systems."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import json
import re
```

---

## 1. Prompt Template String Interpolation

Prompt templates bind user variables into structured instructions while escaping delimiters.

```python
prompt_template = "System: You are an assistant.\nUser: Explain {concept} in {num_words} words."
rendered = prompt_template.format(concept="MapReduce", num_words=20)
assert "Explain MapReduce in 20 words" in rendered
assert "System:" in rendered
print("Prompt template rendered successfully.")
```

---

## 2. Structured JSON Extraction from Model Outputs

Robust parsers extract JSON blocks from LLM output even when surrounded by markdown code fences.

```python
llm_raw_response = 'Here is the extracted data:\n<json>\n{"entity": "AcmeCorp", "confidence": 0.98}\n</json>\nDone.'
pattern = re.compile(r"<json>\n(.*?)\n</json>", re.DOTALL)
match = pattern.search(llm_raw_response)
assert match is not None
parsed = json.loads(match.group(1))
assert parsed["entity"] == "AcmeCorp"
assert parsed["confidence"] == 0.98
print(f"Extracted structured JSON: {parsed}")
```

---

## 3. Simulating Streaming Token Generators

Streaming generation yields tokens incrementally to minimize time-to-first-token latency.

```python
def mock_llm_stream(response_text):
    tokens = response_text.split(" ")
    for tok in tokens:
        yield tok + " "

stream_tokens = list(mock_llm_stream("Python agents reason in iterative loops"))
full_text = "".join(stream_tokens).strip()
assert len(stream_tokens) == 6
assert full_text == "Python agents reason in iterative loops"
print(f"Streaming generated {len(stream_tokens)} tokens.")
```

---
