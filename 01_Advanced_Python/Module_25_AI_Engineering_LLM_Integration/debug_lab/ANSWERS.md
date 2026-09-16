# Debug Lab Answers: Module 25

<details>
<summary>Bug 1 & 2: Naive character chunking without overlap</summary>

### Root Cause
Vector embedding models require coherent semantic units (complete sentences or paragraphs). Slicing raw string indices splits words and fragments semantic context.

### Fix
Use recursive sentence-boundary aware chunking with sliding-window overlap:
```python
def semantic_chunk_text(text: str, chunk_size: int = 200, overlap: int = 40) -> list[str]:
    # Split by sentences first, then assemble with sliding overlap
    sentences = text.split(". ")
    ...
```
</details>
