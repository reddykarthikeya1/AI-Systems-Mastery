# Module 09: Beginner Playground - Context Optimization & NIAH Testing

Welcome to **Context Optimization & Needle-in-a-Haystack (NIAH) Testing**!
Modern LLMs boast massive context windows (128,000 to 1,000,000+ tokens).
You might think: *"Great! I can just dump 50 retrieved documents into the prompt and let the LLM figure it out!"*

**BEWARE: The "Lost in the Middle" Effect!**

---

## 1. The Lost in the Middle Phenomenon

Researchers at Stanford (Liu et al., 2024) discovered a shocking truth about Transformers:
- When key information is at the **very beginning** of the prompt: Model finds it 95% of the time!
- When key information is at the **very end** of the prompt: Model finds it 95% of the time!
- When key information is in the **middle (between 30% and 70% depth)**: Accuracy plunges to **under 40%**!

```
Model Accuracy vs Information Position:
100% |  \                                     /
     |   \                                   /
 50% |    \                                 /
     |     \_______________________________/
  0% +-------------------------------------------------->
    Start                Middle                 End
                 (The Valley of Forgetting)
```

---

## 2. The Solution: U-Shaped Context Reordering

Instead of sorting retrieved documents from best to worst:
- Place the **#1 most relevant document** at the **very end** (closest to the user question).
- Place the **#2 most relevant document** at the **very beginning**.
- Place the least relevant documents in the **middle**!
Accuracy immediately recovers across long prompts!
