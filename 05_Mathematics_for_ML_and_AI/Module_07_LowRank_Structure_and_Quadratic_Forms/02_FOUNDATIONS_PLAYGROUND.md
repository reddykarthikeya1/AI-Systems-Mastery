# 🐣 Interactive Foundations Playground: SVD, Low-Rank & Quadratic Forms

> *"Singular Value Decomposition (SVD) is the master key of linear algebra: any matrix, square or rectangular, fat or tall, can be factored into a rotation, a scaling, and another rotation."*

---

## 1. What is SVD? (The 3-Step Dance)

Every matrix $A$ transforms space. SVD proves that **any** transformation can be decomposed into:
$$A = U \Sigma V^T$$

1. **$V^T$ (First Rotation)**: Rotate the input coordinate axes to align with the primary directions of the data.
2. **$\Sigma$ (Axis Scaling)**: Stretch or shrink along those axes by factors called **singular values** ($\sigma_1 \ge \sigma_2 \ge \dots \ge 0$).
3. **$U$ (Second Rotation)**: Rotate into the output coordinate space.

---

## 2. Low-Rank Compression: The Eckart-Young Magic

Suppose you have a $1000 \times 1000$ weight matrix in a neural network (1,000,000 numbers).
- Often, the top 10 singular values hold **98% of the total energy**!
- By keeping only the top $r=10$ components, we approximate:
$$A \approx A_r = \sum_{i=1}^{r} \sigma_i u_i v_i^T$$
- Storing $A_r$ as $U_r \Sigma_r$ and $V_r^T$ takes only $1000 \times 10 + 10 \times 1000 = 20,000$ numbers — a **50x compression**!

---

## 3. What is LoRA? (Low-Rank Adaptation in Modern LLMs)

When fine-tuning a 70-billion parameter Large Language Model, updating all weights $\Delta W$ is computationally impossible.
- Instead of learning a full $\Delta W \in \mathbb{R}^{d \times k}$, **LoRA** factorizes:
$$\Delta W = B \times A$$
where $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$ with rank $r \ll d$.
- During inference, the model output is $y = W_0 x + \Delta W x = W_0 x + B(Ax)$. Zero latency overhead!

---

## 4. Quadratic Forms: Bowls vs Saddles

An expression like $q(x) = x^T A x$ is called a **quadratic form**.
- If $x^T A x > 0$ for all non-zero $x$, $A$ is **Positive Definite**. Geometrically, it forms a bowl facing upwards with a unique global minimum.
- If some directions curve up and others curve down, it is **Indefinite** — creating a **saddle point** where naive optimizers can get trapped.
