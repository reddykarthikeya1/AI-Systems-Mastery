# Module 06: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: MaxSim Complexity vs Cross-Attention
**Question**: Derive the computational complexity of scoring 100 candidate documents (each length $D=200$ tokens) for a query of length $Q=10$ tokens with embedding dimension $d=128$ under ColBERT Late Interaction vs a standard Cross-Encoder Transformer.

**Solution**:
1. **ColBERT MaxSim Compute**:
   For each document, we compute matrix product $M = E_q \cdot E_d^T$:
   $$\text{FLOPs}_{\text{matmul}} = 2 \times |Q| \times |D| \times d = 2 \times 10 \times 200 \times 128 = 512,000 \text{ FLOPs} = 0.512 \text{ MFLOPs}$$
   For 100 documents: $51.2 \text{ MFLOPs}$.
   On GPU Tensor Cores, $51.2 \text{ MFLOPs}$ executes in **$< 0.1 \text{ ms}$**!
2. **Cross-Encoder Compute**:
   Evaluating a 12-layer BERT-base model over 100 sequences of length $L = |Q| + |D| = 210$:
   $$\text{FLOPs}_{\text{transformer}} \approx 100 \times (24 \times 210 \times 768^2) \approx 300 \times 10^9 \text{ FLOPs} = 300 \text{ GFLOPs}$$
   Takes $\approx 30-50 \text{ ms}$.
3. **Conclusion**: ColBERT achieves a **$5,000\times$ reduction in scoring FLOPs** while retaining fine-grained token-level cross-interaction!

---

### Scenario 2: Punctuation Masking & Query Augmentation
**Question**: Why does ColBERT apply punctuation damping / masking to query tokens during MaxSim summation?

**Solution**:
Common punctuation (commas, periods, question marks) frequently match random punctuation tokens in documents with high similarity.
Including unmasked punctuation tokens in the sum introduces noise that inflates scores for syntactically similar but semantically irrelevant documents.
ColBERT masks query punctuation or sets static punctuation weights to $0.0$.
