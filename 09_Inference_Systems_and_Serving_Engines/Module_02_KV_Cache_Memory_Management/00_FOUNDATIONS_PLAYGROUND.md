# Module 02: Beginner Playground - KV-Cache Memory Management


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to the **KV-Cache Memory Management** module!
If you've ever wondered why an AI server with **80 Gigabytes of VRAM** can suddenly crash when just 20 people ask questions simultaneously, the KV Cache is the culprit!

---

## 1. Why Do We Need a KV Cache?

In Transformer models, generating token $t+1$ requires calculating attention with all tokens $1 \dots t$:
$$\text{Attention}(Q_{t+1}, K_{1\dots t}, V_{1\dots t})$$

- **Without KV Cache**: At step 100, you'd have to re-evaluate tokens 1 through 99. At step 101, re-evaluate 1 through 100!
  This creates an **$O(S^2)$ nightmare** where generation slows down to a crawl.
- **With KV Cache**: You calculate $K$ and $V$ vectors for token $t$ ONCE, save them in GPU memory, and never recompute them! Generation becomes $O(1)$ compute per step!

---

## 2. The Catch: The Exploding Memory Footprint!

Where does the memory go?
Each token requires storing:
1. Key vector: $H_{\text{kv}} \times d_{\text{head}}$ numbers
2. Value vector: $H_{\text{kv}} \times d_{\text{head}}$ numbers
Across **all layers** in FP16 ($2$ bytes each):

$$\text{KV Bytes per Token} = 2 \times 2 \times \text{Layers} \times H_{\text{kv}} \times d_{\text{head}}$$

Let's look at real models:
- **Llama 3 8B** ($32$ layers, $8$ KV heads, $d=128$):
  $$2 \times 2 \times 32 \times 8 \times 128 = 131,072 \text{ bytes} = 128 \text{ KB per token}!$$
  For a $4,096$-token chat, 1 user takes **$512$ Megabytes** of KV cache!
- **Llama 3 70B** ($80$ layers, $8$ KV heads, $d=128$):
  $$2 \times 2 \times 80 \times 8 \times 128 = 327,680 \text{ bytes} = 320 \text{ KB per token}!$$
  For a $4,096$-token chat, 1 user takes **$1.31$ Gigabytes**!
  **Only 30 concurrent users will consume 40 GB of VRAM just for their KV caches!**
