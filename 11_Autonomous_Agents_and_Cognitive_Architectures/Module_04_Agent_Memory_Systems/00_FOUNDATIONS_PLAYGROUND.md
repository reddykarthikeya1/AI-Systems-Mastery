# Beginner Playground: Multi-Tiered Agent Memory Systems

Welcome to Agent Memory Systems! An agent without memory treats every turn like the beginning of time. Real-world agents require cognitive memory inspired by human neuroscience.

---

## 1. The Core Mental Model: Human-Inspired Memory Hierarchy

```
 +---------------------------------------------------------+
 | Working Memory (Short-Term Buffer)                      |
 | -> Current conversation messages within active context  |
 +---------------------------------------------------------+
                             |
                   (Consolidation Threshold)
                             v
 +---------------------------------------------------------+
 | Episodic Memory (Long-Term Vector Log)                  |
 | -> Past interactions indexed by Recency + Importance    |
 +---------------------------------------------------------+
                             |
                   (Reflection & Extraction)
                             v
 +---------------------------------------------------------+
 | Semantic Memory (Entity & Fact Knowledge Store)         |
 | -> "User prefers concise answers", "User works in Python"|
 +---------------------------------------------------------+
```

---

## 2. Interactive Pure-Python Experiment: Stanford Generative Agents Memory Scoring

In the landmark Stanford *Generative Agents* paper (Park et al., 2023), episodic memory retrieval score is calculated as:
$$\text{Score} = \alpha \cdot \text{Recency} + \beta \cdot \text{Importance} + \gamma \cdot \text{Relevance}$$

Run this pure Python script:

```python
import math
import time

def calculate_retrieval_score(
    hours_ago: float,
    importance: float,     # 1 to 10
    relevance_sim: float,  # 0.0 to 1.0 cosine similarity
    decay_rate: float = 0.99
) -> float:
    # Recency exponential decay: decay_rate ^ hours_ago
    recency = math.pow(decay_rate, hours_ago)
    norm_importance = importance / 10.0

    # Weighted combination
    score = 0.3 * recency + 0.3 * norm_importance + 0.4 * relevance_sim
    return score

# Memory 1: Recent but trivial greeting
m1 = calculate_retrieval_score(hours_ago=0.1, importance=2, relevance_sim=0.1)

# Memory 2: Old but critical architectural rule
m2 = calculate_retrieval_score(hours_ago=48, importance=10, relevance_sim=0.9)

print(f"Memory 1 (Recent trivial) Score: {m1:.4f}")
print(f"Memory 2 (Old critical relevant) Score: {m2:.4f}")
```
