# Module 07: Beginner Playground - Speculative Decoding & Medusa


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to **Speculative Decoding**!
If you could hire an ultra-fast intern to draft answers for an executive, and the executive only spent 1 second approving or fixing the draft, how much faster would work get done?

That is the magic of **Speculative Decoding**!

---

## 1. The Executive & Fast Assistant Metaphor

- **The Target Model (70B parameters)**: A brilliant executive. Can write Pulitzer-winning prose, but slow ($35 \text{ ms}$ per word) because loading 140 GB takes time.
- **The Draft Model (1B parameters)**: A speedy assistant. Types at blinding speed ($2 \text{ ms}$ per word) because it's tiny!

```
Step 1: The Draft Model guesses the next 4 words:
Draft: "The" -> "capital" -> "of" -> "France" -> "is" (Took 8 ms)

Step 2: The 70B Target Model verifies all 5 tokens IN PARALLEL in a SINGLE forward pass! (Took 35 ms)
Target: Accepts "The capital of France is" and predicts "Paris"!

Total Generated: 5 tokens in 43 ms = 8.6 ms per token!
Speedup: > 4x faster!
```

---

## 2. Does Speculative Decoding Hurt Model Quality?

**NO! Zero drop in quality!**
Using **Rejection Sampling**, mathematicians proved that the output distribution is **mathematically identical** to sampling directly from the giant 70B model!
If the assistant guesses wrong, the executive rejects the bad word, replaces it with its own true word, and the draft model starts guessing again.
