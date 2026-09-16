# Module 04: Agent Memory Systems

## 1. Theoretical Foundations: Cognitive Architectures & Memory Types

In autonomous agents, memory is not merely a single vector database or conversation history; it is a multi-tiered subsystem designed to balance working context constraints with long-term knowledge retention.

### 1.1 Memory Taxonomy

| Memory Tier | Storage Medium | Access Latency | Retention Duration | Biological Analogy |
| :--- | :--- | :--- | :--- | :--- |
| **Working Memory** | LLM Context Window | Instant (in prompt) | Single Session | Prefrontal Cortex |
| **Episodic Memory** | Dense Vector Store + Timestamps | 5 - 20 ms | Days to Months | Hippocampus |
| **Semantic Memory** | Knowledge Graph / Key-Value | 2 - 10 ms | Permanent | Cerebral Cortex |
| **Procedural Memory** | System Prompt / Code Tools | Static | Permanent | Basal Ganglia |

---

## 2. Episodic Retrieval Formulation (Park et al., 2023)

When querying episodic memory with user query $q$, each stored memory $m_i$ is evaluated against three normalized scoring factors:

$$\text{Score}(m_i, q) = w_r \cdot \text{Recency}(m_i) + w_i \cdot \text{Importance}(m_i) + w_s \cdot \text{Relevance}(m_i, q)$$

where:
1. **Recency**:
   $$\text{Recency}(m_i) = \lambda^{t_{now} - t_i}, \quad \lambda \in (0, 1)$$
2. **Importance**: Integer rating $[1, 10]$ assigned by an LLM prompt assessing how crucial the information is.
3. **Relevance**: Cosine similarity between embedding of memory content and query:
   $$\text{Relevance}(m_i, q) = \frac{\mathbf{e}(m_i) \cdot \mathbf{e}(q)}{\|\mathbf{e}(m_i)\| \|\mathbf{e}(q)\|}$$

---

## 3. Reflection & Memory Consolidation

As episodic memories accumulate, raw events overwhelm retrieval accuracy. Periodic **Reflection** processes raw events into high-level abstractions:
1. Take the last $N$ episodic events.
2. Ask the LLM: *"What are the 3 most important high-level insights or behavioral patterns evident from these interactions?"*
3. Store the synthesized insights as new high-importance Semantic / Episodic nodes.
