# Beginner Playground - Probabilistic Data Structures

> *"A bouncer with a guest list who sometimes says 'maybe' but never wrongly says 'definitely not'. That one-sided error is what you buy, and it is worth an enormous amount of memory."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no
server, no `pip install`, no account to sign up for. You can read it in ten
minutes and run it in one:

```bash
python 00_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints
`All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import hashlib
```

---

## 1. Exact membership costs what it costs

A `set` of a million URLs stores a million URLs. There is no trick - if you need
to answer *exactly*, you must keep enough information to be exact.

If you can tolerate a specific, bounded, one-sided error, you can answer with a
few bits per item instead of a few hundred.

```python
items = [f"https://example.com/page/{i}" for i in range(100_000)]
exact = set(items)
exact_bytes = sum(len(s) for s in items)
print(f"exact set: roughly {exact_bytes / 1e6:.1f} MB of strings")
assert len(exact) == 100_000
```

---

## 2. A Bloom filter is a row of light switches

Take a big array of bits, all off. To add an item, hash it `k` different ways and
turn on the bit at each position.

To test an item, hash it the same `k` ways and look. If *any* of those bits is
off, the item was definitely never added - adding it would have turned that bit
on. If all of them are on, it is *probably* present: those bits may have been
turned on by other items.

```python
class BloomFilter:
    def __init__(self, bits, hashes):
        self.bits = bytearray(bits)
        self.size = bits
        self.hashes = hashes

    def _positions(self, item):
        digest = hashlib.sha256(item.encode()).digest()
        return [int.from_bytes(digest[i * 4:i * 4 + 4], "big") % self.size
                for i in range(self.hashes)]

    def add(self, item):
        for position in self._positions(item):
            self.bits[position] = 1

    def __contains__(self, item):
        return all(self.bits[p] for p in self._positions(item))


bloom = BloomFilter(bits=1_000_000, hashes=7)
for item in items:
    bloom.add(item)

packed_bytes = bloom.size / 8      # a real filter packs 8 flags per byte
print(f"bloom filter: {packed_bytes / 1e6:.3f} MB once packed as real bits")
print(f"exact set:    {exact_bytes / 1e6:.1f} MB of strings")
print("(this teaching version uses a whole byte per flag, for readability)")
assert packed_bytes < exact_bytes / 20, "over 20x smaller"
```

---

## 3. Measure the error, and confirm which direction it goes

Two claims to check, and they are not symmetric:

1. **No false negatives, ever.** Every item that was added is reported present.
   This is a guarantee, not a probability - it follows from the fact that bits are
   only ever turned on.
2. **Some false positives.** Items never added are occasionally reported present,
   at a rate you can calculate in advance from the size and the number of hashes.

```python
false_negatives = sum(1 for item in items if item not in bloom)
print("false negatives:", false_negatives)
assert false_negatives == 0, "this is guaranteed by construction"

never_added = [f"https://example.com/other/{i}" for i in range(100_000)]
false_positives = sum(1 for item in never_added if item in bloom)
rate = false_positives / len(never_added)
print(f"false positives: {false_positives:,} of {len(never_added):,} = {rate:.2%}")
assert 0 < rate < 0.05, "a small, measurable, bounded error rate"
print()
print("So: 'not present' is proof. 'Present' means 'go and check properly'.")
```

---

## 4. The same trade, twice more

**HyperLogLog** counts distinct items. It keeps only the longest run of leading
zeros it has seen in the hashes - because seeing 10 leading zeros suggests you
have looked at roughly 2^10 distinct things. A few kilobytes estimates billions of
uniques to within about 2%.

**Count-Min Sketch** estimates how often each item appeared. It can overestimate
(collisions add) but never underestimates, so "which items are above this
threshold" is answerable without storing a counter per item.

The pattern is always the same: name the error you can live with, and trade it for
memory.

```python
class CountMinSketch:
    def __init__(self, width, depth):
        self.width, self.depth = width, depth
        self.counts = [[0] * width for _ in range(depth)]

    def _cols(self, item):
        digest = hashlib.sha256(item.encode()).digest()
        return [int.from_bytes(digest[i * 4:i * 4 + 4], "big") % self.width
                for i in range(self.depth)]

    def add(self, item):
        for row, col in enumerate(self._cols(item)):
            self.counts[row][col] += 1

    def estimate(self, item):
        return min(self.counts[row][col] for row, col in enumerate(self._cols(item)))


sketch = CountMinSketch(width=2_000, depth=5)
truth = {"popular": 5_000, "rare": 3}
for item, times in truth.items():
    for _ in range(times):
        sketch.add(item)
for i in range(20_000):
    sketch.add(f"noise{i}")

for item, actual in truth.items():
    guess = sketch.estimate(item)
    print(f"  {item:<8} actual {actual:>5,}  estimated {guess:>5,}")
    assert guess >= actual, "Count-Min never undercounts - it takes the minimum row"
print("Overestimates only. That one-sidedness is what makes it safe to use.")
```

---

## 5. Predict before you run

A Bloom filter says an item is NOT in the set. How confident should you be?
Now it says an item IS in the set. How confident should you be? The two
answers are not the same, and that asymmetry is the whole idea.

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

Every LSM-tree database puts a Bloom filter in front of each file so a read
can skip files that definitely do not contain the key. Chrome used one for
malicious URLs. The memory saving is 10-100x, and the cost is a class of error
you have to design around rather than eliminate.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
