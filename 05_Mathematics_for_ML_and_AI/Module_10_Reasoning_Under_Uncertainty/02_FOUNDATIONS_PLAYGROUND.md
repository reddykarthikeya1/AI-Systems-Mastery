# 🐣 Interactive Foundations Playground: Reasoning Under Uncertainty

> *"Probability is not about rolling dice in a casino; it is the logic of science when information is incomplete. Bayes' Theorem tells you exactly how much to update your belief when new evidence arrives."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. The Rare Disease Paradox (Base Rate Fallacy)

Suppose a rare disease affects **1 in 1,000 people** (0.1% prior).
You take a medical test with:
- **Sensitivity = 99%**: If you have it, test says POSITIVE 99% of the time.
- **False Positive Rate = 5%**: If you are healthy, test still says POSITIVE 5% of the time.

You test POSITIVE. Do you have a 99% chance of having the disease?
**NO! You only have ~1.9% chance!**

Why?
- In a crowd of 100,000 people:
  - 100 people are sick. 99 of them test positive.
  - 99,900 people are healthy. 5% of them (4,995 people) test positive!
- Total positive tests = $99 + 4,995 = 5,094$.
- Your chance of actually being sick = $99 / 5,094 \approx 1.94\%$!

---

## 2. Bayes' Theorem: The Machine Learning Belief Engine

$$P(\text{Hypothesis} \mid \text{Data}) = \frac{P(\text{Data} \mid \text{Hypothesis}) \times P(\text{Hypothesis})}{P(\text{Data})}$$

- **Prior $P(H)$**: What you believed before seeing the evidence.
- **Likelihood $P(D \mid H)$**: How probable the observed data would be if the hypothesis were true.
- **Posterior $P(H \mid D)$**: Your updated, rational belief after seeing the data!

---

## 3. Naive Bayes: Why "Naive" Works So Well in Practice

A Gaussian Naive Bayes classifier assumes that given the class label $y$, all features $x_1, x_2, \dots, x_d$ are **conditionally independent**:
$$P(x_1, x_2, \dots, x_d \mid y) = \prod_{j=1}^{d} P(x_j \mid y)$$
Even though features in real life are rarely independent, this "naive" assumption turns intractable multi-dimensional integrals into fast, stable products of 1D Gaussians!
