# 🐣 Interactive Foundations Playground: Reading & Writing AI Research Papers

> *"Most 50-page AI papers can be summarized in 3 sentences: What was slow or broken? What clean mathematical trick fixed it? What ablation proved it wasn't just luck?"*

---

## 1. The 5-Minute arXiv Filter: Pass 1

Never read an AI paper from start to finish on your first pass! Follow the **Keshav 3-Pass Rule**:
1. **Title & Abstract**: Does this solve a problem you care about?
2. **Introduction & Final Paragraph**: What is their specific claimed contribution?
3. **Figure 1 & Architecture Diagram**: If they cannot explain their system in one diagram, they probably don't understand it themselves.
4. **Main Results Table**: Look at the bolded numbers. Did they beat the baseline by 0.2% or 20%?
5. **Conclusion**: Did they admit any major limitations?

---

## 2. How to Spot Bogus or Overhyped Research

When reviewing an AI paper, look for these 3 red flags:
1. **The Weak Baseline Trick**: Comparing their newly tuned model against an untuned, 5-year-old baseline with bad hyperparameters.
2. **No Ablation Table**: If they add 5 new tricks (new loss, new attention, new tokenizer) but don't ablate each one individually, trick #5 probably did all the work and the other 4 are useless baggage!
3. **Data Contamination**: Testing their model on benchmarks that were accidentally included in their web crawl pre-training corpus!

---

## 3. Anatomy of a Top-Tier NeurIPS / ICML Paper

```text
Section 1: Introduction (The Problem & The Gap)
Section 2: Related Work (Standing on the Shoulders of Giants)
Section 3: Method (First-Principles Mathematical Formulation)
Section 4: Experiments (Main Benchmarks vs SOTA)
Section 5: Ablation Studies (Proving which components mattered)
Section 6: Limitations & Broader Impact
```
