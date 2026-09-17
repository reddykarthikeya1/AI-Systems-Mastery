# 🐣 Interactive Foundations Playground: Joint Distributions and Covariance

> *"Covariance measures whether two random variables dance in lockstep or step on each other's toes."*

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

## 1. Expected Value (Mean) Calculation

The expected value $E[X] = \sum x_i p_i$ is the probability-weighted center of mass of the distribution.

```python
outcomes = [1, 2, 3, 4, 5, 6]
probs = [1/6] * 6

expected_value = sum(x * p for x, p in zip(outcomes, probs))
assert abs(expected_value - 3.5) < 1e-6
print(f"Expected value of fair 6-sided die: {expected_value}")
```

---

## 2. Variance and Standard Deviation

Variance measures dispersion around the mean: $\text{Var}(X) = E[(X - \mu)^2]$.

```python
data = [10.0, 12.0, 23.0, 23.0, 16.0, 23.0, 21.0, 16.0]
mean = sum(data) / len(data)
variance = sum((x - mean)**2 for x in data) / len(data)
std_dev = math.sqrt(variance)

assert abs(mean - 18.0) < 1e-6
assert variance > 0.0
assert std_dev == math.sqrt(variance)
print(f"Dataset mean: {mean}, variance: {variance:.2f}, std dev: {std_dev:.2f}")
```

---

## 3. Sample Covariance and Positive Correlation

Positive covariance indicates that above-average values of $X$ coincide with above-average values of $Y$.

```python
xs = [1.0, 2.0, 3.0, 4.0, 5.0]
ys = [2.0, 4.0, 6.0, 8.0, 10.0]  # y = 2x, perfect correlation

mean_x = sum(xs) / len(xs)
mean_y = sum(ys) / len(ys)
cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / len(xs)

assert cov > 0.0, "Positive covariance"
assert cov == 4.0
print(f"Covariance between x and 2x: {cov}")
```

---
