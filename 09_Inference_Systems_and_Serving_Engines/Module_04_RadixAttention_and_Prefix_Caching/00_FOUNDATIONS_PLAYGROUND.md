# Module 04: Beginner Playground - RadixAttention & Prefix Caching


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to **RadixAttention** and **Hierarchical Prefix Caching**!
If you've ever built an AI application with few-shot prompts, system prompts, or multi-turn chat, you know the frustration:
The user asks: *"Hello"*, and the AI engine recomputes the entire 2,000-word system prompt.
The user replies: *"Tell me more"*, and the engine recomputes the system prompt AND the previous conversation from scratch!

Why recompute identical tokens when we can **cache their KV tensors in a tree**?

---

## 1. The Radix Tree of Thought

Imagine a tree structure where every node represents a sequence of tokens that has already been evaluated:

```
[Root Node: Empty]
   |
   +---> ["System: You are an expert Python engineer..."] (KV Cached!)
            |
            +---> ["User: What is a generator?"] (KV Cached!)
            |        |
            |        +---> ["Assistant: A generator is..."] (Turn 1 response)
            |
            +---> ["User: How do metaclasses work?"] (Reuses System Prompt KV!)
```

When a new user prompt arrives:
1. SGLang traverses the tree from root.
2. It matches the token prefix against existing tree nodes.
3. It **reuses the cached KV blocks directly from GPU memory**!
4. It only computes prefill for the **brand new tokens at the end**!

**TTFT drops from $1,200\text{ ms}$ down to $15\text{ ms}$!**

---

## 2. LRU Eviction: What Happens When Memory Fills Up?

A Radix Tree cannot grow forever. When GPU memory reaches capacity:
- SGLang inspects the leaf nodes that have **0 active requests** currently using them.
- It evicts the **Least Recently Used (LRU)** leaf nodes, freeing their physical blocks back to the allocator.
- Shared popular prefixes (like the system prompt) stay warm in cache forever!
