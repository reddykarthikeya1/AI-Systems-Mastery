# Module 07: Beginner Playground - Microsoft GraphRAG & Knowledge Graphs


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to **GraphRAG**!
Traditional RAG (Vector Search) is great at answering localized questions like:
*"What was the price of Widget A in 2022?"*

But what happens when your CEO asks a **Global Sensemaking Question**:
> *"What are the main business risks across our entire 5,000-page corporate archive?"*

**Standard Vector Search Fails 100% of the Time!**
Why? Because there is no single chunk titled *"All Business Risks"*. The answer is spread across hundreds of documents!

Enter **Microsoft GraphRAG**!

---

## 1. How GraphRAG Solves Global Questions

Instead of treating documents as isolated text chunks:
1. **Entity & Relationship Extraction**: An LLM scans documents and builds a **Knowledge Graph**:
   - Entities: `Alice (Engineer)`, `Project Apollo (Initiative)`, `Budget Overrun (Risk)`
   - Edges: `Alice` --(leads)--> `Project Apollo` --(suffers)--> `Budget Overrun`
2. **Leiden Community Detection**: Graph clustering algorithms detect tightly-knit "communities" (neighborhoods) of related concepts.
3. **Hierarchical Summarization**: The system writes a summary report for each community.
4. **Global Query Answering**: When asked a global question, GraphRAG queries the **community summary reports**, providing a comprehensive synthesis of the entire corpus!
