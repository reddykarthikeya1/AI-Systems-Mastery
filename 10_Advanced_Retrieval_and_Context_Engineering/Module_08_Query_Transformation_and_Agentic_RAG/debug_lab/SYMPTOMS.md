# Debug Lab Incident Report: Agentic RAG Answers Only the Last Sub-Question

- **Severity:** P1 Answer Completeness
- **Affected Subsystem:** Module_08_Query_Transformation_and_Agentic_RAG
- **Reported Impact:** Multi-part user questions get answered as if only the
  final decomposed sub-question existed -- earlier sub-questions' retrieved
  evidence never makes it into the context handed to the answer-synthesis
  step, even though the retriever clearly found relevant documents for them.

---

## Observable Symptoms & Logs
```text
Complex query decomposed into 3 sub-questions:
  - 'What is the refund window?' -> [('doc_refund', 0.91), ('doc_faq', 0.4)]
  - 'Do exchanges need a receipt?' -> [('doc_exchange', 0.88), ('doc_faq', 0.35)]
  - 'How long does shipping take?' -> [('doc_shipping', 0.85), ('doc_faq', 0.3)]

Expected: all 4 distinct documents retrieved across the 3 sub-questions
should be in the merged context: ['doc_exchange', 'doc_faq', 'doc_refund', 'doc_shipping']
Actual merged context: {0: ('doc_shipping', 0.85), 1: ('doc_faq', 0.3)}
Actual surviving documents (2): ['doc_faq', 'doc_shipping']
```
Only the documents retrieved by the *last* sub-question (`"How long does
shipping take?"`) survive in the merged context. `doc_refund` and
`doc_exchange` -- the direct answers to the first two sub-questions -- are
completely absent, even though `retrieve()` clearly returned them.

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_08_Query_Transformation_and_Agentic_RAG/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_query_decomposition.py
   ```
3. Observe that `combined_context` only has 2 entries even though 3
   sub-questions each retrieved 2 documents (6 retrievals, 4 distinct docs).

---

## Your Objective
1. Inspect `gather_context()` and trace exactly what key is used to store
   each retrieved result into the `combined` dictionary.
2. Consider what happens when two different sub-questions both retrieve a
   result at the same `rank` position (e.g. both have a rank-0 hit).
3. Formulate a hypothesis for why only the last sub-question's results
   remain, then check `ANSWERS.md`.
