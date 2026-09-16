# Module 08: Beginner Playground - Query Transformation & Agentic RAG

Welcome to **Query Transformation & Agentic RAG**!
When users ask questions in real life, they are often vague, incomplete, or complex:
> *"Compare their performance in Q3."*
*(Who is "their"? Compare on what metrics? Revenue? Net Income? Delivery count?)*

If you send that query directly to a vector database, it returns garbage.

---

## 1. The Transformation Toolkit

1. **Sub-Query Decomposition**:
   - Query: *"Compare Tesla and BYD 2023 EV deliveries."*
   - Transformed into two distinct sub-searches:
     - Sub-Query 1: *"Tesla 2023 total electric vehicle deliveries"*
     - Sub-Query 2: *"BYD 2023 total electric vehicle deliveries"*
2. **HyDE (Hypothetical Document Embeddings)**:
   - Ask an LLM: *"Write a hypothetical 1-paragraph answer to: 'How do you fix a memory leak in asyncio?'"*
   - The LLM hallucinates a passage mentioning `tracemalloc`, `asyncio.all_tasks()`, and `gc.collect()`.
   - We **embed that hypothetical answer** to search the vector DB!
   - Dense embeddings match document-to-document much better than query-to-document!
3. **Agentic Corrective RAG (CRAG)**:
   - After retrieval, an evaluator agent checks: *"Do these documents actually answer the query?"*
   - If YES $\to$ Generate answer.
   - If NO $\to$ Rewrite query and search again!
