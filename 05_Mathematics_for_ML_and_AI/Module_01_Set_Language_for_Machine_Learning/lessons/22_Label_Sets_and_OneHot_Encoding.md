# Lesson 01.22 — Label Sets and One-Hot Encoding

> **Module 01:** Set Language for Machine Learning · Lesson 22 of 25

---

## What you will be able to do after this lesson

- [ ] Represent a label set as a one-hot encoding and state the invariant a valid one-hot row satisfies.
- [ ] Explain what happens at inference when a category appears that was absent from training.

## Prerequisites

- [Lesson 01.11](11_Functions_as_Special_Relations.md) - functions, domain and range.

---

## 1. The idea

A **label set** `Y` is the set of classes a model may emit. **One-hot encoding**
is an injective map from Y into `{0,1}^|Y|` sending the k-th label to the vector
with 1 in position k and 0 elsewhere.

The valid images form a strict subset of `{0,1}^|Y|`: exactly those with a single
1. That is `|Y|` vectors out of `2^|Y|`, and the constraint

    each entry is 0 or 1, and the entries sum to 1

is the invariant. Most of `{0,1}^|Y|` is not a valid encoding, which is the same
codomain-versus-range distinction as before.

Injectivity is what makes decoding possible: `argmax` recovers the label because
no two labels share an encoding. If two categories were accidentally normalised
to the same string, the map stops being injective and decoding returns whichever
happens to win.

The operational question this lesson exists for: **what is `Y`, and where is it
defined?** If Y is derived from the training data, then a category appearing at
inference and not in training has no encoding at all - it is outside the domain.
The options are all explicit decisions: reject the row, map it to a reserved
`<UNK>` slot, or retrain. Silently dropping it is what happens when nobody
chooses.

## 2. Worked example

`Y = {cat, dog, bird}`, fixed in that order. Then

    cat  -> (1, 0, 0)
    dog  -> (0, 1, 0)
    bird -> (0, 0, 1)

Three valid vectors out of `2³ = 8` possible binary triples. `(1,1,0)` and
`(0,0,0)` are in the codomain and are not encodings of anything.

**Decoding.** `argmax((0,1,0)) = 1`, and index 1 is `dog` ✓. This relies on the
order of Y being fixed and shared between encoder and decoder. Sort the labels
differently at inference and every prediction is silently relabelled - the
vectors are correct and the names attached to them are wrong.

**An unseen category.** A row arrives with label `fish`. It is not in Y, so it
has no encoding. Building the encoding from `sorted(set(training_labels))` means
Y is whatever the training file contained, and `fish` simply has no slot. Code
that does `Y.index(label)` raises; code that does `.get(label, zeros)` produces
`(0,0,0)` - a vector that is not a valid one-hot and that no downstream check
will question unless someone wrote the invariant down.

## 3. Verify it in code

```python
import numpy as np

Y = ["bird", "cat", "dog"]          # fixed order, shared by encoder and decoder
index = {label: i for i, label in enumerate(Y)}

def one_hot(label):
    v = np.zeros(len(Y), dtype=int)
    v[index[label]] = 1
    return v

def decode(v):
    return Y[int(np.argmax(v))]

assert list(one_hot("cat")) == [0, 1, 0]
assert decode(one_hot("dog")) == "dog"
assert all(decode(one_hot(y)) == y for y in Y), "the map is injective"

# The invariant a valid one-hot row satisfies.
def valid(v):
    v = np.asarray(v)
    return bool(np.all((v == 0) | (v == 1)) and v.sum() == 1)

assert valid(one_hot("bird"))
assert not valid([1, 1, 0]), "in the codomain, not in the range"
assert not valid([0, 0, 0])

# Only |Y| of the 2^|Y| binary vectors are valid encodings.
from itertools import product
assert sum(1 for v in product([0, 1], repeat=3) if valid(v)) == 3
assert 2 ** 3 == 8

# An unseen category has no encoding - this must be a decision, not an accident.
try:
    one_hot("fish")
    raise AssertionError("should have failed")
except KeyError:
    pass

# The explicit choice: a reserved slot.
Y_UNK = [*Y, "<UNK>"]
index_unk = {label: i for i, label in enumerate(Y_UNK)}
def one_hot_unk(label):
    v = np.zeros(len(Y_UNK), dtype=int)
    v[index_unk.get(label, index_unk["<UNK>"])] = 1
    return v
assert valid(one_hot_unk("fish"))
assert decode_unk if False else Y_UNK[int(np.argmax(one_hot_unk("fish")))] == "<UNK>"
```

## 4. The mistake people actually make

**Deriving the label order from a set, whose iteration order is not guaranteed.**

`list(set(labels))` gives no ordering promise across runs or Python versions.
Build the encoder in one process and the decoder in another and the index-to-
label mapping can differ, so every prediction is silently mislabelled. Accuracy
looks like chance and the model is blamed.

The variant that is worse because it looks careful: building the order from
`sorted(set(training_labels))` in both places. That is deterministic *given the
same label set* - and the label set changes when a new category appears in the
training data, which shifts every index after it. A model trained last month and
a decoder built today then disagree, with no error.

The label set and its order belong in a saved artefact next to the model
weights, versioned with them. Deriving them from data at load time makes the
model's meaning depend on which data happened to be present.

---

## Check yourself

1. How many valid one-hot vectors are there for 6 labels, out of how many binary vectors of that length?
2. Why must the ordering of the label set be saved with the model?
3. A category appears at inference that was absent from training. Name two defensible responses and one non-response.

<details>
<summary>Answers</summary>

1. 6 valid, out of 2⁶ = 64. Only the vectors with exactly one 1 are encodings.
2. Because decoding uses the index produced by `argmax`, and that index only means a particular label under a particular ordering. A different order at decode time relabels every prediction with no error.
3. Defensible: reject the row as out-of-domain, or map it to a reserved `<UNK>` slot that was included at training time. The non-response is silently producing an all-zero vector, which is not a valid encoding and which downstream code will accept.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](21_Feature_Spaces_as_Sets.md) · [Module README](../README.md) · [Next →](23_Train_Validation_and_Test_as_a_Partition.md)
