# Module 06: Beginner Playground - Chunked Prefill & PD Disaggregation


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to **Chunked Prefill & Prefill-Decode (PD) Disaggregation**!
This is the cutting-edge serving architecture used by DeepSeek, Meta, and OpenAI to crush latency jitter and maximize GPU utilization.

---

## 1. The Convoy Problem: Why Big Prompts Ruin Everything

Imagine you are at an ice cream shop:
- You just want 1 scoop of vanilla (1 token decode, takes 1 second).
- Suddenly, someone in front of you orders **500 custom sundaes** (4,000-token prefill prompt)!
- You are stuck standing in line for 20 minutes because the counter is totally blocked!

In LLM serving, whenever a large prompt arrives, all active users experience a **massive freeze in token generation** (Inter-Token Latency spike)!

---

## 2. Solution 1: Chunked Prefill (Sarathi-Serve)

Instead of making all 500 sundaes at once:
- The kitchen makes **10 sundaes (512 tokens)**.
- Then serves a scoop of ice cream to waiting customers (**1 decode step**).
- Then makes another 10 sundaes...
- Both prompt processing and token generation progress smoothly side by side with zero jitter!

---

## 3. Solution 2: Prefill-Decode (PD) Disaggregation

Why even share the same kitchen?
- **Building A (Prefill Cluster)**: Giant, compute-heavy GPUs optimized for massive matrix multiplications.
- **Building B (Decode Cluster)**: High-memory-bandwidth GPUs optimized for streaming tokens at lightning speed.
- Once Building A computes the prompt KV-cache, it transfers the tensors over ultra-fast **RDMA networks** to Building B in milliseconds!
