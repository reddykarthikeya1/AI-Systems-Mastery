# Module 05: Beginner Playground - Continuous & Iteration-Level Batching


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to **Continuous Batching** (the architecture pioneered by Orca and used by vLLM & TensorRT-LLM)!
In traditional deep learning serving (like ResNet or BERT), you batch 16 images together, run forward pass, and return 16 answers.
Why does that **fail completely** for Large Language Models?

---

## 1. The Elevator Analogy: Static vs Continuous Batching

Imagine an elevator in a 100-story building:
- **Static Batching (The Silly Elevator)**:
  The elevator waits until 8 passengers step on. It goes up.
  Passenger 1 wants Floor 3.
  Passenger 2 wants Floor 90.
  The elevator **forces Passenger 1 to stand trapped inside until Floor 90** before letting anyone out or in!
  GPUs running static batching sit idle generating blank `<pad>` tokens for finished requests until the longest request finishes!
- **Continuous Batching (The Smart Elevator)**:
  At **every single floor** (iteration), the doors open:
  - If a passenger reached their floor (generated `<eos>`), they step out immediately!
  - If someone is waiting in the lobby, they step into the empty slot immediately!
  - The GPU is **never idle, never computing useless padding**!

---

## 2. Why Continuous Batching Doubles Serving Capacity

```
Static Batching (Padding Waste):
Req 1: [Tok][Tok][Tok][PAD][PAD][PAD]  <-- 50% wasted compute!
Req 2: [Tok][Tok][Tok][Tok][Tok][Tok]

Continuous Batching (No Waste):
Step 1: Req 1 [Tok], Req 2 [Tok]
Step 2: Req 1 [Tok], Req 2 [Tok]
Step 3: Req 1 [EOS] -> Retired! Req 3 Admitted!
Step 4: Req 3 [Tok], Req 2 [Tok]
```
Throughput increases by **$2\times$ to $4\times$** with zero hardware changes!
