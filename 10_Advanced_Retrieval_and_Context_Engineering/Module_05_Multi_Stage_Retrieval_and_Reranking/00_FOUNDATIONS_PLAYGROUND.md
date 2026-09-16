# Module 05: Beginner Playground - Multi-Stage Retrieval & Reranking

Welcome to **Multi-Stage Retrieval & Cross-Encoder Reranking**!
In search engineering, there is a fundamental law:
- **Fast search algorithms are imprecise.**
- **Precise search algorithms are slow.**

How do systems like Google, Amazon, and Cohere deliver both **instant speed** and **human-level precision**?

They use a **Two-Stage Funnel**!

---

## 1. The College Admissions Funnel Metaphor

1. **Stage 1: The Bi-Encoder / Vector Filter (Fast & Coarse)**:
   - Evaluates 1,000,000 documents in **5 milliseconds**.
   - Filters down to the **Top 50 candidate passages**.
   - Bi-encoders compare single compressed vectors: fast, but loses fine details.
2. **Stage 2: The Cross-Encoder Reranker (Slow & Ultra-Deep)**:
   - Takes only the 50 candidate passages.
   - Feeds the user query and each passage **together** into a deep Transformer:
     `[CLS] What is the interest rate? [SEP] The prime lending rate is 5.5% [SEP]`
   - Every single word in the question interacts with every word in the document!
   - Selects the true **Top 3 perfect answers** in **20 milliseconds**!

Total search time: **25 milliseconds** with 100% precision!
