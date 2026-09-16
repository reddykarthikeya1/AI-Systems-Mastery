# 🐣 W3Schools-Style Playground: Fine-Tuning, LoRA & DPO

> *"Full fine-tuning is throwing an entire encyclopedia into a blender to update one chapter. LoRA is writing a 1-page sticky note delta and slapping it on the back cover."*

---

## 1. Why Full Fine-Tuning Is Dead for Most Teams

When you fine-tune an LLM with 70 billion parameters:
- Model weights: 140 GB (16-bit float).
- Gradients: 140 GB.
- Optimizer States (Adam 32-bit): **560 GB**!
- Total GPU RAM needed: **$> 800 \text{ GB}$** (requiring an entire \$300,000 DGX cluster)!

---

## 2. LoRA: Low-Rank Adaptation

**The Core Insight (Hu et al., 2021)**:
Weight update matrices $\Delta W \in \mathbb{R}^{d \times k}$ have a very low "intrinsic dimension".
Instead of training all $d \times k$ parameters, we factorize:
$$\Delta W = \frac{\alpha}{r} (B \times A)$$
where $A \in \mathbb{R}^{r \times k}$ and $B \in \mathbb{R}^{d \times r}$ with rank $r \ll d$ (e.g. $r=8$ or $16$):
- **Initialization Trick**:
  - $A \sim \mathcal{N}(0, \sigma^2)$
  - $B = 0$
  - At step 0: $\Delta W = B \times A = 0$. The model starts **identically** to the base pre-trained model! Zero disruption!
- **Inference Magic**: During deployment, you can permanently merge $W_{merged} = W_0 + \frac{\alpha}{r} (B \times A)$ into the base weights. **Zero extra latency!**

---

## 3. Direct Preference Optimization (DPO)

Older RLHF required training 3 separate models:
1. Actor (LLM)
2. Reward Model (scoring human preference)
3. Critic / Reference Model (for PPO stability)

**DPO (Rafailov et al., 2023)** mathematically proves you don't need a reward model at all!
Given prompt $x$, chosen response $y_w$ and rejected response $y_l$, DPO optimizes the policy directly:
$$\mathcal{L}_{DPO} = -\log \sigma \left( \beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{ref}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{ref}(y_l \mid x)} \right)$$
If the model raises the probability of the chosen response relative to the rejected response, the loss drops. Simple, stable, and fast!
