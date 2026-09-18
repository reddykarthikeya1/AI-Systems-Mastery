# Debug Lab Incident Report: Contextual Retrieval Returns the Wrong Policy Chunk, and One Topic Is Unsearchable

- **Severity:** P1 Retrieval Correctness
- **Affected Subsystem:** Module_02_Contextual_Retrieval_Architecture
- **Reported Impact:** A support-bot query about shipping times returned the
  exchange policy instead, and a separate audit found the shipping-policy
  chunk cannot be retrieved by ANY query -- it appears to have vanished from
  the index entirely after the contextual-retrieval preprocessing step.

---

## Observable Symptoms & Logs
```text
Source corpus has 3 chunks (refund, exchange, shipping).
Chunks that actually made it into the embedded index: 2
  embedded[0]: "This chunk explains the store's exchange policy. Refunds are issued within five business days of the return arriving at our warehouse."
  embedded[1]: "This chunk explains the store's shipping policy. Exchanges require the original receipt and must happen within thirty days of purchase."

Query: 'How long does international shipping take?'
Expected: the top match should be the shipping-policy chunk ('Shipping to international addresses adds'...).
Actual similarities over the embedded index: [0.0, 0.408]
Actual top match text: "This chunk explains the store's shipping policy. Exchanges require the original receipt and must happen within thirty days of purchase."
Is the shipping chunk even present in the embedded index? False
```
Two things stand out: (1) the embedded index has only 2 entries for 3 source
chunks -- the shipping chunk is missing entirely -- and (2) each surviving
embedded entry pairs a chunk's raw text with a *different* chunk's topic
sentence (the "exchange policy" context sentence is glued onto the refund
chunk's raw text, and vice versa).

---

## How to Reproduce
1. Navigate to this module's debug lab:
   ```bash
   cd Module_02_Contextual_Retrieval_Architecture/debug_lab
   ```
2. Run the defective simulation script:
   ```bash
   python broken_contextual_retrieval.py
   ```
3. Observe that the embedded index has fewer entries than the source corpus,
   and that a shipping-related query never surfaces the shipping chunk.

---

## Your Objective
1. Inspect `contextualize_chunks()` and trace exactly how `contexts` and
   `chunks` are paired together with `zip()`.
2. Compare the length of `contexts[1:]` against the length of `chunks`, and
   consider what `zip()` does when its inputs have different lengths.
3. Formulate a hypothesis for why one chunk disappears and the remaining ones
   get the wrong context sentence, then check `ANSWERS.md`.
