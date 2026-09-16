# Debug Lab 07 - Symptoms

> A low-rank compressor of the kind LoRA uses: keep the k most important directions and throw the rest away.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom - the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_lowrank_compressor.py
echo "exit=$?"
```

There are **3** sections below. Not all of them contain a defect; deciding
which are sound is part of the exercise.

---

## Section 1 - The singular values look normal

```
    [50.0, 12.0, 3.0, 0.4, 0.05]
    total energy: 2653.16
```

Descending, as the convention requires, and the total energy is the sum of their squares. Nothing wrong.

**Ask yourself:** which end of this list carries the information?

---

## Section 2 - Keeping one component retains almost no energy

```
    k=1: 0.000001
    k=2: 0.000061
    k=3: 0.003453
    k=4: 0.057728
    k=5: 1.000000
```

The largest singular value is 50 and the next is 12, so the first component alone should carry the overwhelming majority of the energy. The table says k=1 retains a tiny fraction, and the numbers only become sensible as k approaches 5.

**Ask yourself:** the values are sorted descending. Which slice of the list does `singular_values[-k:]` actually take?

---

## Section 3 - It decided to keep everything, and still called it compression

```
    rank chosen for 99% energy: 5
    a 1000x1000 weight matrix at that rank:
      dense parameters  : 1,000,000
      factored parameters: 10,000
      compression ratio : 100.0x
```

The rank chosen is 5 - out of 5. The compressor concluded that not a single direction could be discarded, on a matrix whose singular values run from 50 down to 0.05.

The 100x ratio looks impressive and is beside the point: a truncation that truncates nothing is not a truncation. Both numbers follow from the previous section.

**Ask yourself:** if the ranking were the right way round, what k would reach 99% here, and what compression would that give? Work it out by hand before changing any code.

---
