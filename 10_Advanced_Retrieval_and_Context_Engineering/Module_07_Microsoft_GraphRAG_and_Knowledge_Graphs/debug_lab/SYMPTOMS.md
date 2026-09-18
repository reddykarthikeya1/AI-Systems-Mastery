# Debug Lab Incident Report: The Graph's Obvious Hub Entity Is Missing From Rankings

- **Severity:** P1 Retrieval Correctness
- **Affected Subsystem:** Module_07_Microsoft_GraphRAG_and_Knowledge_Graphs
- **Reported Impact:** GraphRAG queries about a well-known, heavily-referenced
  entity return thin or irrelevant context, because that entity never gets
  selected during the "which entities matter most" ranking step used to
  assemble the context window.

---

## Observable Symptoms & Logs
```text
Relationships extracted from the source documents:
  Alice --works_at--> Acme Corp
  Bob --works_at--> Acme Corp
  Carol --works_at--> Acme Corp
  Alice --knows--> Bob

Computed degree centrality: {'Alice': 2, 'Bob': 1, 'Carol': 1}
Expected: 'Acme Corp' is referenced by three separate relationships (it's the
clear hub of this graph) and should be the #1 ranked entity.
Actual top-ranked entity for context building: Alice
Is 'Acme Corp' even present in the degree scores? False
```
`Acme Corp` is the target of three separate relationships -- clearly the most
referenced entity in the graph -- yet it has no entry at all in
`degree_centrality`, and a far less-connected entity (`Alice`) is ranked #1
instead.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_07_Microsoft_GraphRAG_and_Knowledge_Graphs/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_entity_centrality.py
   ```
3. Observe that `degree` has no key for `Acme Corp`, despite it appearing in
   three of the four extracted relationships.

---

## Your Objective
1. Inspect `compute_degree_centrality()` and trace exactly which part of
   each `(source, target, relation)` triple it updates a score for.
2. Consider what "connected" means for a relationship like
   `Alice --works_at--> Acme Corp` -- does only `Alice` become more
   connected, or does `Acme Corp` too?
3. Formulate a hypothesis for why an entity that only ever appears as a
   `target` never accumulates any score, then check `ANSWERS.md`.
