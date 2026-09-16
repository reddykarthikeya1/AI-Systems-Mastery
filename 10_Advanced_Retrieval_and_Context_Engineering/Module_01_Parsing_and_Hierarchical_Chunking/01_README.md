# Module 01: Parsing & Hierarchical Chunking

## 1. Structural Document Parsing Foundations

Real-world enterprise documents (PDFs, DOCX, Markdown, HTML) are non-linear hierarchical data structures containing titles, headings, bullet lists, code blocks, and multi-column tables.

### 1.1 Naive Fixed-Window vs. Structural Chunking
- **Fixed-Window Chunking**: Chops raw text into character or token slices of size $K$ with overlap $O$. Slices across sentence boundaries, separates table headers from cell data, and destroys Markdown header hierarchies.
- **Structural AST Parsing**: Converts documents into an Abstract Syntax Tree (AST), preserving heading levels ($H_1, H_2, H_3$), code blocks, and table elements as discrete semantic blocks.

---

## 2. Parent-Child Hierarchical Architecture

Let a document $\mathcal{D}$ be partitioned into coarse parent blocks $\mathcal{P} = \{P_1, P_2, \dots, P_m\}$ and fine child blocks $\mathcal{C} = \{c_1, c_2, \dots, c_n\}$:
$$\bigcup_{j \in \text{children}(P_i)} c_j \subseteq P_i$$

1. **Indexing**: Embed only child blocks: $v_j = \text{Embed}(c_j)$. Store $v_j$ in vector index with metadata `{"parent_id": P_i}`.
2. **Querying**: Given user query $q$, compute top-$k$ nearest child vectors:
   $$\mathcal{C}^* = \arg\max_{c \in \mathcal{C}}^{(k)} \text{sim}(\text{Embed}(q), \text{Embed}(c))$$
3. **Context Assembly**: Deduplicate parent IDs $\mathcal{P}^* = \bigcup_{c \in \mathcal{C}^*} \text{parent\_id}(c)$ and inject full parent chunks into LLM context.
