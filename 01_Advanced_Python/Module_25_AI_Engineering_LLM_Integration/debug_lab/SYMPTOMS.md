# Debug Lab: Module 25 — AI Engineering Traps

## How to Run
```bash
python debug_lab/broken_rag_agent.py
```

## Observed Symptoms
1. **Fractured tokens / word mangling**:
   Chunks break mid-word (`'9988-S'`, `'ECURE'`), making dense vector embeddings fail to match search queries for `'9988-SECURE'`.
2. **Context truncation without chunk overlap**:
   Information split across chunk boundary is completely lost during semantic similarity lookup.
