# Module 08: Beginner Playground - Model Quantization for Serving

Welcome to **Model Quantization**!
A 70 Billion parameter model in FP16 takes **140 Gigabytes of VRAM**.
Can we shrink that model down to **35 Gigabytes** and run it on a single GPU without losing its intelligence?

Yes! Welcome to **FP8, INT8, and INT4 Quantization**!

---

## 1. The Suitcase Vacuum Bag Analogy

- **FP16 (16 bits per number)**: Packing wool sweaters unfolded in a giant suitcase. Takes 140 GB.
- **INT8 / FP8 (8 bits per number)**: Vacuum-sealing the sweaters. 50% smaller! Takes 70 GB.
- **INT4 (4 bits per number)**: Compressing everything down to minimal socks and shirts. 75% smaller! Takes 35 GB!

---

## 2. The Trap: Activation Outliers!

If you simply round every floating-point number to the nearest integer:
Most numbers in AI models are small (e.g. $0.05, -0.12, 0.08$).
Suddenly, in one channel, there is a giant number: **$128.5$**!
If your scale factor must fit $128.5$ into an 8-bit integer, all the small numbers ($0.05$) get rounded to **ZERO**! The model completely breaks!

### The Modern Solutions:
1. **AWQ (Activation-aware Weight Quantization)**: Identifies the 1% most critical weights (by looking at which weights multiply with large activation outliers) and keeps them in full precision, quantizing the remaining 99%!
2. **SmoothQuant**: Mathematically multiplies activations by a smoothing factor $S$ and divides weights by $S$, balancing the numbers so both round cleanly!
