# Module 06: Beginner Playground - ColBERTv2 & Late Interaction


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to **ColBERTv2** (Contextualized Late Interaction over BERT)!
In the previous module, we learned that:
- Bi-Encoders compress an entire 500-word passage into a **single vector** (lossy!).
- Cross-Encoders evaluate full word-to-word attention, but take too long!

What if you could keep **all token vectors** and compute word-to-word alignment in **just 10 milliseconds**?

Welcome to **ColBERT's Late Interaction**!

---

## 1. How Late Interaction Works: The MaxSim Operator

Instead of collapsing a document into 1 vector:
- Query $Q$ has 5 token vectors: $(q_1, q_2, q_3, q_4, q_5)$
- Document $D$ has 100 token vectors: $(d_1, d_2, \dots, d_{100})$

For every single query word:
1. Find the **highest similarity match** across all words in the document (**Max**).
2. Sum those best scores together (**Sim**)!

$$\text{Score}(Q, D) = \sum_{i \in Q} \max_{j \in D} (q_i \cdot d_j)$$

```
Query Token "Leaky"   --> [Max similarity with Document Token "Dripping"] = 0.88
Query Token "Faucet"  --> [Max similarity with Document Token "Pipe"]     = 0.91
Query Token "Fix"     --> [Max similarity with Document Token "Repair"]   = 0.85

Total MaxSim Score = 0.88 + 0.91 + 0.85 = 2.64!
```

---

## 2. Why is ColBERTv2 So Fast?

- Document token embeddings are pre-computed offline and compressed using **centroid quantization** down to $< 2$ bits per dimension!
- When a query arrives, vector dot products execute in fast GPU registers without launching heavy transformer layers!
- You get **Cross-Encoder precision at Bi-Encoder speed**!
