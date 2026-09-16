# Module 01: Beginner Playground - Parsing & Hierarchical Chunking

Welcome to **Advanced Retrieval & Context Engineering**!
Retrieval-Augmented Generation (RAG) is only as good as the chunks you retrieve.
If you feed an LLM garbage, out-of-context snippets, it will hallucinate and make up facts!

---

## 1. The Shredded Contract Analogy

Imagine taking a 100-page enterprise software contract and running it through a dumb paper shredder that cuts every **300 words** into a chunk:
- Chunk 14 ends with: *"The Customer agrees to pay the annual fee of $1,000,000, except..."*
- Chunk 15 starts with: *"...if Section 4.2 termination notice is served within 30 days."*

If a user asks: *"Does the customer have to pay $1M?"*, a standard vector search might retrieve **only Chunk 14**!
The LLM reads Chunk 14 and authoritatively answers: *"Yes! They must pay $1,000,000!"*
**The company just lost a lawsuit because of naive chunking!**

---

## 2. The Solution: Parent-Child Hierarchical Chunking

Instead of choosing between tiny chunks (good for search) and big chunks (good for context), **we use BOTH**:

```
[Parent Chunk: Whole Section (1024 Tokens)]
    |
    +---> [Child Chunk 1 (256 Tokens)] -> Embedded in Vector DB
    +---> [Child Chunk 2 (256 Tokens)] -> Embedded in Vector DB
    +---> [Child Chunk 3 (256 Tokens)] -> Embedded in Vector DB
```

1. **Search Phase**: The query matches the sharp, granular **Child Chunk 2** in the vector database.
2. **Retrieval Phase**: The retriever looks up the **Parent Chunk ID** and passes the **entire Parent Section** to the LLM!
The LLM sees the complete context, the exceptions, the tables, and the nuances!
