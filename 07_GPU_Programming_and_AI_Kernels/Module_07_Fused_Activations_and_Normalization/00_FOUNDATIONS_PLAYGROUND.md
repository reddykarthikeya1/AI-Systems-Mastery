# 🐣 Interactive Foundations Playground: Fused Activations & Normalization

> *"In deep learning inference, 80% of your GPU's time is spent reading and writing numbers that are immediately thrown away. Kernel fusion glues operations together so intermediate numbers live exclusively in ultra-fast registers, cutting memory traffic by 80%."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. The Memory Wall: Why Unfused PyTorch Is Slow

Consider computing standard LayerNorm in PyTorch:
$$y = \frac{x - \mu}{\sqrt{\sigma^2 + \epsilon}} \cdot \gamma + \beta$$

In naive, unfused code:
1. Kernel 1 reads $x$ from HBM $\to$ computes mean $\mu$ $\to$ writes to HBM.
2. Kernel 2 reads $x$ and $\mu$ $\to$ computes variance $\sigma^2$ $\to$ writes to HBM.
3. Kernel 3 reads $x, \mu, \sigma^2$ $\to$ subtracts and divides $\to$ writes normalized $x$ to HBM.
4. Kernel 4 reads normalized $x, \gamma, \beta$ $\to$ multiplies and adds $\to$ writes $y$ to HBM.

**The Catastrophe**: Your GPU transferred the entire tensor across slow global memory **4 times**!

---

## 2. Kernel Fusion: Everything in Registers!

In a **Fused RMSNorm** kernel:
1. Each GPU block loads one row of $x$ into fast registers and shared memory **once**.
2. Threads compute the mean square in registers: $\text{RMS} = \sqrt{\frac{1}{d} \sum x_i^2 + \epsilon}$.
3. Threads immediately scale: $y_i = \frac{x_i}{\text{RMS}} \times \gamma_i$.
4. Writes $y$ back to HBM **once**!
- **Memory Traffic**: Reduced from $4 \times$ to $1 \times$! Speedup is typically $3\times$ to $5\times$!

---

## 3. Fused SwiGLU: Modern LLM Activation

Modern architectures like LLaMA and Mistral use **SwiGLU**:
$$\text{SwiGLU}(x) = \text{Swish}(x W_1) \odot (x W_2) = (z_1 \cdot \sigma(z_1)) \odot z_2$$
A fused kernel computes the sigmoid $\sigma(z_1)$, multiplies by $z_1$, and multiplies by $z_2$ in a single hardware ALU cycle inside registers.

---

## 4. Online Safe Softmax: The Secret Sauce of FlashAttention

When computing Softmax across large sequences:
$$S_i = \frac{e^{x_i - m}}{\sum_j e^{x_j - m}}$$
Normally, you need 3 passes: (1) find max $m$, (2) compute sum of exponentials $l$, (3) divide.
**Online Softmax (Milakov & Gimelshein)** computes running max and running normalizer in a **single pass**!
When a new value $x_{new}$ arrives:
$$m_{new} = \max(m_{old},\; x_{new})$$
$$l_{new} = l_{old} \times e^{m_{old} - m_{new}} + e^{x_{new} - m_{new}}$$
Notice: multiplying $l_{old}$ by $e^{m_{old} - m_{new}}$ rescales previous partial sums to the new maximum instantly!
