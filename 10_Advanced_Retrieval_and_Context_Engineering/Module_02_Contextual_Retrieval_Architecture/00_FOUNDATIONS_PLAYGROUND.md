# Module 02: Beginner Playground - Contextual Retrieval Architecture


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to **Contextual Retrieval** (the breakthrough popularized by Anthropic in 2024)!
When documents are chopped into chunks, critical situational context is lost.

Let's see why this ruins search and how a tiny 50-token prefix fixes it!

---

## 1. The Lost Context Mystery

Imagine your vector database stores this isolated chunk:
> *"The company's operating margin declined by 4.2% due to increased legal fees."*

If a user searches:
*"Why did Apple's margin drop in 2023?"*
The vector database computes similarity. But this chunk doesn't say **Apple**! It doesn't say **2023**!
The similarity score is terrible, and the chunk is never retrieved!

---

## 2. Anthropic's Contextual Retrieval Secret

Before creating embeddings, we pass the chunk and the entire parent document to a fast, cheap LLM and ask it:
*"In 1-2 sentences, provide the overarching context for this chunk."*

The LLM outputs:
> *"This chunk is from Apple Inc.'s 2023 Q3 10-Q filing, discussing Operating Expenses in the Services division."*

We prepend this header directly to the chunk text:
```
[Context: This chunk is from Apple Inc.'s 2023 Q3 10-Q filing, Services division.]
The company's operating margin declined by 4.2% due to increased legal fees.
```

When you embed this new enriched chunk:
- Both dense embeddings and BM25 keywords now contain **Apple**, **2023**, and **10-Q**!
- Retrieval failure drops by **$49\%$**!
