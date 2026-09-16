# Module 10: Beginner Playground - Scaling Laws, Profiling & FinOps


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to **Scaling Laws, Profiling & FinOps**!
Training state-of-the-art Large Language Models is among the most expensive engineering endeavors in human history.
Training a frontier AI model can cost **$50,000,000 to $200,000,000+** in electricity and GPU compute!

If your GPU cluster is misconfigured and runs at **25% efficiency instead of 50%**, you literally burned **$25 Million**!

---

## 1. What is MFU (Model FLOPs Utilization)?

Think of your car's engine. If the speedometer says top speed is 200 mph, but you can only drive 50 mph because your transmission is slipping, your car is at 25% efficiency.

In AI:
- An **NVIDIA H100 SXM5** GPU can perform **989 Trillion floating-point calculations per second (989 TFLOPs)** in BF16 precision.
- **Model FLOPs**: During training, processing **1 token** through a model with $\Phi$ parameters requires approximately:
  $$\text{FLOPs per token} = 6\Phi$$
  ($2\Phi$ for the forward pass, $4\Phi$ for the backward pass).

$$\text{MFU} = \frac{\text{Actual Tokens/sec} \times 6\Phi}{\text{Number of GPUs} \times \text{Peak Hardware FLOPs}}$$

- **< 30% MFU**: Poor. Severe network bottlenecks, pipeline bubbles, or CPU stalls.
- **35% - 45% MFU**: Standard industry production level.
- **> 50% MFU**: Elite / State-of-the-art (Meta Llama 3, DeepSeek V3).

---

## 2. Chinchilla Scaling Laws: How Big Should Your Model Be?

In 2020, OpenAI published Kaplan's scaling laws, which suggested making models much bigger than the data size.
In 2022, DeepMind's **Chinchilla** paper corrected this:
- If your compute budget $C$ increases by $10\times$, you should scale **model size ($N$)** and **training tokens ($D$)** in **equal proportions**:
  $$N \propto \sqrt{C}, \quad D \propto \sqrt{C}$$
- For compute-optimal pre-training:
  $$\text{Tokens} \approx 20 \times \text{Parameters}$$
  A 70B model requires $\approx 1.4 \text{ Trillion}$ tokens for compute-optimal training.

### Why did Llama 3 train on 15 Trillion tokens (200x parameters)?
**Inference Amortization!**
If billions of users will query your model for years, spending 10x more money during training to make a smaller model smarter saves billions of dollars during inference!
