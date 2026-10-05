# Chapter 8: Company-Specific Coding Archetypes & Interview Rubrics

> **Preceding Bridge:** In [Chapter 02: Essential Patterns](02-Essential-Patterns-Cheat-Sheet.md) and [Chapter 03: The Core 75 Mastery Walkthroughs](03-The-Core-75-Mastery-Walkthroughs.md), you mastered universal algorithmic templates. In this chapter, we calibrate your preparation for specific Tier-1 Product-Based Companies (Google, Meta, Amazon, Uber, Stripe). You will learn which patterns each company over-indexes on, how their interview rubrics evaluate candidates, and how to avoid company-specific pitfalls.

---

## 1. Plain-English Jargon Demystifier

| Technical Term | Plain English Translation | Real-World Metaphor |
| :--- | :--- | :--- |
| **Over-Indexing** | When a specific company's interviewers disproportionately favor certain problem patterns over others. | An Italian restaurant heavily favoring pasta and olive oil, while a sushi bar favors rice and raw fish. |
| **Bar Raiser** | An independent interviewer from another department whose sole job is to ensure you meet high cross-company standards. | An outside health inspector ensuring the kitchen meets national food safety laws. |
| **Speed vs Depth Trade-off** | Meta expects 2 Mediums in 40 minutes (blazing speed), whereas Google expects 1 deep problem with curveballs (deep architectural exploration). | A 100-meter sprint (Meta) versus a tactical 5,000-meter chess match (Google). |
| **Clean Code Rubric** | Scoring based on idiomatic syntax, modular helper functions, meaningful variable names, and zero global state. | A mechanic returning your car with the engine wiped clean, tools organized, and zero grease stains on the seats. |

---

## 2. Company-Specific Pattern Frequency Matrix

Not all companies ask the same questions! Use this matrix to focus your study time based on your target company:

| Algorithmic Pattern | Google | Meta | Amazon | Uber / Stripe |
| :--- | :---: | :---: | :---: | :---: |
| **Graph BFS / DFS & Topological Sort** | **VERY HIGH** | HIGH | MEDIUM | HIGH |
| **Dynamic Programming (1D, 2D, Trees)** | **VERY HIGH** | LOW / MED | LOW | MEDIUM |
| **Binary Search on Answer Space** | MEDIUM | **VERY HIGH** | MEDIUM | MEDIUM |
| **Two Pointers & Sliding Window** | MEDIUM | **VERY HIGH** | HIGH | **VERY HIGH** |
| **Heap / Priority Queue (Top K)** | MEDIUM | MEDIUM | **VERY HIGH** | HIGH |
| **Intervals (Merge, Sweep-Line)** | MEDIUM | HIGH | HIGH | **VERY HIGH** |
| **Trie & Prefix Matching** | **HIGH** | LOW | MEDIUM | MEDIUM |
| **Monotonic Stack / Deque** | **HIGH** | MEDIUM | MEDIUM | **HIGH** |

---

## 3. Deep Dive: The Big 4 Company Rubrics

### 1. Google: The Architectural Explorer
* **The Format:** Typically 1 complex problem per 45-minute round, followed by 1 or 2 dynamic follow-up curveballs.
* **What Google Values:**
  1. **First-Principles Modeling:** Google rarely asks vanilla LeetCode problems. They present real-world scenarios (e.g., *"Model a distributed build dependency graph"* $\to$ Topological Sort with cycle detection).
  2. **Mathematical Invariants:** Explain *why* your greedy choice is optimal.
  3. **Extensibility:** Writing clean modular code that can easily accommodate follow-up constraints (e.g., *"What if the graph cannot fit in memory?"*).
* **Fatal Google Trap:** Memorizing code without understanding the underlying proof. If the interviewer changes one constraint and you blindly regurgitate LeetCode, it is an automatic rejection.

### 2. Meta (Facebook): The 100% Bug-Free Speed Demon
* **The Format:** Exactly **2 LeetCode Mediums in 40 minutes** (20 minutes per problem including explanation, coding, and dry-run).
* **What Meta Values:**
  1. **Speed & Fluency:** You must recognize the pattern within 60 seconds and start typing cleanly.
  2. **Zero Syntax or Off-by-One Bugs:** Meta strongly penalizes candidates who run buggy code or fail simple boundary checks.
  3. **No Hints Required:** A "Strong Hire" at Meta solves both problems without the interviewer needing to nudge them.
* **Fatal Meta Trap:** Spending 10 minutes discussing theoretical trade-offs. Jump straight into: State constraints $\to$ Propose optimal Big-O $\to$ Write typed code $\to$ Dry run with test cases.

### 3. Amazon: The Pragmatic Systems Builder
* **The Format:** 1 Coding Problem + 20 minutes of Behavioral Leadership Principles (Customer Obsession, Ownership, Bias for Action).
* **What Amazon Values:**
  1. **Clean Object-Oriented Code:** Use dataclasses, clear class hierarchies, and avoid 5-level nested loops.
  2. **Pragmatic Edge Cases:** Null checks, empty collections, negative numbers, extreme capacity limits.
  3. **Explaining Trade-Offs in Plain English:** Justify why you chose a Hash Map over a Tree in terms of memory and latency.
* **Fatal Amazon Trap:** Ignoring the Leadership Principles questions. You can write perfect code, but if you fail the LP stories, the Bar Raiser will veto your offer!

### 4. Uber & Stripe: Real-World Concurrency & Geospatial Data
* **The Format:** Practical algorithmic challenges involving financial ledgers, time intervals, geofences, and rate limiting.
* **What Uber/Stripe Values:**
  1. **Interval Manipulation:** Overlapping driver shifts, surge pricing intervals, scheduling windows.
  2. **Data Structure Hygiene:** Storing financial numbers as integer cents rather than floats.
  3. **Thread-Safety & Race Conditions:** Asking whether your in-memory cache needs a lock.
* **Fatal Uber/Stripe Trap:** Using floating-point variables for currency or failing to handle overlapping time boundaries correctly.

---

## 4. The 5-Minute Opening Interview Script

When the interviewer finishes reading the prompt, do **NOT** start typing immediately! Recite this standardized 5-step checklist:

1. **Clarify Constraints (60s):**
   > *"Before diving in, I want to clarify: Can the input array be empty or contain negative numbers? What is the maximum value of $N$ so I can target the right Big-O complexity?"*
2. **State Edge Cases (60s):**
   > *"I see three key edge cases: $N=0$, all identical elements, and an array already sorted in reverse order."*
3. **Propose Brute Force & Explain Big-O Failure (60s):**
   > *"A naive brute-force approach would check every subarray using nested loops in $O(N^2)$ time. But with $N=10^5$, $O(N^2)$ will trigger a Time Limit Exceeded (TLE)."*
4. **Present the Optimal Pattern & Invariant (60s):**
   > *"We can achieve $O(N)$ time using a Monotonic Stack / Sliding Window, because each element is pushed and popped at most once."*
5. **Ask for Alignment Before Coding (30s):**
   > *"Does this approach sound good to you, or would you like me to consider an alternate trade-off before I write the code?"*

---

## 5. Chapter Milestone Check

Verify your understanding before your interviews:

1. **Why does Meta's interview process demand a fundamentally different pacing strategy than Google's?**
   - *Answer:* Meta tests speed and implementation precision under pressure (2 Mediums in 40 minutes), requiring immediate pattern execution and zero bugs. Google tests conceptual depth and mathematical problem-modeling (1 deep problem with evolving constraints).
2. **Which algorithmic patterns should you practice most heavily for Uber, Stripe, and fintech interviews?**
   - *Answer:* Interval merging/sweep-line algorithms, Sliding Window, Coordinate Compression, and Double-Entry ledger state tracking.
3. **What is the number one reason candidates fail Amazon coding interviews despite writing working code?**
   - *Answer:* Failing the 20-minute Behavioral Leadership Principles portion or failing to demonstrate clean, maintainable code structure (treating code as a competitive programming hack rather than production software).
