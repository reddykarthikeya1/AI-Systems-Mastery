# 🐣 Interactive Foundations Playground: MLOps, Dynamic Batching & Drift

> *"A trained model in a Jupyter notebook is a science project. A model deployed behind an auto-scaling dynamic batching inference gateway with drift detection is a business."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. Dynamic Batching: 10x Inference Throughput

A modern GPU can execute a forward pass for a batch of 32 requests in almost the **exact same time** as a single request!
- **Without Dynamic Batching**: If 32 users send queries at slightly different milliseconds, the GPU runs 32 sequential passes (e.g. $32 \times 10\text{ ms} = 320\text{ ms}$).
- **With Dynamic Batching (Triton / vLLM)**: An in-memory queue collects incoming queries for up to `max_wait_ms` (e.g. 2 ms). It packs all waiting queries into one $(B, D)$ tensor, runs 1 forward pass in 12 ms, and fans the answers back out. Throughput jumps from 100 QPS to 1,500 QPS!

---

## 2. Data Drift & Concept Drift

Once deployed, models silently degrade over time:
- **Data Drift**: The input distribution $P(X)$ changes (e.g. camera lens gets scratched, or new slang enters customer queries).
- **Concept Drift**: The relationship $P(Y \mid X)$ changes (e.g. inflation changes what constitutes a "high price").
- **Detection**: The **Kolmogorov-Smirnov (KS) Test** compares the empirical cumulative distribution function (eCDF) of production inputs against the training baseline. If the maximum distance $D$ exceeds a critical threshold, sound the alarm for automated retraining!
