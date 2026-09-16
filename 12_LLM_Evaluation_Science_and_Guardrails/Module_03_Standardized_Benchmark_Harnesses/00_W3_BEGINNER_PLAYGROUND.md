# Beginner Playground: Benchmark Harnesses & Decontamination

Welcome to Benchmark Harnesses! Standardized evaluations like MMLU, GSM8K, and HumanEval allow AI teams to compare models objectively.

---

## 1. The Core Mental Model: Pass@k & Benchmark Contamination

- **Pass@1**: Proportion of problems solved correctly on the first attempt.
- **Pass@k**: Probability that at least one of $k$ generated attempts passes verification.
- **Data Contamination**: Did the model memorize the test answers during pretraining? If the benchmark test set was accidentally in the training corpus, the model achieves 99% accuracy on the benchmark but fails in real life.

```
 Problem ---> [ Generate K Candidates ] ---> [ Run Unit Tests / Match Oracle ]
                                                           |
                                                (Any candidate passes?)
                                                           |
                                                   [ Pass@k Metric ]
```

---

## 2. Interactive Pure-Python Experiment: Pass@k Estimator

In the landmark HumanEval paper (Chen et al., 2021), Pass@k is calculated without generating combinatorially massive samples:
$$\text{Pass}@k = 1 - \frac{\binom{n - c}{k}}{\binom{n}{k}}$$

```python
import math

def calculate_pass_at_k(n: int, c: int, k: int) -> float:
    """Calculates pass@k given n total samples and c correct samples."""
    if n - c < k:
        return 1.0
    return 1.0 - (math.comb(n - c, k) / math.comb(n, k))

# Model generated n=10 samples, c=2 passed the unit tests
p1 = calculate_pass_at_k(n=10, c=2, k=1)
p5 = calculate_pass_at_k(n=10, c=2, k=5)

print(f"Pass@1 (Chance of 1 random sample passing): {p1:.2%}")
print(f"Pass@5 (Chance of at least 1 of 5 samples passing): {p5:.2%}")
```
