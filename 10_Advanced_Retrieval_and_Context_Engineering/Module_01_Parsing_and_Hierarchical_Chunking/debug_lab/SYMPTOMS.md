# Debug Lab Incident Report: Facts Straddling a Chunk Boundary Vanish From Retrieval

- **Severity:** P2 Retrieval Quality Regression
- **Affected Subsystem:** Module_01_Parsing_and_Hierarchical_Chunking
- **Reported Impact:** Users asking questions whose answer spans two
  paragraphs near a chunk boundary get no relevant hits, even though the
  chunker is configured with a nonzero overlap specifically to prevent this.

---

## Observable Symptoms & Logs
```text
Document length: 185 chars, chunk_size=40, overlap=10
Chunks produced:
  [0] 'Section 1: Refunds are processed within '
  [1] 'five business days of the return being r'
  [2] 'eceived. Section 2: Exchanges require th'
  [3] 'e original receipt and must occur within'
  [4] ' thirty days of purchase.'

Expected: the boundary phrase 'received. Section 2' (which straddles a chunk
cut) should appear INTACT in at least one chunk, thanks to the 10-char
overlap.
Actual: phrase found intact in some chunk = False
```
Chunk `[2]` starts mid-word (`'eceived. Section 2...'`), showing the cut
landed inside `"received"` -- and no chunk contains the full phrase
`"received. Section 2"` even though `OVERLAP = 10` is configured.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_01_Parsing_and_Hierarchical_Chunking/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_chunker.py
   ```
3. Observe that consecutive chunks pick up exactly where the previous one
   left off, with no repeated characters between them.

---

## Your Objective
1. Inspect `chunk_document()` and trace exactly how `start` is updated for
   the next iteration of the loop.
2. Compare that against the `overlap` parameter -- is it used anywhere in the
   function body?
3. Formulate a hypothesis for why consecutive chunks never share any
   characters despite `overlap=10`, then check `ANSWERS.md`.
