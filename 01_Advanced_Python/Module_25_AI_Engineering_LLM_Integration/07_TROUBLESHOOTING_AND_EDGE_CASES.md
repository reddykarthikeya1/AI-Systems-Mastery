# Module 25: Troubleshooting, AI Traps & RAG Hallucinations

This reference guide details common errors and security vulnerabilities in AI engineering and RAG pipelines.

---

## 1. Chunk Boundary Truncation & Loss of Context

### The Problem
Splitting text strictly every 500 characters splits a critical sentence in half:
- *Chunk 1:* "...the annual interest rate is strictly"
- *Chunk 2:* "5.4% for premium accounts."
Retrieving Chunk 1 provides no actionable value.

### The Fix
Always use **Semantic Chunking with Overlap**:
```python
# ✅ Preserves 50-token overlapping buffer between adjacent chunks:
chunk_size = 500
chunk_overlap = 50
```

---

## 2. Preventing LLM Hallucinations in RAG

### The Prompt Architecture Fix
Enforce strict ground-truth constraints in your system prompt:
```text
System: You are an enterprise compliance assistant.
Rule 1: Answer the user's question ONLY based on the provided [CONTEXT] documents.
Rule 2: If the answer cannot be directly deduced from the context, state:
"I do not possess sufficient verified documentation to answer this question."
Do NOT invent or extrapolate facts.
```
