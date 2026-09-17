# 🐣 Interactive Foundations Playground: Statistical Estimation from Samples

> *"Estimation is inferring the properties of the ocean from a bucket of seawater."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import math
```

---

## 1. Sample Mean as an Unbiased Estimator

The sample mean $\bar{x} = \frac{1}{N} \sum x_i$ is an unbiased estimator of the true population mean $\mu$.

```python
population_mean = 50.0
sample = [48.0, 52.0, 51.0, 49.0, 50.0]

sample_mean = sum(sample) / len(sample)
assert sample_mean == population_mean
print(f"Sample mean: {sample_mean} accurately estimates population mean {population_mean}")
```

---

## 2. Bessel's Correction for Sample Variance

Dividing by $N-1$ instead of $N$ corrects for downward bias when estimating population variance from small samples.

```python
n = len(sample)
biased_var = sum((x - sample_mean)**2 for x in sample) / n
unbiased_var = sum((x - sample_mean)**2 for x in sample) / (n - 1)

assert unbiased_var > biased_var, "Bessel's correction increases estimate to eliminate bias"
assert biased_var == 2.0
assert unbiased_var == 2.5
print(f"Biased variance (N={n}): {biased_var}, Unbiased variance (N-1={n-1}): {unbiased_var}")
```

---

## 3. Standard Error of the Mean (SEM)

The uncertainty of the sample mean shrinks proportionally to the square root of sample size: $\text{SEM} = \frac{\sigma}{\sqrt{N}}$.

```python
sigma = 10.0
sem_100 = sigma / math.sqrt(100)
sem_400 = sigma / math.sqrt(400)

assert sem_100 == 1.0
assert sem_400 == 0.5, "Quadrupling sample size cuts error in half"
print(f"SEM with N=100: {sem_100}, SEM with N=400: {sem_400}")
```

---
