"""
Curriculum-Wide Diagram & Scrubber Trace Generator
Generates technical, domain-accurate Mermaid diagrams and AlgorithmTraceScrubber trace blocks
across all courses (Courses 02, 03, 05, 06, 07, 08, 09, 10, 11, 12).
"""

import os
import re

# Target diagrams keyed by relative file pattern or (course, module)
DIAGRAMS = {
    # -------------------------------------------------------------------------
    # COURSE 02: DATA STRUCTURES & ALGORITHMS (All 17 Modules)
    # -------------------------------------------------------------------------
    ("02_Data_Structures_and_Algorithms", "Module_01"): """## Memory Hierarchy & Cache Locality Architecture

```mermaid
flowchart TD
    subgraph CPU["CPU Die"]
        subgraph Core["CPU Execution Core"]
            Reg["Registers<br/>(~1 KB, 0.5 ns)"]
        end
        L1["L1 Data Cache<br/>(32 KB, 1.0 ns, 4 cycles)<br/>64-Byte Line"]
        L2["L2 Cache<br/>(512 KB, 3.5 ns, 14 cycles)<br/>64-Byte Line"]
    end
    L3["L3 Shared Cache<br/>(32 MB, 12 ns, 50 cycles)<br/>64-Byte Line"]
    DRAM["Main Memory (DRAM)<br/>(64 GB, 60-100 ns, 200+ cycles)"]
    SSD["NVMe SSD Storage<br/>(2 TB, 10-50 µs, 50,000+ cycles)"]

    Reg <-->|Register Spill/Fill| L1
    L1 <-->|Cache Hit / Miss Line Fill| L2
    L2 <-->|Cross-Core Bus Snooping| L3
    L3 <-->|DDR5 Bus Transaction (64B)| DRAM
    DRAM <-->|PCIe Gen5 DMA Page Fault (4KB)| SSD

    classDef fast fill:#059669,stroke:#047857,color:#fff;
    classDef mid fill:#0284c7,stroke:#0369a1,color:#fff;
    classDef slow fill:#d97706,stroke:#b45309,color:#fff;
    classDef disc fill:#dc2626,stroke:#b91c1c,color:#fff;
    class Reg,L1 fast;
    class L2,L3 mid;
    class DRAM slow;
    class SSD disc;
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_02"): """## Dynamic Array Geometric Doubling & Pointer Layout

```mermaid
flowchart LR
    subgraph S1["Initial Capacity = 4"]
        A1["[0]: 10"] --- A2["[1]: 20"] --- A3["[2]: 30"] --- A4["[3]: 40"]
    end

    subgraph S2["Reallocation: Capacity = 8 (2x Factor)"]
        direction TB
        Alloc["1. Allocate Contiguous Heap Chunk (8 slots)"]
        Copy["2. Copy 4 elements to new memory buffer"]
        Append["3. Write new item [4]: 50 in O(1)"]
        Free["4. Free old memory block"]
        Alloc --> Copy --> Append --> Free
    end

    subgraph S3["New Buffer State"]
        B1["10"] --- B2["20"] --- B3["30"] --- B4["40"] --- B5["50"] --- B6["Free"] --- B7["Free"] --- B8["Free"]
    end

    S1 -->|Push 50 Triggers Doubling| S2 --> S3
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_03"): """## Linked List Pointer Mutation: In-Place Reversal Workflow

```mermaid
sequenceDiagram
    autonumber
    participant Prev as prev Pointer (None)
    participant Curr as curr Pointer (Node 1)
    participant Next as next_temp (Node 2)
    Note over Curr,Next: Step 1: Save next pointer to prevent orphan loss
    Curr->>Next: next_temp = curr.next
    Note over Prev,Curr: Step 2: Invert link direction backward
    Curr->>Prev: curr.next = prev
    Note over Prev,Curr: Step 3: Advance prev pointer forward
    Prev->>Curr: prev = curr
    Note over Curr,Next: Step 4: Advance curr pointer forward
    Curr->>Next: curr = next_temp
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_04"): """## Monotonic Decreasing Stack Invariant

```mermaid
flowchart TD
    subgraph Input["Input Stream: [2, 1, 5, 6, 2, 3]"]
        N1["2"] --> N2["1"] --> N3["5"] --> N4["6"]
    end

    subgraph StackOp["Stack Invariant: Elements strictly decrease top-to-bottom"]
        direction TB
        P1["Push 2: Stack=[2]"]
        P2["Push 1: Stack=[2, 1] (1 < 2 OK)"]
        P3["Arrive 5: Pop 1, Pop 2 (5 violates decreasing invariant!)<br/>Compute span/area for popped nodes<br/>Push 5: Stack=[5]"]
        P1 --> P2 --> P3
    end

    Input --> StackOp
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_05"): """## Hash Collision Resolution: Separate Chaining vs Robin Hood Probing

```mermaid
flowchart TD
    subgraph SC["Separate Chaining (Bucket Array + Linked Nodes)"]
        B0["Bucket 0"] --> N0["(K0, V0)"]
        B1["Bucket 1 (Collision)"] --> N1A["(K1, V1)"] --> N1B["(K4, V4)"]
        B2["Bucket 2"] --> N2["(K2, V2)"]
    end

    subgraph RH["Robin Hood Open Addressing (Linear Probing with PSL)"]
        R0["[0]: Key A (PSL = 0)"]
        R1["[1]: Key B (PSL = 1)"]
        R2["[2]: Key C (PSL = 2)"]
        R3["Insert Key D (PSL = 3) > Key C (PSL = 2) -> SWAP & DISPLACE"]
    end
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_06"): """## AVL Tree Double Rotation (Left-Right Case)

```mermaid
flowchart TD
    subgraph Before["Before Rotation (Imbalance at Node 50, BF = +2)"]
        N50["50 (BF=+2)"] --> N20["20 (BF=-1)"]
        N50 --> N60["60"]
        N20 --> N10["10"]
        N20 --> N30["30 (Right Child)"]
        N30 --> N25["25"]
        N30 --> N35["35"]
    end

    subgraph Step1["Step 1: Left Rotate at Child 20"]
        S50["50"] --> S30["30"]
        S30 --> S20["20"]
        S30 --> S35["35"]
        S20 --> S10["10"]
        S20 --> S25["25"]
    end

    subgraph Step2["Step 2: Right Rotate at Root 50 (Balanced)"]
        R30["30 (BF=0)"]
        R30 --> R20["20 (BF=0)"]
        R30 --> R50["50 (BF=0)"]
        R20 --> R10["10"]
        R20 --> R25["25"]
        R50 --> R35["35"]
        R50 --> R60["60"]
    end

    Before -->|Left Rotate (Child)| Step1 -->|Right Rotate (Root)| Step2
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_07"): """## Binary Min-Heap Array Mapping & Sift-Down Invariant

```mermaid
flowchart TD
    subgraph Tree["Heap Tree Representation"]
        H1["1 (idx 0)"]
        H1 --> H3["3 (idx 1)"]
        H1 --> H2["2 (idx 2)"]
        H3 --> H6["6 (idx 3)"]
        H3 --> H5["5 (idx 4)"]
        H2 --> H8["8 (idx 5)"]
        H2 --> H4["4 (idx 6)"]
    end

    subgraph Array["Contiguous Array Storage Layout"]
        A0["[0]: 1"] --- A1["[1]: 3"] --- A2["[2]: 2"] --- A3["[3]: 6"] --- A4["[4]: 5"] --- A5["[5]: 8"] --- A6["[6]: 4"]
    end

    subgraph Formulas["Index Math Formulas"]
        F1["Parent(i) = (i - 1) // 2"]
        F2["LeftChild(i) = 2*i + 1"]
        F3["RightChild(i) = 2*i + 2"]
    end
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_08"): """## DAG Topological Sort & In-Degree Reduction (Kahn's Algorithm)

```mermaid
flowchart LR
    A["Node A<br/>in-degree: 0"] --> B["Node B<br/>in-degree: 1"]
    A --> C["Node C<br/>in-degree: 1"]
    B --> D["Node D<br/>in-degree: 2"]
    C --> D
    D --> E["Node E<br/>in-degree: 1"]

    subgraph Queue["Zero In-Degree Queue Progress"]
        Q1["[A]"] -->|Pop A, decrement B & C| Q2["[B, C]"] -->|Pop B, C, decrement D| Q3["[D]"] -->|Pop D, decrement E| Q4["[E]"]
    end

    subgraph TopoOrder["Final Topological Ordering"]
        O["A -> B -> C -> D -> E"]
    end
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_09"): """## Dijkstra Shortest Path Relaxation Frontier

```mermaid
flowchart LR
    S(("Start S<br/>dist: 0")) -->|wt: 4| A(("Node A<br/>dist: 4"))
    S -->|wt: 2| B(("Node B<br/>dist: 2"))
    B -->|wt: 1| A
    B -->|wt: 5| C(("Node C<br/>dist: 7"))
    A -->|wt: 2| C
    C -->|wt: 3| T(("Target T<br/>dist: 8"))

    subgraph Relax["Relaxation Invariant"]
        R["if dist[u] + wt(u, v) < dist[v]:<br/>dist[v] = dist[u] + wt(u, v)<br/>pq.push((dist[v], v))"]
    end
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_10"): """## 1D Dynamic Programming: Longest Increasing Subsequence DAG

```mermaid
flowchart LR
    subgraph Array["Input Array"]
        I0["[0]: 10"] --- I1["[1]: 9"] --- I2["[2]: 2"] --- I3["[3]: 5"] --- I4["[4]: 3"] --- I5["[5]: 7"] --- I6["[6]: 101"]
    end

    subgraph DP["Subproblem Transition Dependencies"]
        D2["dp[2]=1 (val: 2)"] -->|2 < 5| D3["dp[3]=2 (val: 5)"]
        D2 -->|2 < 3| D4["dp[4]=2 (val: 3)"]
        D3 -->|5 < 7| D5["dp[5]=3 (val: 7)"]
        D4 -->|3 < 7| D5
        D5 -->|7 < 101| D6["dp[6]=4 (val: 101)"]
    end
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_11"): """## 2D Dynamic Programming: 0/1 Knapsack Grid Transitions

```mermaid
flowchart TD
    subgraph Grid["DP Table: dp[i][w] = Max Value using first i items with capacity w"]
        Cell["dp[i][w]"]
        Top["dp[i-1][w]<br/>(Option 1: Exclude item i)"]
        TopLeft["dp[i-1][w - weight[i]] + value[i]<br/>(Option 2: Include item i)"]

        Top -->|max| Cell
        TopLeft -->|max| Cell
    end

    subgraph Invariant["Bellman Optimality Condition"]
        B["dp[i][w] = max(dp[i-1][w], dp[i-1][w - wt[i]] + val[i]) if w >= wt[i] else dp[i-1][w]"]
    end
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_12"): """## Greedy Interval Scheduling: Earliest Finish Time Selection

```mermaid
gantt
    title Interval Scheduling: Greedy Optimal Selection
    dateFormat X
    axisFormat %s

    section Rejected
    Task A (Ends 4) : 0, 4
    Task C (Ends 7) : 3, 7
    Task E (Ends 9) : 6, 9

    section Selected (Optimal)
    Job 1 (Ends 2) :crit, active, 0, 2
    Job 2 (Ends 5) :crit, active, 2, 5
    Job 3 (Ends 8) :crit, active, 5, 8
    Job 4 (Ends 10) :crit, active, 8, 10
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_13"): """## Backtracking State-Space Tree Pruning (4-Queens)

```mermaid
flowchart TD
    R["Root (Empty Board)"]
    R --> Q0["Row 0: Col 0"]
    R --> Q1["Row 0: Col 1"]

    Q0 --> Q00["Row 1: Col 0 (Pruned: Col Conflict)"]
    Q0 --> Q01["Row 1: Col 1 (Pruned: Diag Conflict)"]
    Q0 --> Q02["Row 1: Col 2 (Valid)"]
    Q0 --> Q03["Row 1: Col 3 (Valid)"]

    Q02 --> Q020["Row 2: Col 0 (Pruned: Col Conflict)"]
    Q02 --> Q021["Row 2: Col 1 (Pruned: Diag Conflict)"]
    Q02 --> Q02X["All Row 2 Choices Pruned -> BACKTRACK!"]

    classDef pruned fill:#f87171,stroke:#dc2626,color:#fff;
    classDef valid fill:#34d399,stroke:#059669,color:#fff;
    class Q00,Q01,Q020,Q021,Q02X pruned;
    class Q02,Q03 valid;
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_14"): """## Segment Tree Binary Range Decomposition

```mermaid
flowchart TD
    R["[0..7] Sum: 36"]
    R --> L1["[0..3] Sum: 16"]
    R --> R1["[4..7] Sum: 20"]

    L1 --> L2A["[0..1] Sum: 7"]
    L1 --> L2B["[2..3] Sum: 9"]
    R1 --> R2A["[4..5] Sum: 9"]
    R1 --> R2B["[6..7] Sum: 11"]

    L2A --> L3A["[0]: 3"]
    L2A --> L3B["[1]: 4"]
    L2B --> L3C["[2]: 2"]
    L2B --> L3D["[3]: 7"]
    R2A --> R3A["[4]: 1"]
    R2A --> R3B["[5]: 8"]
    R2B --> R3C["[6]: 5"]
    R2B --> R3D["[7]: 6"]
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_15"): """## Skip List Multi-Level Index Towers

```mermaid
flowchart LR
    subgraph L3["Level 3 (Express Lane - P=1/8)"]
        H3["Head"] --> N3_1["Node 1"] --> N3_7["Node 7"] --> NIL3["NIL"]
    end

    subgraph L2["Level 2 (Fast Lane - P=1/4)"]
        H2["Head"] --> N2_1["Node 1"] --> N2_3["Node 3"] --> N2_7["Node 7"] --> NIL2["NIL"]
    end

    subgraph L1["Level 1 (Intermediate - P=1/2)"]
        H1["Head"] --> N1_1["Node 1"] --> N1_3["Node 3"] --> N1_5["Node 5"] --> N1_7["Node 7"] --> NIL1["NIL"]
    end

    subgraph L0["Level 0 (Base Linked List - All Elements)"]
        H0["Head"] --> N0_1["1"] --> N0_2["2"] --> N0_3["3"] --> N0_4["4"] --> N0_5["5"] --> N0_6["6"] --> N0_7["7"] --> NIL0["NIL"]
    end
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_16"): """## KMP String Matching Failure Automaton (Prefix Table Pi)

```mermaid
stateDiagram-v2
    direction LR
    [*] --> S0: Match 'A'
    S0 --> S1: Match 'B'
    S1 --> S2: Match 'A'
    S2 --> S3: Match 'B'
    S3 --> S4: Match 'C'
    S4 --> [*]: Pattern Found!

    S1 --> S0: Mismatch -> Fallback pi[1]=0
    S2 --> S0: Mismatch -> Fallback pi[2]=1
    S3 --> S1: Mismatch -> Fallback pi[3]=2
```
""",

    ("02_Data_Structures_and_Algorithms", "Module_17"): """## Dinic Network Flow: Level Graph & Augmenting Path

```mermaid
flowchart LR
    S(("Source S<br/>[Layer 0]")) -->|cap: 10, flow: 10| U(("Node U<br/>[Layer 1]"))
    S -->|cap: 10, flow: 4| V(("Node V<br/>[Layer 1]"))
    U -->|cap: 4, flow: 4| W(("Node W<br/>[Layer 2]"))
    U -->|cap: 8, flow: 6| X(("Node X<br/>[Layer 2]"))
    V -->|cap: 9, flow: 4| X
    W -->|cap: 10, flow: 4| T(("Sink T<br/>[Layer 3]"))
    X -->|cap: 10, flow: 10| T

    subgraph Invariant["Dinic Layered Invariant"]
        I["1. BFS builds Level Graph where level[v] = level[u] + 1<br/>2. DFS pushes blocking flow only along forward edges<br/>3. Repeat until Sink is unreachable in BFS"]
    end
```
""",

    # -------------------------------------------------------------------------
    # COURSE 06: DEEP LEARNING & AI FOUNDATIONS (All 12 Modules)
    # -------------------------------------------------------------------------
    ("06_Deep_Learning_and_AI_Foundations", "Module_01"): """## Vector Subspace Orthogonality & Gradient Direction

```mermaid
flowchart TD
    Loss["Scalar Loss Function L(w)"] --> Grad["Gradient Vector ∇L(w) = [∂L/∂w₁, ∂L/∂w₂, ..., ∂L/∂wₙ]"]
    Grad --> Direction["Steepest Ascent Direction"]
    Direction --> Step["Weight Update: w_{t+1} = w_t - η ∇L(w_t)"]
    Step --> Minima["Local/Global Loss Minimization"]
```
""",

    ("06_Deep_Learning_and_AI_Foundations", "Module_02"): """## Multi-Layer Perceptron Forward & Backward Propagation

```mermaid
flowchart LR
    subgraph Forward["Forward Inference Path"]
        X["Input Vector x"] -->|"Linear: z1 = W1 x + b1"| Z1["Pre-activation z1"]
        Z1 -->|"Activation: a1 = ReLU(z1)"| A1["Activation a1"]
        A1 -->|"Linear: z2 = W2 a1 + b2"| Z2["Pre-activation z2"]
        Z2 -->|"Softmax: y_hat = σ(z2)"| Y["Predicted Probability y_hat"]
        Y -->|"Cross-Entropy"| L["Loss L(y, y_hat)"]
    end

    subgraph Backward["Backward Reverse-Mode Autograd Tape"]
        dL_dZ2["∂L/∂z2 = y_hat - y"] --> dL_dW2["∂L/∂W2 = (∂L/∂z2) a1^T"]
        dL_dZ2 --> dL_dA1["∂L/∂a1 = W2^T (∂L/∂z2)"]
        dL_dA1 --> dL_dZ1["∂L/∂z1 = (∂L/∂a1) ⊙ ReLU'(z1)"]
        dL_dZ1 --> dL_dW1["∂L/∂W1 = (∂L/∂z1) x^T"]
    end
```
""",

    ("06_Deep_Learning_and_AI_Foundations", "Module_03"): """## PyTorch Tensor Memory Layout: Storage vs Strides

```mermaid
flowchart TD
    subgraph Logical["Logical 2D Tensor Shape (3 x 4)"]
        R0["Row 0: [a00, a01, a02, a03]"]
        R1["Row 1: [a10, a11, a12, a13]"]
        R2["Row 2: [a20, a21, a22, a23]"]
    end

    subgraph Physical["Flat 1D Storage Buffer (StorageOffset = 0, Strides = (4, 1))"]
        S["[a00, a01, a02, a03, a10, a11, a12, a13, a20, a21, a22, a23]"]
    end

    subgraph Transposed["Transposed View (4 x 3): Zero Memory Copy! Strides = (1, 4)"]
        T["Index Formula: offset = i * stride[0] + j * stride[1]"]
    end

    Logical --> Physical --> Transposed
```
""",

    ("06_Deep_Learning_and_AI_Foundations", "Module_04"): """## Autograd Reverse-Mode Computational Graph

```mermaid
flowchart BT
    x["Leaf Tensor: x<br/>requires_grad=True"] -->|MulBackward| mul1["v1 = x * y"]
    y["Leaf Tensor: y<br/>requires_grad=True"] -->|MulBackward| mul1
    mul1 -->|SinBackward| sin1["v2 = sin(v1)"]
    sin1 -->|AddBackward| out["Loss = v2 + x"]
    x -->|AddBackward| out

    classDef leaf fill:#0284c7,stroke:#0369a1,color:#fff;
    classDef op fill:#6366f1,stroke:#4f46e5,color:#fff;
    class x,y leaf;
    class mul1,sin1,out op;
```
""",

    ("06_Deep_Learning_and_AI_Foundations", "Module_05"): """## Adaptive Optimizers: Adam Moment Correction

```mermaid
flowchart TD
    Grad["Raw Gradient g_t = ∇_θ L(θ_t)"] --> M1["1st Moment (Mean):<br/>m_t = β₁ m_{t-1} + (1 - β₁) g_t"]
    Grad --> M2["2nd Moment (Variance):<br/>v_t = β₂ v_{t-1} + (1 - β₂) g_t²"]

    M1 --> Corr1["Bias Correction:<br/>m_hat = m_t / (1 - β₁^t)"]
    M2 --> Corr2["Bias Correction:<br/>v_hat = v_t / (1 - β₂^t)"]

    Corr1 --> Update["Weight Step:<br/>θ_{t+1} = θ_t - η · m_hat / (sqrt(v_hat) + ε)"]
    Corr2 --> Update
```
""",

    ("06_Deep_Learning_and_AI_Foundations", "Module_06"): """## 2D Convolution Receptive Field & Feature Map Pipeline

```mermaid
flowchart LR
    Input["Input Image<br/>(C_in x H x W)"] -->|"Kernel W (C_out x C_in x K_h x K_w) + Stride + Padding"| Conv["Convolved Activations<br/>(C_out x H_out x W_out)"]
    Conv --> BN["BatchNorm2d"]
    BN --> Act["ReLU / SiLU"]
    Act --> Pool["MaxPool2d / Strided Conv"]
    Pool --> Next["Next Hierarchical Stage"]
```
""",

    ("06_Deep_Learning_and_AI_Foundations", "Module_07"): """## LSTM Recurrent Cell State Gating

```mermaid
flowchart LR
    X_t["Input x_t"] --> Forget["Forget Gate: f_t = σ(W_f [h_{t-1}, x_t] + b_f)"]
    X_t --> Input["Input Gate: i_t = σ(W_i [h_{t-1}, x_t] + b_i)"]
    X_t --> Cand["Candidate: C~_t = tanh(W_c [h_{t-1}, x_t] + b_c)"]
    X_t --> Output["Output Gate: o_t = σ(W_o [h_{t-1}, x_t] + b_o)"]

    Forget --> Cell["Cell State: C_t = f_t ⊙ C_{t-1} + i_t ⊙ C~_t"]
    Input --> Cell
    Cand --> Cell

    Cell --> Hidden["Hidden State: h_t = o_t ⊙ tanh(C_t)"]
    Output --> Hidden
```
""",

    ("06_Deep_Learning_and_AI_Foundations", "Module_08"): """## Scaled Dot-Product Attention Pipeline

```mermaid
flowchart TD
    Q["Query Matrix Q<br/>(B, H, S_q, D)"] --> MatMul1["Batch MatMul: Q × K^T"]
    K["Key Matrix K<br/>(B, H, S_k, D)"] --> MatMul1
    MatMul1 --> Scale["Scale by 1 / sqrt(D)"]
    Scale --> Mask["Apply Causal Mask (Lower Triangular)"]
    Mask --> Softmax["Softmax along last dimension"]
    Softmax --> AttnWeights["Attention Probabilities P<br/>(B, H, S_q, S_k)"]
    AttnWeights --> MatMul2["Batch MatMul: P × V"]
    V["Value Matrix V<br/>(B, H, S_k, D)"] --> MatMul2
    MatMul2 --> Out["Context Output O<br/>(B, H, S_q, D)"]
```
""",

    ("06_Deep_Learning_and_AI_Foundations", "Module_09"): """## Modern Pre-LN Transformer Decoder Block

```mermaid
flowchart TD
    X["Input Tokens X"] --> LN1["RMSNorm / LayerNorm"]
    X --> Add1["Residual Add ⊕"]
    LN1 --> MHA["Multi-Head Attention / RoPE"]
    MHA --> Add1

    Add1 --> LN2["RMSNorm / LayerNorm"]
    Add1 --> Add2["Residual Add ⊕"]
    LN2 --> MLP["SwiGLU / MLP Feed-Forward (d_model -> 4*d_model -> d_model)"]
    MLP --> Add2
    Add2 --> Out["Block Output X_out"]
```
""",

    ("06_Deep_Learning_and_AI_Foundations", "Module_10"): """## Rotary Position Embedding (RoPE) 2D Subspace Rotation

```mermaid
flowchart LR
    subgraph Vector["Embedding Vector x (Dimension d)"]
        P1["Pair (x_0, x_1)"]
        P2["Pair (x_2, x_3)"]
        PK["Pair (x_{d-2}, x_{d-1})"]
    end

    subgraph Rotation["Orthogonal 2D Givens Rotations (Token Index m)"]
        R1["Rotate by m * θ₀"]
        R2["Rotate by m * θ₁"]
        RK["Rotate by m * θ_{d/2-1}"]
    end

    P1 --> R1
    P2 --> R2
    PK --> RK

    subgraph Prop["Inner Product Property"]
        IP["<R_m x, R_n y> = <x, R_{n-m} y> -> Pure Relative Distance!"]
    end
```
""",

    ("06_Deep_Learning_and_AI_Foundations", "Module_11"): """## Normalization Dimension Comparison

```mermaid
flowchart TD
    subgraph BN["Batch Norm (BN)"]
        BNDesc["Normalizes across Batch dimension (N)<br/>Preserves Channels & Spatial tokens independently"]
    end

    subgraph LN["Layer Norm (LN)"]
        LNDesc["Normalizes across Channels & Spatial dimensions (C, L)<br/>Independent per batch element"]
    end

    subgraph RMS["RMSNorm (Modern LLMs)"]
        RMSDesc["No mean centering: scale = x / sqrt(mean(x²) + ε)<br/>Saves 30% reduction overhead vs LayerNorm"]
    end
```
""",

    ("06_Deep_Learning_and_AI_Foundations", "Module_12"): """## Chinchilla Compute-Optimal Scaling Frontier

```mermaid
flowchart TD
    Compute["Fixed FLOP Compute Budget C ≈ 6 N D"]
    Compute --> Opt["Compute-Optimal Allocation (Hoffmann et al.)"]
    Opt --> N["Scale Parameters N ∝ C^0.5"]
    Opt --> D["Scale Training Tokens D ∝ C^0.5"]
    Opt --> Ratio["Golden Ratio: ~20 Tokens per Model Parameter"]

    subgraph PreChinchilla["Legacy Oversized Models (Under-trained)"]
        GPT3["GPT-3: 175B parameters on 300B tokens (1.7 tokens/param - sub-optimal)"]
    end

    subgraph Modern["Modern Compute-Optimal Models"]
        LLaMA["LLaMA 3: 8B parameters on 15T tokens (Over-trained for serving inference efficiency)"]
    end
```
""",

    # -------------------------------------------------------------------------
    # COURSE 07: GPU PROGRAMMING & AI KERNELS (All 11 Modules)
    # -------------------------------------------------------------------------
    ("07_GPU_Programming_and_AI_Kernels", "Module_01"): """## GPU Hardware Execution Hierarchy

```mermaid
flowchart TD
    subgraph Device["NVIDIA GPU (e.g. H100 SXM5)"]
        HBM["High-Bandwidth Memory (HBM3, 3.35 TB/s, 80 GB)"]
        L2["Shared L2 Cache (50 MB)"]
        
        subgraph SM1["Streaming Multiprocessor 0 (SM)"]
            WarpSched1["4x Warp Schedulers"]
            RegFile1["64K x 32-bit Register File"]
            SRAM1["228 KB Shared Memory / L1 Data Cache"]
            TensorCores1["4x 4th-Gen Tensor Cores"]
            CUDACores1["128x FP32 CUDA Cores"]
        end

        subgraph SM2["Streaming Multiprocessor 131 (SM)"]
            WarpSched2["4x Warp Schedulers"]
            RegFile2["Register File"]
            SRAM2["Shared Memory / L1"]
            TensorCores2["Tensor Cores"]
        end
    end

    HBM <--> L2
    L2 <--> SM1
    L2 <--> SM2
```
""",

    ("07_GPU_Programming_and_AI_Kernels", "Module_02"): """## CUDA Host-to-Device Asynchronous Execution Pipeline

```mermaid
sequenceDiagram
    autonumber
    participant Host as CPU Host (Thread 0)
    participant Stream as CUDA Stream 1 (PCIe/SM)
    participant DevMem as GPU Global Memory (HBM)
    participant SM as GPU SM Execution Core

    Host->>Stream: cudaMemcpyAsync(d_A, h_A, H2D)
    Stream->>DevMem: DMA Transfer via PCIe Gen5 (64 GB/s)
    Host->>Stream: kernel<<<grid, block, 0, stream>>>(d_A, d_B, d_C)
    Note over Host: Host CPU continues execution asynchronously!
    Stream->>SM: Dispatch Thread Blocks to SM Warp Schedulers
    SM->>DevMem: Read d_A, d_B, Write d_C
    Host->>Stream: cudaMemcpyAsync(h_C, d_C, D2H)
    Stream->>Host: DMA Transfer result to Host Pinned Memory
    Host->>Stream: cudaStreamSynchronize(stream)
```
""",

    ("07_GPU_Programming_and_AI_Kernels", "Module_03"): """## Global Memory Coalescing vs Strided Serialization

```mermaid
flowchart TD
    subgraph Coalesced["Coalesced Access (Consecutive Threads -> Consecutive Addresses)"]
        T0["Thread 0 -> Addr 0"]
        T1["Thread 1 -> Addr 4"]
        T2["Thread 2 -> Addr 8"]
        T31["Thread 31 -> Addr 124"]
        CoalescedBurst["Single 128-Byte Memory Transaction (100% Bus Utilization!)"]
        T0 --- T1 --- T2 --- T31 --> CoalescedBurst
    end

    subgraph Uncoalesced["Strided Access (Stride = 32 Words)"]
        U0["Thread 0 -> Addr 0"]
        U1["Thread 1 -> Addr 128"]
        U2["Thread 2 -> Addr 256"]
        U31["Thread 31 -> Addr 3968"]
        UncoalescedBursts["32 Separate 32-Byte Transactions (96.8% Bandwidth Wasted!)"]
        U0 --- U1 --- U2 --- U31 --> UncoalescedBursts
    end
```
""",

    ("07_GPU_Programming_and_AI_Kernels", "Module_04"): """## Shared Memory 32-Bank Conflict Mechanics

```mermaid
flowchart LR
    subgraph ConflictFree["Conflict-Free Stride-1 Access"]
        Th0["Thread 0"] --> B0["Bank 0"]
        Th1["Thread 1"] --> B1["Bank 1"]
        Th2["Thread 2"] --> B2["Bank 2"]
        Th31["Thread 31"] --> B31["Bank 31"]
        CF_Note["1 Cycle: All 32 words serviced simultaneously!"]
    end

    subgraph TwoWay["2-Way Bank Conflict (Stride = 2 or 32)"]
        C0["Thread 0"] --> Bank0["Bank 0 (Port 0)"]
        C16["Thread 16"] -.->|Serialized Wait!| Bank0
        Conflict_Note["2 Serial Cycles: Thread 16 stalled behind Thread 0!"]
    end
```
""",

    ("07_GPU_Programming_and_AI_Kernels", "Module_05"): """## Warp Shuffle Butterfly Reduction Topology

```mermaid
flowchart TD
    subgraph S1["Step 1: __shfl_xor_sync(mask, val, 16)"]
        T0_16["Threads [0..15] combine with Threads [16..31]"]
    end
    subgraph S2["Step 2: __shfl_xor_sync(mask, val, 8)"]
        T0_8["Threads [0..7] combine with Threads [8..15]"]
    end
    subgraph S3["Step 3: __shfl_xor_sync(mask, val, 4)"]
        T0_4["Threads [0..3] combine with Threads [4..7]"]
    end
    subgraph S4["Step 4: __shfl_xor_sync(mask, val, 2)"]
        T0_2["Threads [0..1] combine with Threads [2..3]"]
    end
    subgraph S5["Step 5: __shfl_xor_sync(mask, val, 1)"]
        T0_final["Thread 0 holds Full Warp Sum in exactly 5 clock cycles!"]
    end

    S1 --> S2 --> S3 --> S4 --> S5
```
""",

    ("07_GPU_Programming_and_AI_Kernels", "Module_06"): """## Shared Memory Matrix Tiling Workflow

```mermaid
flowchart TD
    subgraph GlobalMem["Global Memory (DRAM / HBM)"]
        MatA["Matrix A (M x K)"]
        MatB["Matrix B (K x N)"]
    end

    subgraph SharedMem["Shared Memory Tile Buffers (SRAM, 15 TB/s)"]
        TileA["Tile As[BM][BK] (e.g. 128 x 16)"]
        TileB["Tile Bs[BK][BN] (e.g. 16 x 128)"]
    end

    subgraph Regs["Warp Register File (RF, 30+ TB/s)"]
        Compute["Accumulate Partial Dot Products in Registers (C_sub)"]
    end

    MatA -->|Collaborative Load 128-bit LDG.128| TileA
    MatB -->|Collaborative Load 128-bit LDG.128| TileB
    TileA -->|LDS to Registers| Compute
    TileB -->|LDS to Registers| Compute
```
""",

    ("07_GPU_Programming_and_AI_Kernels", "Module_07"): """## Tensor Core MMA Matrix Multiply Instruction

```mermaid
flowchart LR
    subgraph Inputs["Warp Input Fragments"]
        FragA["Fragment A<br/>16 x 16 (FP16 / BF16)"]
        FragB["Fragment B<br/>16 x 16 (FP16 / BF16)"]
        FragC["Accumulator C<br/>16 x 16 (FP32)"]
    end

    subgraph TensorCore["4th-Gen Tensor Core Unit"]
        MMA["D = A × B + C in Single Instruction Cycle"]
    end

    subgraph Output["Result Fragment"]
        FragD["Fragment D<br/>16 x 16 (FP32 / FP16)"]
    end

    FragA --> MMA
    FragB --> MMA
    FragC --> MMA
    MMA --> FragD
```
""",

    ("07_GPU_Programming_and_AI_Kernels", "Module_08"): """## FlashAttention Tiling & Online Softmax Algorithm

```mermaid
flowchart TD
    subgraph HBM["High-Bandwidth Memory (HBM)"]
        Q_hbm["Query Q"]
        K_hbm["Key K"]
        V_hbm["Value V"]
        O_hbm["Output O"]
    end

    subgraph SRAM["Fast SRAM / Shared Memory (SM)"]
        Q_tile["Q Block Tile (Br x d)"]
        K_tile["K Block Tile (Bc x d)"]
        V_tile["V Block Tile (Bc x d)"]
        S_tile["Attention Logits: S = Q_tile × K_tile^T"]
        OnlineSoftmax["Online Softmax Rescaling:<br/>m_new = max(m_prev, rowmax(S))<br/>P_tile = exp(S - m_new)<br/>l_new = exp(m_prev - m_new) * l_prev + rowsum(P_tile)"]
        O_accum["O = (exp(m_prev - m_new) * O_prev + P_tile × V_tile) / l_new"]
    end

    Q_hbm --> Q_tile
    K_hbm --> K_tile
    V_hbm --> V_tile
    Q_tile --> S_tile
    K_tile --> S_tile
    S_tile --> OnlineSoftmax --> O_accum
    O_accum --> O_hbm
```
""",

    ("07_GPU_Programming_and_AI_Kernels", "Module_09"): """## Triton Compiler Pipeline: Python AST to PTX

```mermaid
flowchart LR
    Python["@triton.jit Python Kernel<br/>(Block-Level Tensors)"] --> AST["Triton AST"]
    AST --> TTIR["Triton-IR (TTIR)<br/>Block Dialect"]
    TTIR --> TTGIR["TritonGPU-IR (TTGIR)<br/>Warp & Layout Layout Dialect"]
    TTGIR --> LLVM["LLVM-IR Code Generation"]
    LLVM --> PTX["NVIDIA PTX Assembly"]
    PTX --> Cubin["SASS Machine Binary (cubin)"]
```
""",

    ("07_GPU_Programming_and_AI_Kernels", "Module_10"): """## Kernel Fusion: Eliminating Intermediate DRAM Roundtrips

```mermaid
flowchart TD
    subgraph Unfused["Unfused PyTorch Pipeline (3 HBM Roundtrips)"]
        Act["Activation X"] -->|Write HBM| K1["Kernel 1: BiasAdd"]
        K1 -->|Read HBM / Write HBM| K2["Kernel 2: GeLU"]
        K2 -->|Read HBM / Write HBM| K3["Kernel 3: LayerNorm"]
        K3 -->|Write HBM| Out1["Final Output"]
    end

    subgraph Fused["Fused Kernel (1 Single HBM Load & Store)"]
        FAct["Activation X"] -->|Single HBM Read| FusedOp["FusedBiasAddGeLULayerNorm<<<...>>><br/>(Passes values through GPU Registers & SRAM)"]
        FusedOp -->|Single HBM Write| FOut["Final Output (3-4x Speedup!)"]
    end
```
""",

    ("07_GPU_Programming_and_AI_Kernels", "Module_11"): """## GPU Roofline Model: Memory-Bound vs Compute-Bound Regimes

```mermaid
flowchart TD
    subgraph Roofline["Roofline Model Graph"]
        MemCeiling["Diagonal Bandwidth Ceiling: Performance = Intensity × Bandwidth (TB/s)"]
        PeakCompute["Horizontal Compute Ceiling: Peak Tensor Core FLOP/s (e.g. 989 TFLOPs FP16)"]
        Knee["Inflection Ridge Point: Intensity_crit = Peak_FLOPs / Peak_Bandwidth"]
    end

    subgraph Regimes["Kernel Operational Classification"]
        MemBound["Low Intensity (< 150 FLOPs/byte):<br/>LayerNorm, Softmax, Elementwise Add<br/>Optimization: Kernel Fusion, SRAM Tiling"]
        CompBound["High Intensity (> 150 FLOPs/byte):<br/>Large Batch GEMM, Conv2d<br/>Optimization: Tensor Cores, WMMA, ILP"]
    end

    Roofline --> Regimes
```
""",

    # -------------------------------------------------------------------------
    # COURSE 08: DISTRIBUTED TRAINING & GPU INFRASTRUCTURE (All 10 Modules)
    # -------------------------------------------------------------------------
    ("08_Distributed_Training_and_GPU_Infrastructure", "Module_01"): """## GPU Cluster Interconnect Topology (NVLink vs InfiniBand)

```mermaid
flowchart TD
    subgraph Node1["DGX H100 Server Node 1"]
        GPU1_0["GPU 0"] <-->|NVLink 900 GB/s| NVSwitch1["NVSwitch Fabric"]
        GPU1_1["GPU 1"] <-->|NVLink 900 GB/s| NVSwitch1
        NIC1["ConnectX-7 NIC<br/>(400 Gb/s RoCE/IB)"]
    end

    subgraph Node2["DGX H100 Server Node 2"]
        GPU2_0["GPU 0"] <-->|NVLink 900 GB/s| NVSwitch2["NVSwitch Fabric"]
        GPU2_1["GPU 1"] <-->|NVLink 900 GB/s| NVSwitch2
        NIC2["ConnectX-7 NIC<br/>(400 Gb/s RoCE/IB)"]
    end

    subgraph Spine["InfiniBand Quantum-2 Leaf-Spine Switch Fabric (3.2 Tb/s)"]
        Leaf1["Leaf Switch 1"]
        Leaf2["Leaf Switch 2"]
    end

    NIC1 <--> Leaf1
    NIC2 <--> Leaf2
    Leaf1 <--> Leaf2
```
""",

    ("08_Distributed_Training_and_GPU_Infrastructure", "Module_02"): """## NCCL Ring AllReduce Step Progression

```mermaid
sequenceDiagram
    autonumber
    participant G0 as GPU 0
    participant G1 as GPU 1
    participant G2 as GPU 2
    participant G3 as GPU 3

    Note over G0,G3: Phase 1: Scatter-Reduce (N-1 = 3 ring steps)
    G0->>G1: Send Chunk 0, Reduce locally
    G1->>G2: Send Chunk 1, Reduce locally
    G2->>G3: Send Chunk 2, Reduce locally
    G3->>G0: Send Chunk 3, Reduce locally
    Note over G0,G3: Each GPU now possesses exactly 1 fully reduced chunk!

    Note over G0,G3: Phase 2: AllGather (N-1 = 3 ring steps)
    G0->>G1: Send fully reduced Chunk 3
    G1->>G2: Send fully reduced Chunk 0
    G2->>G3: Send fully reduced Chunk 1
    G3->>G0: Send fully reduced Chunk 2
    Note over G0,G3: All GPUs now possess complete updated gradient buffer!
```
""",

    ("08_Distributed_Training_and_GPU_Infrastructure", "Module_03"): """## PyTorch DDP Computation & Communication Overlap

```mermaid
sequenceDiagram
    autonumber
    participant Fwd as Forward Pass
    participant Bwd as Backward Pass (Grads)
    participant Bucket as DDP Bucket (25MB)
    participant NCCL as NCCL AllReduce Stream

    Fwd->>Bwd: Layer N Loss Computed
    Bwd->>Bucket: Layer N Gradients Computed -> Placed in Bucket
    Bwd->>Bucket: Layer N-1 Gradients Computed -> Bucket Full!
    Bucket->>NCCL: Trigger Async AllReduce Bucket 1
    Note over Bwd,NCCL: NCCL AllReduces Bucket 1 WHILE Backward computes Layer N-2!
    Bwd->>Bucket: Layer N-2 Gradients Computed -> Bucket 2
    NCCL-->>Bwd: Bucket 1 AllReduce Complete!
```
""",

    ("08_Distributed_Training_and_GPU_Infrastructure", "Module_04"): """## ZeRO Memory Partitioning Hierarchy (Deepspeed)

```mermaid
flowchart TD
    subgraph Baseline["Baseline DDP (Redundant Storage on All GPUs)"]
        BaseP["Parameters Ψ (4x bytes)"]
        BaseG["Gradients Ψ (4x bytes)"]
        BaseO["Optimizer States (12x bytes: FP32 Master + Mom + Var)"]
        BaseTotal["Total Static: 16x Model Size per GPU!"]
    end

    subgraph ZeRO1["ZeRO-1: Optimizer State Partitioning (P_os)"]
        Z1["Partition 12x bytes across N GPUs -> 4x Memory Reduction!"]
    end

    subgraph ZeRO2["ZeRO-2: + Gradient Partitioning (P_g)"]
        Z2["Partition Gradients + Optimizer States -> 8x Memory Reduction!"]
    end

    subgraph ZeRO3["ZeRO-3: + Parameter Partitioning (P_p)"]
        Z3["Partition Parameters, Gradients, and Optimizer States across N GPUs -> Linear Memory Scaling with Zero Redundancy!"]
    end

    Baseline --> ZeRO1 --> ZeRO2 --> ZeRO3
```
""",

    ("08_Distributed_Training_and_GPU_Infrastructure", "Module_05"): """## FSDP (Fully Sharded Data Parallel) Execution Cycle

```mermaid
flowchart TD
    subgraph Forward["Forward Pass"]
        F1["AllGather Sharded Params for Layer i"] --> F2["Compute Forward Activations"]
        F2 --> F3["Discard Unsharded Params (Keep only local shard)"]
    end

    subgraph Backward["Backward Pass"]
        B1["AllGather Sharded Params for Layer i"] --> B2["Compute Backward Gradients"]
        B2 --> B3["ReduceScatter Gradients across Ranks"]
        B3 --> B4["Discard Unsharded Params & Accumulate Local Grad Shard"]
    end

    Forward --> Backward
```
""",

    ("08_Distributed_Training_and_GPU_Infrastructure", "Module_06"): """## Megatron-LM Tensor Parallelism (MLP Block)

```mermaid
flowchart TD
    X["Input Activations X"] --> Split["Broadcast to TP GPUs"]
    
    subgraph ColParallel["Column Parallel Linear (W1)"]
        W1_0["W1_0 (Rank 0)"]
        W1_1["W1_1 (Rank 1)"]
    end

    subgraph RowParallel["Row Parallel Linear (W2)"]
        W2_0["W2_0 (Rank 0)"]
        W2_1["W2_1 (Rank 1)"]
    end

    Split --> W1_0 --> W2_0
    Split --> W1_1 --> W2_1

    W2_0 --> AllReduce["AllReduce Sum: Y = W2_0(W1_0(X)) + W2_1(W1_1(X))"]
    W2_1 --> AllReduce
    AllReduce --> Out["Output Y"]
```
""",

    ("08_Distributed_Training_and_GPU_Infrastructure", "Module_07"): """## Pipeline Parallelism 1F1B Scheduling Schedule

```mermaid
gantt
    title Pipeline 1F1B Execution Timeline (4 Stages)
    dateFormat X
    axisFormat %s

    section Stage 0
    F0 :active, 0, 1
    F1 :active, 1, 2
    F2 :active, 2, 3
    F3 :active, 3, 4
    B0 :crit, 4, 5
    F4 :active, 5, 6
    B1 :crit, 6, 7

    section Stage 1
    Idle :crit, 0, 1
    F0 :active, 1, 2
    F1 :active, 2, 3
    F2 :active, 3, 4
    F3 :active, 4, 5
    B0 :crit, 5, 6
    F4 :active, 6, 7

    section Stage 2
    Idle :crit, 0, 2
    F0 :active, 2, 3
    F1 :active, 3, 4
    F2 :active, 4, 5
    B0 :crit, 6, 7

    section Stage 3
    Idle :crit, 0, 3
    F0 :active, 3, 4
    F1 :active, 4, 5
    B0 :crit, 5, 6
    B1 :crit, 6, 7
```
""",

    ("08_Distributed_Training_and_GPU_Infrastructure", "Module_08"): """## 3D Parallelism Architectural Orthogonality

```mermaid
flowchart TD
    subgraph Cube["3D Parallelism Grid (e.g. 64 GPUs)"]
        TP["Tensor Parallelism (TP = 8)<br/>Intra-Node NVLink"]
        PP["Pipeline Parallelism (PP = 4)<br/>Inter-Node InfiniBand Layers"]
        DP["Data Parallelism (DP = 2)<br/>Cross-Cluster Replicas"]
    end

    subgraph Total["Total World Size = TP × PP × DP = 8 × 4 × 2 = 64 GPUs"]
        Desc["Enables training 100B+ parameter models across hundreds of nodes"]
    end

    Cube --> Total
```
""",

    ("08_Distributed_Training_and_GPU_Infrastructure", "Module_09"): """## Activation Checkpointing Memory Savings

```mermaid
flowchart LR
    subgraph Standard["Standard Training (Stores all intermediate activations)"]
        F1["Forward Layer 1"] -->|Store a1| F2["Forward Layer 2"] -->|Store a2| F3["Forward Layer 3"]
        F3 -->|Compute Grad| B3["Backward Layer 3"] --> B2["Backward Layer 2"] --> B1["Backward Layer 1"]
        MemStd["Memory: O(N_layers) activations retained in VRAM"]
    end

    subgraph Checkpointed["Activation Checkpointing (Recompute on demand)"]
        CF1["Forward Layer 1"] -->|Discard a1| CF2["Forward Layer 2"] -->|Discard a2| CF3["Forward Layer 3"]
        CF3 -->|Recompute Layer 2| CB2["Backward Layer 2"] -->|Recompute Layer 1| CB1["Backward Layer 1"]
        MemChk["Memory: O(sqrt(N_layers)) VRAM footprint -> 70% Memory Saved!"]
    end
```
""",

    ("08_Distributed_Training_and_GPU_Infrastructure", "Module_10"): """## Resilient Distributed Fault Tolerance Architecture

```mermaid
flowchart TD
    Health["Node Heartbeat Monitor (etcd / Slurm)"] --> Detect["Worker Node 3 Failure Detected!"]
    Detect --> Evict["Evict Faulty Node from Hostfile"]
    Evict --> Checkpoint["Load Last Valid Distributed Checkpoint (S3 / Ceph)"]
    Checkpoint --> Reroute["Reconfigure NCCL Ring Topology & World Size"]
    Reroute --> Resume["Resume Training without Job Termination"]
```
""",

    # -------------------------------------------------------------------------
    # COURSE 09: INFERENCE SYSTEMS & SERVING ENGINES (All 9 Modules)
    # -------------------------------------------------------------------------
    ("09_Inference_Systems_and_Serving_Engines", "Module_01"): """## LLM Inference Latency Breakdown (Prefill vs Decode)

```mermaid
flowchart LR
    subgraph TTFT["Time To First Token (Prefill Phase)"]
        Prompt["Input Prompt: 2048 Tokens"] --> GEMM["Parallel Matrix Multiply (GEMM)"]
        GEMM --> HighCompute["Compute-Bound (High Arithmetic Intensity)<br/>Tensor Cores 100% Saturated"]
    end

    subgraph TPOT["Time Per Output Token (Decode Phase)"]
        TokenGen["Autoregressive Generation (1 Token at a time)"] --> GEMV["Matrix-Vector Multiply (GEMV)"]
        GEMV --> LowCompute["Memory-Bound (Low Arithmetic Intensity)<br/>Bottlenecked by HBM Memory Bandwidth!"]
    end

    TTFT --> TPOT
```
""",

    ("09_Inference_Systems_and_Serving_Engines", "Module_02"): """## Traditional Contiguous KV Cache Memory Fragmentation

```mermaid
flowchart TD
    subgraph Prealloc["Static Pre-Allocation for Max Sequence Length (e.g. 4096)"]
        Req1["Request 1: Length 120 -> 3976 Slots Wasted!"]
        Req2["Request 2: Length 500 -> 3596 Slots Wasted!"]
        Req3["Request 3: Length 80 -> 4016 Slots Wasted!"]
    end

    subgraph Problem["GPU Memory Waste"]
        Waste["Over 60-80% of GPU VRAM wasted due to internal and external fragmentation!"]
    end

    Prealloc --> Problem
```
""",

    ("09_Inference_Systems_and_Serving_Engines", "Module_03"): """## PagedAttention Virtual Memory Block Table (vLLM)

```mermaid
flowchart LR
    subgraph Logical["Logical KV Cache (Contiguous per Request)"]
        L0["Block 0 (Tokens 0-15)"]
        L1["Block 1 (Tokens 16-31)"]
        L2["Block 2 (Tokens 32-47)"]
    end

    subgraph Table["Block Table (Page Table)"]
        BT0["Logical 0 -> Physical 7"]
        BT1["Logical 1 -> Physical 3"]
        BT2["Logical 2 -> Physical 12"]
    end

    subgraph Physical["Physical GPU DRAM Pages (Non-Contiguous)"]
        P3["Physical Block 3"]
        P7["Physical Block 7"]
        P12["Physical Block 12"]
    end

    L0 --> BT0 --> P7
    L1 --> BT1 --> P3
    L2 --> BT2 --> P12
```
""",

    ("09_Inference_Systems_and_Serving_Engines", "Module_04"): """## Continuous (Iteration-Level) Batching vs Static Batching

```mermaid
gantt
    title Serving Batch Scheduling: Continuous vs Static
    dateFormat X
    axisFormat %s

    section Static Batching (Bubbles)
    Req A (Tokens 1-4) :crit, 0, 4
    Req B (Tokens 1-2) :active, 0, 2
    Req B Wasted Idle :done, 2, 4
    Req C (Blocked Waiting) :crit, 4, 8

    section Continuous Batching (Orca)
    Req A (Tokens 1-4) :active, 0, 4
    Req B (Tokens 1-2) :active, 0, 2
    Req C (Inserts at Step 2) :crit, 2, 6
    Req D (Inserts at Step 4) :crit, 4, 7
```
""",

    ("09_Inference_Systems_and_Serving_Engines", "Module_05"): """## Speculative Decoding Verification Pipeline

```mermaid
sequenceDiagram
    autonumber
    participant Draft as Draft Small Model (e.g. 1B)
    participant Target as Target LLM (e.g. 70B)
    participant Verifier as Acceptance Logic

    Draft->>Draft: Generate K=4 Candidate Tokens sequentially
    Draft->>Target: Pass Prompt + [t1, t2, t3, t4]
    Target->>Target: Single Forward Pass evaluates all 4 positions in parallel!
    Target->>Verifier: Return Target Probabilities p(t)
    Verifier->>Verifier: Accept t1 (p_target >= p_draft)
    Verifier->>Verifier: Accept t2 (p_target >= p_draft)
    Verifier->>Verifier: Reject t3! Sample corrective token t3'
    Verifier->>Draft: 3 Tokens generated in 1 Target Forward Pass (2.5x Speedup!)
```
""",

    ("09_Inference_Systems_and_Serving_Engines", "Module_06"): """## Chunked Prefill & Decode Co-Scheduling

```mermaid
flowchart TD
    subgraph RequestPool["Incoming Requests"]
        LongPrefill["Long Context Prefill: 8192 Tokens"]
        ActiveDecodes["16 Active Decode Requests"]
    end

    subgraph Chunking["Chunked Prefill Strategy"]
        Chunk["Split 8192 Tokens into 512-Token Chunks"]
    end

    subgraph Batch["Balanced Iteration Batch"]
        Iter["512 Prefill Tokens + 16 Decode Tokens = 528 Tokens<br/>Completely eliminates decode latency spikes!"]
    end

    RequestPool --> Chunking --> Batch
```
""",

    ("09_Inference_Systems_and_Serving_Engines", "Module_07"): """## LLM Weight & Activation Quantization Formats

```mermaid
flowchart LR
    FP16["FP16 / BF16<br/>(16 bits, Baseline)"] --> FP8["FP8 (E4M3 / E5M2)<br/>(8 bits, 2x Memory & Speed)"]
    FP8 --> INT4["INT4 / AWQ / GPTQ<br/>(4 bits, 3.5x Memory Reduction)"]

    subgraph Tradeoff["Accuracy vs Performance Frontier"]
        Desc["AWQ preserves top 1% salient weight channels to maintain perplexity!"]
    end

    INT4 --> Tradeoff
```
""",

    ("09_Inference_Systems_and_Serving_Engines", "Module_08"): """## Radix Tree Prefix Cache Sharing Architecture

```mermaid
flowchart TD
    Root["Root Node (Empty)"] --> SysPrompt["System Prompt: 'You are an expert systems engineer...' (500 tokens)"]
    
    SysPrompt --> UserA["User Request A: 'Explain Raft...' (Node A)"]
    SysPrompt --> UserB["User Request B: 'Explain Paxos...' (Node B)"]

    subgraph CacheHit["Prefix Cache Hit Invariant"]
        Hit["System Prompt KV cache reused directly without recomputation!"]
    end

    SysPrompt --- CacheHit
```
""",

    ("09_Inference_Systems_and_Serving_Engines", "Module_09"): """## Distributed Multi-GPU Tensor Parallel Inference Serving

```mermaid
flowchart TD
    Prompt["Input Token ID"] --> Broadcast["Broadcast to All Serving GPUs"]
    
    subgraph GPUs["Tensor Parallel Rank Slices"]
        GPU0["GPU 0: Compute Q0, K0, V0, Attention, W1_0, W2_0"]
        GPU1["GPU 1: Compute Q1, K1, V1, Attention, W1_1, W2_1"]
    end

    Broadcast --> GPU0
    Broadcast --> GPU1

    GPU0 --> AllReduce["NCCL AllReduce Sum Output"]
    GPU1 --> AllReduce

    AllReduce --> Sample["Logits Sampling -> Next Token"]
```
""",

    # -------------------------------------------------------------------------
    # COURSE 10: ADVANCED RETRIEVAL & CONTEXT SYSTEMS (All 9 Modules)
    # -------------------------------------------------------------------------
    ("10_Advanced_Retrieval_and_Context_Engineering", "Module_01"): """## Document Parsing & Hierarchical Chunking Pipeline

```mermaid
flowchart TD
    Doc["Raw PDF / Markdown Document"] --> AST["Structure-Aware AST Parser"]
    AST --> Sections["Section & Header Hierarchy"]
    Sections --> Chunks["Semantic Chunks (500 tokens) with 50-token Overlap"]
    Chunks --> Meta["Enrich Metadata (Headers, Parent Section, Doc Title)"]
    Meta --> Embed["Embedder Model -> Vector Embeddings"]
```
""",

    ("10_Advanced_Retrieval_and_Context_Engineering", "Module_02"): """## Contextual Retrieval: Prepending Global Context

```mermaid
flowchart TD
    subgraph Problem["Isolated Chunk Context Loss"]
        RawChunk["Chunk: 'The company grew revenue by 12% in Q3.'<br/>(Which company? Which year?)"]
    end

    subgraph Solution["Contextual Retrieval (Anthropic Pattern)"]
        LLM["Prompt Claude: Generate 50-word context summary using entire document"]
        Context["Context: 'In Apple Inc 2023 10-K filing financial results section...'"]
        Enriched["Enriched Chunk = Context + Raw Chunk"]
    end

    RawChunk --> LLM --> Context --> Enriched
```
""",

    ("10_Advanced_Retrieval_and_Context_Engineering", "Module_03"): """## Vector Database Internals: IVF-PQ Compression

```mermaid
flowchart LR
    Vector["High-Dim Vector (1536-d FP32 = 6144 bytes)"] --> IVF["1. Inverted File Index (IVF): Assign to Voronoi Centroid"]
    IVF --> Subvectors["2. Split into M=16 Subvectors (96-d each)"]
    Subvectors --> PQ["3. Product Quantization (PQ): Quantize to Codebook Centroid (1 byte)"]
    PQ --> Compressed["Compressed Representation: 16 bytes (384x Space Reduction!)"]
```
""",

    ("10_Advanced_Retrieval_and_Context_Engineering", "Module_04"): """## HNSW Hierarchical Multi-Layer Skip-Graph Search

```mermaid
flowchart TD
    subgraph Layer2["Layer 2 (Express Coarse Jump)"]
        L2_Start(("Entry")) --> L2_Next(("Node B"))
    end

    subgraph Layer1["Layer 1 (Intermediate Proximity)"]
        L1_B(("Node B")) --> L1_C(("Node C")) --> L1_D(("Node D"))
    end

    subgraph Layer0["Layer 0 (Dense Nearest Neighbors)"]
        L0_D(("Node D")) --> L0_Target(("Nearest Neighbor Match!"))
    end

    Layer2 -->|Greedy Local Minimum| Layer1 -->|Greedy Local Minimum| Layer0
```
""",

    ("10_Advanced_Retrieval_and_Context_Engineering", "Module_05"): """## Hybrid Search Reciprocal Rank Fusion (RRF)

```mermaid
flowchart TD
    Query["User Query"] --> Sparse["BM25 Lexical Keyword Search"]
    Query --> Dense["Dense Semantic Vector Embeddings"]

    Sparse --> TopSparse["Sparse Top-K Ranks"]
    Dense --> TopDense["Dense Top-K Ranks"]

    TopSparse --> RRF["Reciprocal Rank Fusion Formula:<br/>RRF_score(d) = Σ 1 / (k + rank_i(d)) (k=60)"]
    TopDense --> RRF

    RRF --> Merged["Fused Ranked Results (Best of Exact Match & Conceptual Match)"]
```
""",

    ("10_Advanced_Retrieval_and_Context_Engineering", "Module_06"): """## Two-Stage Retrieval & Cross-Encoder Reranker

```mermaid
flowchart LR
    Q["User Query"] --> Fast["Stage 1: Bi-Encoder Vector Search<br/>Retrieve Top-100 in 5 ms"]
    Fast --> Candidates["100 Candidate Chunks"]
    Candidates --> Cross["Stage 2: Cross-Encoder Transformer<br/>Full Joint Attention [Query, Chunk]"]
    Cross --> Top5["High-Precision Top-5 Chunks to LLM Context"]
```
""",

    ("10_Advanced_Retrieval_and_Context_Engineering", "Module_07"): """## GraphRAG Knowledge Graph & Community Summarization

```mermaid
flowchart TD
    Text["Corpus Text Chunks"] --> Extr["LLM Information Extraction"]
    Extr --> KG["Knowledge Graph (Entities, Relations, Claims)"]
    KG --> Leiden["Leiden Community Detection Algorithm"]
    Leiden --> C1["Community 1 (Low-Level)"]
    Leiden --> C2["Community 2 (High-Level Cluster)"]
    C1 --> Sum1["Community Summary 1"]
    C2 --> Sum2["Community Summary 2"]
    Sum1 --> GlobalQA["Global Sensemaking Query Response"]
    Sum2 --> GlobalQA
```
""",

    ("10_Advanced_Retrieval_and_Context_Engineering", "Module_08"): """## ColBERT Late Interaction Token Similarity Matrix

```mermaid
flowchart TD
    Q_Tokens["Query Tokens: [q0, q1, ..., qn]"] --> Mat["Late Interaction Similarity Matrix (Cosine Sim)"]
    D_Tokens["Document Tokens: [d0, d1, ..., dm]"] --> Mat
    Mat --> MaxSim["MaxSim Operator: For each query token, take max similarity across all doc tokens"]
    MaxSim --> Sum["Sum MaxSim scores -> Final Document Relevance Score"]
```
""",

    ("10_Advanced_Retrieval_and_Context_Engineering", "Module_09"): """## Attention-Based Context Pruning & Compression

```mermaid
flowchart LR
    LongCtx["Long Retrieved Context (32K tokens)"] --> Scorer["Small LLM / Perplexity Scorer"]
    Scorer --> Mask["Filter Low-Information Spans & Duplicate Chunks"]
    Mask --> CompressedCtx["Dense Context (8K tokens, 100% Salient Information)"]
    CompressedCtx --> MainLLM["Target LLM Generation (4x Faster, Lower Token Cost)"]
```
""",

    # -------------------------------------------------------------------------
    # COURSE 11 & 12: AGENTS & EVALUATION SCIENCE (Sample Modules)
    # -------------------------------------------------------------------------
    ("11_Autonomous_Agents_and_Cognitive_Architectures", "Module_01"): """## ReAct Agent Cognitive Loop Architecture

```mermaid
sequenceDiagram
    autonumber
    participant User as User Request
    participant Agent as ReAct Core Agent
    participant LLM as Reasoning Engine
    participant Tool as External Tools / Environment

    User->>Agent: "Find GPU memory bandwidth of H100 and calculate roofline"
    Agent->>LLM: Generate Thought & Action Plan
    LLM-->>Agent: Thought: Need exact H100 memory bandwidth specs.<br/>Action: search_specs(query='H100 SXM5 memory bandwidth')
    Agent->>Tool: Execute search_specs(...)
    Tool-->>Agent: Observation: "H100 SXM5 features 3.35 TB/s HBM3 bandwidth"
    Agent->>LLM: Pass Observation & Request Next Step
    LLM-->>Agent: Thought: Now compute roofline intensity threshold.<br/>Action: python_calc(flops=989e12, bw=3.35e12)
    Agent->>Tool: Execute python_calc(...)
    Tool-->>Agent: Observation: "295.22 FLOPs/byte"
    Agent->>LLM: Synthesize Final Answer
    LLM-->>User: "H100 bandwidth is 3.35 TB/s, requiring 295 FLOPs/byte for compute ceiling."
```
""",

    ("12_LLM_Evaluation_Science_and_Guardrails", "Module_01"): """## Multi-Tiered LLM Evaluation & Guardrails Defense

```mermaid
flowchart TD
    UserPrompt["Incoming User Prompt"] --> InputGuard["Input Guardrail (Llama-Guard / Semantic Filter)"]
    InputGuard -->|Clean| Model["Target Model Generation"]
    InputGuard -->|Injection / Attack Detected| Block["403 Forbidden Block Response"]

    Model --> OutputGuard["Output Guardrail (Hallucination / PII Filter)"]
    OutputGuard -->|Safe| Response["Safe Verified Response to User"]
    OutputGuard -->|Violation| Redact["Fallback Safe Redacted Response"]

    subgraph EvalHarness["Offline Evaluation Pipeline"]
        Golden["Golden Dataset Evaluation"] --> LLMJudge["LLM-as-a-Judge Pairwise Scoring"]
        LLMJudge --> Metric["Faithfulness, Precision, Toxicity Metrics"]
    end
```
""",
}

# Concrete AlgorithmTraceScrubber Traces for Course 02
SCRUBBER_TRACES = {
    "Module_02": """## Interactive Algorithm Trace Scrubber

```trace
{
  "title": "Two Pointers Search: Two Sum II",
  "algorithm": "Two Pointers on Sorted Array",
  "timeComplexity": "O(n)",
  "spaceComplexity": "O(1)",
  "frames": [
    {
      "step": 1,
      "description": "Initialize left=0, right=5 on sorted array. Target sum is 18.",
      "array": [2, 4, 7, 11, 14, 20],
      "pointers": { "left": 0, "right": 5 },
      "highlights": { "0": "active", "5": "active" },
      "variables": { "left": 0, "right": 5, "currentSum": 22, "target": 18 },
      "invariants": "Sum 2 + 20 = 22 > 18: Decrement right pointer to reduce sum"
    },
    {
      "step": 2,
      "description": "right moves to index 4. Sum is 2 + 14 = 16 < 18.",
      "array": [2, 4, 7, 11, 14, 20],
      "pointers": { "left": 0, "right": 4 },
      "highlights": { "0": "active", "4": "active" },
      "variables": { "left": 0, "right": 4, "currentSum": 16, "target": 18 },
      "invariants": "Sum 16 < 18: Increment left pointer to increase sum"
    },
    {
      "step": 3,
      "description": "left moves to index 1. Sum is 4 + 14 = 18 === target! Match found.",
      "array": [2, 4, 7, 11, 14, 20],
      "pointers": { "left": 1, "right": 4 },
      "highlights": { "1": "sorted", "4": "sorted" },
      "variables": { "left": 1, "right": 4, "currentSum": 18, "target": 18, "found": true },
      "invariants": "Target pair matched: return indices [1, 4] (1-indexed: [2, 5])"
    }
  ]
}
```
""",

    "Module_06": """## Interactive Algorithm Trace Scrubber

```trace
{
  "title": "Binary Search Tree Key Insertion & Rebalance",
  "algorithm": "BST Search and Traversal",
  "timeComplexity": "O(log n)",
  "spaceComplexity": "O(1)",
  "frames": [
    {
      "step": 1,
      "description": "Root node comparison: Target 25 vs Root 30.",
      "array": [30, 15, 45, 10, 25, 35, 60],
      "pointers": { "curr": 0 },
      "highlights": { "0": "comparing" },
      "variables": { "currKey": 30, "target": 25, "direction": "left" },
      "invariants": "25 < 30: Traverse to left child (index 1)"
    },
    {
      "step": 2,
      "description": "Compare Target 25 with Left Child 15.",
      "array": [30, 15, 45, 10, 25, 35, 60],
      "pointers": { "curr": 1 },
      "highlights": { "1": "comparing" },
      "variables": { "currKey": 15, "target": 25, "direction": "right" },
      "invariants": "25 > 15: Traverse to right child of 15 (index 4)"
    },
    {
      "step": 3,
      "description": "Compare Target 25 with Node 25: Target Matched!",
      "array": [30, 15, 45, 10, 25, 35, 60],
      "pointers": { "curr": 4 },
      "highlights": { "4": "sorted" },
      "variables": { "currKey": 25, "target": 25, "found": true },
      "invariants": "Exact key hit at node 25 in 3 comparisons"
    }
  ]
}
```
""",

    "Module_07": """## Interactive Algorithm Trace Scrubber

```trace
{
  "title": "Min-Heap Sift-Down Invariant Scrubber",
  "algorithm": "Binary Heap Sift-Down",
  "timeComplexity": "O(log n)",
  "spaceComplexity": "O(1)",
  "frames": [
    {
      "step": 1,
      "description": "Root has invalid high value 50 after extracting min. Needs sift-down.",
      "array": [50, 4, 7, 12, 15, 20, 30],
      "pointers": { "parent": 0, "smallestChild": 1 },
      "highlights": { "0": "pivot", "1": "active", "2": "comparing" },
      "variables": { "parentVal": 50, "leftVal": 4, "rightVal": 7, "swapWith": 4 },
      "invariants": "Left child 4 is smaller than right child 7 and parent 50 -> Swap parent with 4"
    },
    {
      "step": 2,
      "description": "Swapped 50 and 4. Current parent index is 1. Check children 12 and 15.",
      "array": [4, 50, 7, 12, 15, 20, 30],
      "pointers": { "parent": 1, "smallestChild": 3 },
      "highlights": { "1": "pivot", "3": "active", "4": "comparing" },
      "variables": { "parentVal": 50, "leftVal": 12, "rightVal": 15, "swapWith": 12 },
      "invariants": "Child 12 is smaller than parent 50 -> Swap parent with 12"
    },
    {
      "step": 3,
      "description": "Swapped 50 and 12. Parent index 3 is now a leaf node. Heap property fully restored!",
      "array": [4, 12, 7, 50, 15, 20, 30],
      "pointers": { "parent": 3 },
      "highlights": { "0": "sorted", "1": "sorted", "2": "sorted", "3": "sorted" },
      "variables": { "parentVal": 50, "heapPropertyRestored": true },
      "invariants": "Min-heap invariant holds: parent <= all children"
    }
  ]
}
```
""",

    "Module_10": """## Interactive Algorithm Trace Scrubber

```trace
{
  "title": "Kadane's Algorithm Maximum Subarray Sum",
  "algorithm": "Dynamic Programming: Kadane",
  "timeComplexity": "O(n)",
  "spaceComplexity": "O(1)",
  "frames": [
    {
      "step": 1,
      "description": "Index 0: val = -2. currentMax = -2, globalMax = -2.",
      "array": [-2, 1, -3, 4, -1, 2, 1, -5, 4],
      "pointers": { "i": 0 },
      "highlights": { "0": "active" },
      "variables": { "num": -2, "currentMax": -2, "globalMax": -2 },
      "invariants": "Initialize Kadane window with first element"
    },
    {
      "step": 2,
      "description": "Index 1: val = 1. max(1, -2 + 1) = 1. Reset window! globalMax = 1.",
      "array": [-2, 1, -3, 4, -1, 2, 1, -5, 4],
      "pointers": { "i": 1 },
      "highlights": { "1": "sorted" },
      "variables": { "num": 1, "currentMax": 1, "globalMax": 1 },
      "invariants": "Starting new subarray at index 1 is strictly better than extending -2"
    },
    {
      "step": 3,
      "description": "Index 3 to 6: Accumulated contiguous sum [4, -1, 2, 1] = 6.",
      "array": [-2, 1, -3, 4, -1, 2, 1, -5, 4],
      "pointers": { "start": 3, "end": 6 },
      "highlights": { "3": "sorted", "4": "sorted", "5": "sorted", "6": "sorted" },
      "variables": { "subArraySum": 6, "globalMax": 6 },
      "invariants": "Max contiguous subarray sum identified: 6 (indices [3..6])"
    }
  ]
}
```
"""
}

def inject_content(fpath, content_to_inject, marker="```mermaid"):
    if not os.path.exists(fpath):
        return False
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Check if marker already present
    if marker in text:
        return False # Already has diagram/trace

    # Inject after first heading or after first paragraph
    lines = text.splitlines()
    insert_idx = len(lines)
    for i, line in enumerate(lines):
        if line.startswith('# ') and i < 15:
            # Found main header, find end of intro paragraph
            for j in range(i + 1, min(len(lines), i + 25)):
                if lines[j].strip().startswith('## '):
                    insert_idx = j
                    break
            break

    new_lines = lines[:insert_idx] + ["\n" + content_to_inject.strip() + "\n"] + lines[insert_idx:]
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write("\n".join(new_lines))
    return True

def main():
    injected_diagrams = 0
    injected_traces = 0

    # 1. Inject Diagrams into READMEs
    for (course_prefix, mod_prefix), diagram in DIAGRAMS.items():
        course_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and d.startswith(course_prefix)]
        if not course_dirs:
            continue
        cdir = course_dirs[0]

        mod_dirs = [d for d in os.listdir(cdir) if os.path.isdir(os.path.join(cdir, d)) and d.startswith(mod_prefix)]
        if not mod_dirs:
            continue
        mdir = os.path.join(cdir, mod_dirs[0])

        # Target candidate files: 01_README.md, README.md
        for cand in ['01_README.md', 'README.md', '00_FOUNDATIONS_PLAYGROUND.md', '02_FOUNDATIONS_PLAYGROUND.md']:
            fpath = os.path.join(mdir, cand)
            if os.path.exists(fpath):
                if inject_content(fpath, diagram, marker="```mermaid"):
                    injected_diagrams += 1
                    print(f"Injected Mermaid diagram into {fpath}")
                    break

    # 2. Inject AlgorithmTraceScrubber traces into Course 02
    c02_dir = '02_Data_Structures_and_Algorithms'
    if os.path.exists(c02_dir):
        for mod_prefix, trace in SCRUBBER_TRACES.items():
            mod_dirs = [d for d in os.listdir(c02_dir) if os.path.isdir(os.path.join(c02_dir, d)) and d.startswith(mod_prefix)]
            if not mod_dirs:
                continue
            mdir = os.path.join(c02_dir, mod_dirs[0])
            for cand in ['02_FOUNDATIONS_PLAYGROUND.md', '01_README.md', '00_interactive_arrays_dynamic_arrays_and_strings.ipynb']:
                fpath = os.path.join(mdir, cand)
                if os.path.exists(fpath) and fpath.endswith('.md'):
                    if inject_content(fpath, trace, marker="```trace"):
                        injected_traces += 1
                        print(f"Injected Scrubber trace into {fpath}")
                        break

    print(f"\nSummary:")
    print(f"  Mermaid diagrams injected: {injected_diagrams}")
    print(f"  Scrubber traces injected:  {injected_traces}")

if __name__ == '__main__':
    main()
