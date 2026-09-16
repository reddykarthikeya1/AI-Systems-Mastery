# Module 06: Pipeline Parallelism (PP) & Schedules

## 1. Architectural Principles of Pipeline Parallelism

Pipeline Parallelism partitions the sequential layers of a deep neural network across a linear chain of $p$ stages (devices).
Let $L$ denote total model layers. Stage $k \in \{0, \dots, p-1\}$ hosts layers $\left[k \cdot \frac{L}{p}, (k+1) \cdot \frac{L}{p} - 1\right]$.

### 1.1 Why Pipeline Parallelism is Network-Friendly
Unlike Tensor Parallelism which requires collective communication (`All-Reduce`) at every layer, Pipeline Parallelism requires only **point-to-point (P2P) communication** of activation tensors at stage boundaries:
- Stage $k$ sends activation $A_k \in \mathbb{R}^{b_{\mu} \times s \times h}$ to Stage $k+1$.
- Stage $k+1$ sends gradient $\frac{\partial L}{\partial A_k} \in \mathbb{R}^{b_{\mu} \times s \times h}$ back to Stage $k$.
Because communication volume is proportional only to hidden dimension $h$ (and not parameter size $\Phi$) and occurs only once per stage boundary, Pipeline Parallelism easily traverses **inter-node InfiniBand or high-speed Ethernet**.

---

## 2. Schedule Mechanics & Bubble Analysis

### 2.1 The GPipe Schedule
In GPipe (Huang et al., 2019):
1. An iteration is divided into $m$ micro-batches ($m \ge p$).
2. In the forward phase, all $m$ micro-batches are evaluated sequentially through stages $0 \to p-1$.
3. In the backward phase, gradients are backpropagated in reverse order $p-1 \to 0$.

$$\text{Bubble Fraction} = F_{\text{GPipe}} = \frac{p - 1}{m + p - 1}$$
$$\text{Peak Activation Memory} = O(m)$$

### 2.2 The 1F1B (One Forward, One Backward) Schedule
In 1F1B (Narayanan et al., 2021):
1. **Warmup Phase**: Stage $k$ executes $p - k - 1$ forward micro-batches.
2. **Steady-State Phase**: Stage $k$ alternates between executing one backward step and one forward step ($1F1B$).
3. **Cooldown Phase**: Stage $k$ drains remaining backward micro-batches.

$$\text{Bubble Fraction} = F_{\text{1F1B}} = \frac{p - 1}{m}$$
$$\text{Peak Activation Memory} = O(p)$$
Because $p \ll m$ in production training, 1F1B reduces activation memory footprint dramatically compared to GPipe.

```
1F1B Execution Timeline (p=4 stages, m=8 microbatches):
Stage 0: F1 F2 F3 F4 B1 F5 B2 F6 B3 F7 B4 F8 B5 .. B8
Stage 1: -- F1 F2 F3 B1 F4 B2 F5 B3 F6 B4 F7 B5 .. B8
Stage 2: ---- F1 F2 B1 F3 B2 F4 B3 F5 B4 F6 B5 .. B8
Stage 3: ------ F1 B1 F2 B2 F3 B3 F4 B4 F5 B5 .. B8
```

### 2.3 Interleaved 1F1B Schedule
Each physical GPU hosts multiple non-contiguous virtual stages. For example, with $v=2$ virtual stages on $p=4$ physical GPUs:
- GPU 0 holds Stage 0 (layers 1–4) and Stage 4 (layers 17–20).
- GPU 1 holds Stage 1 (layers 5–8) and Stage 5 (layers 21–24).

$$\text{Bubble Fraction} = F_{\text{interleaved}} = \frac{p - 1}{v \cdot m}$$
Interleaving reduces the bubble fraction by a factor of $v$ at the cost of additional network communication hops.
