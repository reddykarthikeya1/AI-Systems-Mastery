# Project Guide: Building an Enterprise LLM Judge Calibration Engine

In this project, you will build an automated LLM Judge calibration engine with swap-pair position debiasing, verbosity normalization, and Cohen's Kappa calculation.

---

## Three-Tier Implementation Path

### Tier 1: Pairwise Swap-Pair Evaluation (Required)
- Implement `evaluate_pairwise(model_a, model_b, judge_fn)`: runs forward and swapped trials.
- Aggregate outcomes into WIN, LOSS, or TIE.

### Tier 2: Verbosity Penalty Normalization
- Compute length ratio between candidates.
- Apply length discount penalty when candidate length exceeds reference by $>1.5\times$ without adding factual substance.

### Tier 3: Agreement Metrics (Cohen's Kappa)
- Implement `compute_cohens_kappa(human_labels, judge_labels)`.
