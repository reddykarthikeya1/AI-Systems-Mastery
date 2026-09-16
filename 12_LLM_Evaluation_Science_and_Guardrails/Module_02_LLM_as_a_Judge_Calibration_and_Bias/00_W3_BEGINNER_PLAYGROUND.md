# Beginner Playground: LLM-as-a-Judge & Position Bias Calibration

Welcome to LLM-as-a-Judge! Using a powerful model (e.g. GPT-4) to evaluate smaller models is standard practice, but LLM judges suffer from severe human-like cognitive biases.

---

## 1. The Core Mental Model: Positional Bias & Swap Calibration

When an LLM judge is asked:
> *"Compare Answer A and Answer B. Which one is better?"*

LLMs exhibit **Position Bias**: they favor Answer A (or Answer B) simply based on order of presentation!

```
 Trial 1: [ Order: (Model X as A, Model Y as B) ] ---> Judge picks A (Model X wins)
 Trial 2: [ Order: (Model Y as A, Model X as B) ] ---> Judge picks A (Model Y wins!)
```

To achieve mathematical calibration, we perform **Swap-Pair Evaluation**:
1. Run evaluation with order $(A, B)$.
2. Run evaluation with swapped order $(B, A)$.
3. Model $X$ only wins if it wins BOTH trials or has higher aggregate score. If trials disagree, declare a **Tie**.

---

## 2. Interactive Pure-Python Experiment: Swap-Pair Calibrator

```python
def mock_biased_judge(candidate_a: str, candidate_b: str) -> str:
    # Biased judge that ALWAYS prefers Candidate A regardless of quality!
    return "A"

def calibrate_pairwise_decision(text_x: str, text_y: str):
    # Trial 1: X is A, Y is B
    res1 = mock_biased_judge(candidate_a=text_x, candidate_b=text_y)
    winner_trial_1 = "X" if res1 == "A" else "Y"

    # Trial 2: Y is A, X is B (Swapped)
    res2 = mock_biased_judge(candidate_a=text_y, candidate_b=text_x)
    winner_trial_2 = "Y" if res2 == "A" else "X"

    print(f"Trial 1 Winner: {winner_trial_1}")
    print(f"Trial 2 (Swapped) Winner: {winner_trial_2}")

    if winner_trial_1 == winner_trial_2:
        return f"Clear Winner: Model {winner_trial_1}"
    else:
        return "TIE (Position Bias Detected and Neutralized)"

print("Decision:", calibrate_pairwise_decision("Model X text", "Model Y text"))
```
