# Module 01: Self-Assessment & Staff Engineering Interview Challenges

## Part I: Deep Diagnostic Questions & Comprehensive Solutions

### Scenario 1: Multi-Page PDF Table Reconstruction
**Question**: An insurance policy PDF contains a 4-page table with claim coverage rules. Naive OCR tools extract tables as unformatted raw lines, losing column alignment and header names on pages 2–4. How do you design an enterprise ingestion pipeline that preserves table relational integrity?

**Solution**:
1. **Layout-Aware Vision / Bounding Box Parsing**: Use layout models (e.g. LayoutLM / Marker / Docling) to detect table bounding boxes and cell coordinates across page breaks.
2. **Header Propagation**: If a table spans multiple pages, detect header repetition or propagate the primary header row across subsequent page fragments.
3. **Markdown / HTML Linearization**: Convert the parsed grid into structured Markdown or HTML table syntax (`| Col A | Col B |`).
4. **Row-Level Chunking with Header Injection**: Instead of arbitrary token splitting, chunk by table rows, prepending the full column header schema to every single row chunk.

---

### Scenario 2: Semantic Chunking via Embedding Cosine Shift
**Question**: How does semantic chunking identify natural topic transitions, and what statistical threshold prevents over-segmentation?

**Solution**:
1. Split document into individual sentences: $(s_1, s_2, \dots, s_n)$.
2. Compute sliding sentence group embeddings and calculate cosine distance between adjacent sentence pairs:
   $$d_i = 1 - \cos(\text{Embed}(s_i), \text{Embed}(s_{i+1}))$$
3. Compute moving average $\mu$ and standard deviation $\sigma$ of distances.
4. Establish breakpoint threshold:
   $$\tau = \mu + k \cdot \sigma, \quad k \in [1.0, 2.0]$$
   Whenever $d_i > \tau$, trigger a chunk boundary.
