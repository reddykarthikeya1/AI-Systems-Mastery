"""
Curriculum-Wide Diagram Expansion:
Injects technical Mermaid diagrams into:
- Course 05: Mathematics for ML & AI (All 12 Modules)
- Course 03: Databases & Storage Engines (Key Storage & Concurrency Modules)
- Course 11: Autonomous Agents (Modules 02-08)
- Course 12: LLM Evaluation & Safety (Modules 02-08)
"""

import os

EXPANSION_DIAGRAMS = {
    # -------------------------------------------------------------------------
    # COURSE 05: MATHEMATICS FOR ML & AI (All 12 Modules)
    # -------------------------------------------------------------------------
    ("05_Mathematics_for_ML_and_AI", "Module_01"): """## Set Theory & Sample Space Partitioning

```mermaid
flowchart TD
    subgraph Universal["Universal Sample Space Ω"]
        subgraph Subsets["Set Operations & Measure"]
            A["Event Set A"]
            B["Event Set B"]
            Intersect["Intersection A ∩ B<br/>(Joint Occurrence)"]
            Union["Union A ∪ B = A + B - (A ∩ B)"]
            CompA["Complement Aᶜ = Ω \\ A"]
        end
    end
    A --- Intersect --- B
    Intersect --> Union
    Universal --> CompA
```
""",

    ("05_Mathematics_for_ML_and_AI", "Module_02"): """## Propositional Logic & Deduction Inference Engine

```mermaid
flowchart LR
    P["Hypothesis P (Premise)"] --> Imp["Implication P ⟹ Q"]
    Imp --> Eq["Material Equivalence: ¬P ∨ Q"]
    Eq --> Contra["Contrapositive Law: ¬Q ⟹ ¬P (Logically Identical)"]
    Contra --> Proof["Proof by Contradiction: P ∧ ¬Q ⟹ ⊥ (False)"]
```
""",

    ("05_Mathematics_for_ML_and_AI", "Module_03"): """## Linear Transformation & Column Space Mapping: Ax = b

```mermaid
flowchart LR
    subgraph Domain["Input Domain ℝⁿ (Coordinates x)"]
        x["Vector x = [x₁, x₂, ..., xₙ]ᵀ"]
    end

    subgraph Map["Linear Map Matrix A (m × n)"]
        Col["Linear Combination of Columns:<br/>Ax = x₁ a₁ + x₂ a₂ + ... + xₙ aₙ"]
    end

    subgraph Codomain["Codomain ℝᵐ (Output Space)"]
        b["Vector b ∈ Col(A)"]
    end

    x --> Col --> b
```
""",

    ("05_Mathematics_for_ML_and_AI", "Module_04"): """## Fundamental Subspaces & Rank-Nullity Theorem

```mermaid
flowchart TD
    subgraph Rn["Domain Space ℝⁿ"]
        Row["Row Space Row(A)<br/>Dimension: r"]
        Null["Null Space Null(A)<br/>Dimension: n - r"]
        Row ---|Orthogonal Complement ⟂| Null
    end

    subgraph Rm["Codomain Space ℝᵐ"]
        Col["Column Space Col(A)<br/>Dimension: r"]
        LeftNull["Left Null Space Null(Aᵀ)<br/>Dimension: m - r"]
        Col ---|Orthogonal Complement ⟂| LeftNull
    end

    Row -->|Bijective Mapping via A| Col
    Null -->|Maps to Zero Vector 0| LeftNull
```
""",

    ("05_Mathematics_for_ML_and_AI", "Module_05"): """## Spectral Thinking: Eigenvector Invariance (Av = λv)

```mermaid
flowchart TD
    subgraph Arbitrary["Arbitrary Vector x"]
        x["x (Rotates and Scales under A)"]
    end

    subgraph Eigen["Eigenvector v"]
        v["Eigenvector v (Direction is Invariant!)"] --> Scale["Scaled purely by Scalar λ:<br/>A v = λ v"]
    end

    subgraph Eigendecomp["Matrix Diagonalization"]
        Diag["A = Q Λ Q⁻¹ = Σ λᵢ qᵢ qᵢᵀ"]
    end

    Scale --> Diag
```
""",

    ("05_Mathematics_for_ML_and_AI", "Module_06"): """## Orthogonal Projection onto Subspace W

```mermaid
flowchart TD
    b["Vector b ∈ ℝⁿ"] --> Proj["Orthogonal Projection onto Col(A):<br/>p = A (Aᵀ A)⁻¹ Aᵀ b"]
    b --> Error["Error Residual Vector:<br/>e = b - p"]
    Error --> Ortho["Orthogonality Condition:<br/>Aᵀ e = Aᵀ (b - Ax̂) = 0<br/>Error is perpendicular to every column in A!"]
```
""",

    ("05_Mathematics_for_ML_and_AI", "Module_07"): """## Singular Value Decomposition (SVD) Geometry: A = U Σ Vᵀ

```mermaid
flowchart LR
    UnitCircle["Input Unit Sphere in ℝⁿ"] -->|"1. Rotate by Vᵀ (Orthogonal Map)"| Rot1["Rotated Basis in ℝⁿ"]
    Rot1 -->|"2. Scale by Singular Values Σ (Dilation)"| Scaled["Hyper-ellipsoid in ℝᵐ (Radii σᵢ)"]
    Scaled -->|"3. Rotate by U (Orthogonal Map)"| Final["Transformed Output Space Col(A)"]
```
""",

    ("05_Mathematics_for_ML_and_AI", "Module_08"): """## Linear Algebra in Machine Learning: Normal Equations & Ridge

```mermaid
flowchart TD
    Data["Design Matrix X (N × d), Target y (N × 1)"] --> Loss["Least Squares Loss: ||X w - y||²"]
    Loss --> Grad["Gradient: ∇_w = 2 Xᵀ (X w - y) = 0"]
    Grad --> NormalEq["Normal Equations: (Xᵀ X) w = Xᵀ y"]
    NormalEq --> OLS["OLS Solution: w = (Xᵀ X)⁻¹ Xᵀ y"]
    NormalEq --> Ridge["Ridge Regularization (L2):<br/>w_ridge = (Xᵀ X + λ I)⁻¹ Xᵀ y<br/>(Always invertible!)"]
```
""",

    ("05_Mathematics_for_ML_and_AI", "Module_09"): """## Multivariable Calculus: Gradient & Hessian Curvature

```mermaid
flowchart TD
    Loss["Multivariable Function f(x, y)"] --> Grad["Gradient ∇f = [∂f/∂x, ∂f/∂y]ᵀ<br/>(Steepest Ascent Vector)"]
    Loss --> Hessian["Hessian Matrix H = [∂²f/∂x², ∂²f/∂x∂y; ∂²f/∂y∂x, ∂²f/∂y²]<br/>(Local Curvature Tensor)"]
    
    Hessian --> PosDef["H is Positive Definite (Eigenvalues > 0) ⟹ Local Minimum!"]
    Hessian --> NegDef["H is Negative Definite (Eigenvalues < 0) ⟹ Local Maximum!"]
    Hessian --> Indef["H has Mixed Signs ⟹ Saddle Point!"]
```
""",

    ("05_Mathematics_for_ML_and_AI", "Module_10"): """## Bayesian Reasoning & Belief Update Engine

```mermaid
flowchart LR
    Prior["Prior Belief P(θ)<br/>(Initial Confidence)"] --> Likelihood["Likelihood P(D | θ)<br/>(Evidence from Observed Data)"]
    Likelihood --> Bayes["Bayes' Theorem:<br/>P(θ | D) = P(D | θ) P(θ) / P(D)"]
    Bayes --> Posterior["Posterior Belief P(θ | D)<br/>(Updated Knowledge)"]
    Posterior --> Predictive["Posterior Predictive Distribution"]
```
""",

    ("05_Mathematics_for_ML_and_AI", "Module_11"): """## Covariance Matrix & Principal Components Ellipsoid

```mermaid
flowchart TD
    Data["Zero-Mean Data Matrix X"] --> Cov["Sample Covariance Matrix:<br/>Σ = (1/N) Xᵀ X"]
    Cov --> Spectral["Eigendecomposition: Σ = V Λ Vᵀ"]
    Spectral --> PC1["1st Principal Component (v₁):<br/>Direction of Maximum Variance (λ₁)"]
    Spectral --> PC2["2nd Principal Component (v₂ ⟂ v₁):<br/>Orthogonal Direction of 2nd Largest Variance (λ₂)"]
```
""",

    ("05_Mathematics_for_ML_and_AI", "Module_12"): """## Statistical Estimation: MLE vs MAP

```mermaid
flowchart TD
    Likelihood["Likelihood Function L(θ) = ∏ p(xᵢ | θ)"] --> LogLike["Log-Likelihood ℓ(θ) = Σ log p(xᵢ | θ)"]
    LogLike --> MLE["MLE: θ̂_MLE = argmax ℓ(θ)<br/>(Pure data fit, no prior)"]

    Prior["Prior Distribution p(θ)"] --> MAP["MAP: θ̂_MAP = argmax [ℓ(θ) + log p(θ)]<br/>(Equivalent to Regularized Empirical Risk!)"]
```
""",

    # -------------------------------------------------------------------------
    # COURSE 03: DATABASES & STORAGE ENGINES (Key Modules)
    # -------------------------------------------------------------------------
    ("03_Databases_and_Storage_Engines", "Module_02"): """## Slotted-Page Physical Storage Architecture

```mermaid
flowchart TD
    subgraph Page["Physical 4KB / 8KB Database Page Frame"]
        Header["Page Header (LSN, TxID, Slot Count, FreeSpace Pointer)"]
        Slots["Slot Array (Line Pointers): [Slot 0: offset=3900, len=100] [Slot 1: offset=3750, len=150]"]
        FreeSpace["Free Unallocated Space Gap (Shrinks from middle)"]
        Tuple1["Tuple Record 1 (Variable-Length Data)"]
        Tuple0["Tuple Record 0 (Variable-Length Data)"]
    end

    Header --> Slots
    Slots --> FreeSpace
    FreeSpace --> Tuple1 --> Tuple0
```
""",

    ("03_Databases_and_Storage_Engines", "Module_03"): """## Buffer Pool Manager & CLOCK Replacement Algorithm

```mermaid
flowchart LR
    Req["Page Request (page_id)"] --> Hash["Page Hash Table (page_id -> frame_id)"]
    Hash -->|Hit| Frame["Return In-Memory Buffer Pool Frame (Increment Pin Count)"]
    Hash -->|Miss| Evict["CLOCK Replacement Policy (Search usage_bit == 0)"]
    Evict --> Flush["If Dirty Page: Write to Disk (Fsync)"]
    Flush --> Load["DMA Read Page from Disk into Free Frame"]
```
""",

    ("03_Databases_and_Storage_Engines", "Module_04"): """## B+ Tree Leaf Page Split & Parent Key Promotion

```mermaid
flowchart TD
    subgraph Before["Overflowing Leaf Page (Capacity = 4 keys)"]
        L["[10, 20, 30, 40, 50 (Overflow!)]"]
    end

    subgraph Split["50% Split & Invariant Maintenance"]
        L1["Left Leaf: [10, 20]"]
        L2["Right Leaf: [30, 40, 50]"]
        Promote["Promote Key 30 to Parent Index Node"]
        L1 -->|Doubly-Linked Sibling Pointer| L2
    end

    Before --> Split
```
""",

    ("03_Databases_and_Storage_Engines", "Module_05"): """## LSM-Tree Write Path: MemTable, WAL & SSTables

```mermaid
flowchart TD
    Write["Write Transaction PUT(key, val)"] --> WAL["1. Append-Only Write-Ahead Log (WAL) -> Sequential Disk IO"]
    Write --> MemTable["2. In-Memory SkipList / Red-Black Tree (MemTable)"]
    MemTable -->|MemTable Reaches Threshold (64MB)| Flush["3. Immutable MemTable Flushed as Level 0 SSTable"]
    Flush --> SSTable["Disk SSTable File (Sorted Data + Index Block + Bloom Filter)"]
```
""",

    ("03_Databases_and_Storage_Engines", "Module_08"): """## Two-Phase Locking (2PL) Concurrency Protocol

```mermaid
flowchart LR
    subgraph Phase1["Growing Phase"]
        L1["Acquire Shared Lock S(A)"] --> L2["Acquire Exclusive Lock X(B)"]
    end

    subgraph Peak["Lock Point (All Locks Held)"]
        LP["Transaction Mutates Records"]
    end

    subgraph Phase2["Shrinking Phase"]
        R1["Release Lock X(B)"] --> R2["Release Lock S(A) (No new locks can ever be acquired!)"]
    end

    Phase1 --> Peak --> Phase2
```
""",

    ("03_Databases_and_Storage_Engines", "Module_09"): """## MVCC Undo-Chain & Snapshot Visibility

```mermaid
flowchart LR
    subgraph ActiveRecord["Active Record in Slotted Page"]
        Cur["Row ID: 101<br/>xmin: 205 (Current Tx)<br/>val: 'Updated Value'"]
    end

    subgraph UndoLog["Undo Log Delta Chain"]
        V2["Version Tx 190<br/>val: 'Previous Value'"]
        V1["Version Tx 150<br/>val: 'Initial Value'"]
    end

    Cur -->|Rollback Pointer (roll_ptr)| V2
    V2 -->|roll_ptr| V1
```
""",

    # -------------------------------------------------------------------------
    # COURSE 11: AUTONOMOUS AGENTS (Modules 02-05)
    # -------------------------------------------------------------------------
    ("11_Autonomous_Agents_and_Cognitive_Architectures", "Module_02"): """## Agent Tool Calling & Schema Validation Engine

```mermaid
flowchart TD
    User["User Query"] --> LLM["LLM Function Calling Protocol"]
    LLM --> JSON["Structured JSON Tool Call: { name, arguments }"]
    JSON --> Validate["JSON Schema Validation (Pydantic / TypeGuard)"]
    Validate -->|Invalid Arguments| Reflect["Reflection Loop: Feed Schema Error back to LLM"]
    Validate -->|Valid| Exec["Execute Sandbox Tool Function"]
    Exec --> Result["Return Observation { stdout, exitCode }"]
    Result --> LLM
```
""",

    ("11_Autonomous_Agents_and_Cognitive_Architectures", "Module_03"): """## Plan-and-Solve Hierarchical Agent Architecture

```mermaid
flowchart TD
    Goal["Complex User Objective"] --> Planner["Planner Agent (Strategic Decomposition)"]
    Planner --> DAG["Execution DAG: [Subtask 1, Subtask 2, Subtask 3]"]
    DAG --> Worker1["Worker Agent: Execute Subtask 1"]
    DAG --> Worker2["Worker Agent: Execute Subtask 2 (Blocked on 1)"]
    Worker1 --> Synthesizer["Synthesizer Agent: Aggregate Evidence & Final Output"]
    Worker2 --> Synthesizer
```
""",

    ("11_Autonomous_Agents_and_Cognitive_Architectures", "Module_04"): """## Dual-Loop Evaluator & Self-Correction Reflection

```mermaid
flowchart TD
    Generator["Generator Agent: Draft Code / Solution"] --> Tester["Execution Sandbox: Run Assertion Suite"]
    Tester -->|All Tests Pass| Complete["Success Verified!"]
    Tester -->|AssertionError / Exception| Critic["Critic Agent: Analyze Traceback & Failure Root Cause"]
    Critic --> Memory["Episodic Memory: Record Error Pattern"]
    Critic --> Refine["Refinement Instructions -> Generator Agent (Loop 2)"]
    Refine --> Generator
```
""",

    ("11_Autonomous_Agents_and_Cognitive_Architectures", "Module_05"): """## Multi-Agent Consensus Debate Protocol

```mermaid
sequenceDiagram
    autonumber
    participant Prop as Proposer Agent
    participant Opp as Opponent Agent
    participant Mod as Moderator Agent (Judge)

    Prop->>Opp: Present Hypothesis & Justification
    Opp->>Prop: Rebuttal: Highlight Counter-Examples & Failure Scenarios
    Prop->>Opp: Defend with Empirical Benchmarks & Refined Claim
    Opp->>Mod: Submit Remaining Open Discrepancies
    Prop->>Mod: Submit Convergence Points
    Mod->>Mod: Synthesize Consensus Compromise
    Mod-->>Prop: Final Decision Report
```
""",

    # -------------------------------------------------------------------------
    # COURSE 12: EVALUATION SCIENCE & GUARDRAILS (Modules 02-05)
    # -------------------------------------------------------------------------
    ("12_LLM_Evaluation_Science_and_Guardrails", "Module_02"): """## The RAG Triad Evaluation Architecture

```mermaid
flowchart TD
    Q["User Query"] --> C["Retrieved Context Chunks"]
    C --> A["Generated Response Answer"]

    subgraph Triad["The 3 Pillars of RAG Quality"]
        Metric1["1. Context Relevance: Does Context answer the Query?"]
        Metric2["2. Groundedness: Is Answer strictly faithful to Context?"]
        Metric3["3. Answer Relevance: Does Answer directly address the Query?"]
    end

    Q -.-> Metric1 .- C
    C -.-> Metric2 .- A
    Q -.-> Metric3 .- A
```
""",

    ("12_LLM_Evaluation_Science_and_Guardrails", "Module_03"): """## LLM-as-a-Judge Pairwise Arena & Position Bias Calibration

```mermaid
flowchart TD
    Prompt["Benchmark Prompt"] --> M1["Model A Response"]
    Prompt --> M2["Model B Response"]

    subgraph Round1["Evaluation Round 1: [Model A, Model B]"]
        Judge1["Judge LLM: Select Winner (Round 1)"]
    end

    subgraph Round2["Evaluation Round 2: [Model B, Model A] (Position Swap!)"]
        Judge2["Judge LLM: Select Winner (Round 2)"]
    end

    M1 & M2 --> Round1
    M1 & M2 --> Round2

    Round1 & Round2 --> Calibrate["Bias Filter: Only award win if choice is consistent across both positions!"]
```
""",

    ("12_LLM_Evaluation_Science_and_Guardrails", "Module_04"): """## Automated Red-Teaming Adversarial Attack Pipeline

```mermaid
flowchart LR
    Attacker["Red-Team Attacker LLM"] --> Mutator["Jailbreak Mutator (Base64, Roleplay, Multilingual, Suffix Injection)"]
    Mutator --> Target["Target Production Model"]
    Target --> Output["Model Output"]
    Output --> SafetyJudge["Safety Classifier (Detect Policy Violation)"]
    SafetyJudge -->|Jailbreak Succeeded| Log["Log Vulnerability Vector into Adversarial Dataset"]
    SafetyJudge -->|Safely Refused| Attacker
```
""",

    ("12_LLM_Evaluation_Science_and_Guardrails", "Module_05"): """## Production Real-Time Guardrail Defense Layers

```mermaid
flowchart TD
    In["User HTTP Request"] --> L1["Layer 1: Regex & PII Redactor"]
    L1 --> L2["Layer 2: Fast Vector Embedding Safety Classifier (Llama-Guard)"]
    L2 -->|Safe| Model["Target LLM Inference"]
    L2 -->|Violation Detected| Block["403 Forbidden Blocked"]

    Model --> L3["Layer 3: Hallucination & Faithfulness NLI Verifier"]
    L3 -->|Faithful| Out["HTTP 200 Return Verified Response"]
    L3 -->|Unfaithful| Redact["Replace with Safe Grounded Fallback"]
```
""",
}

def inject_diagram(fpath, diagram):
    if not os.path.exists(fpath):
        return False
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    if "```mermaid" in text:
        return False

    lines = text.splitlines()
    insert_idx = len(lines)
    for i, line in enumerate(lines):
        if line.startswith('# ') and i < 15:
            for j in range(i + 1, min(len(lines), i + 25)):
                if lines[j].strip().startswith('## '):
                    insert_idx = j
                    break
            break

    new_lines = lines[:insert_idx] + ["\n" + diagram.strip() + "\n"] + lines[insert_idx:]
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write("\n".join(new_lines))
    return True

def main():
    count = 0
    for (course, mod_prefix), diagram in EXPANSION_DIAGRAMS.items():
        if not os.path.exists(course):
            continue
        mod_dirs = [d for d in os.listdir(course) if os.path.isdir(os.path.join(course, d)) and d.startswith(mod_prefix)]
        if not mod_dirs:
            continue
        mdir = os.path.join(course, mod_dirs[0])
        for cand in ['README.md', '01_README.md', '00_FOUNDATIONS_PLAYGROUND.md', '02_FOUNDATIONS_PLAYGROUND.md']:
            fpath = os.path.join(mdir, cand)
            if os.path.exists(fpath):
                if inject_diagram(fpath, diagram):
                    count += 1
                    print(f"Injected into {fpath}")
                    break

    print(f"\nTotal advanced diagrams injected: {count}")

if __name__ == '__main__':
    main()
