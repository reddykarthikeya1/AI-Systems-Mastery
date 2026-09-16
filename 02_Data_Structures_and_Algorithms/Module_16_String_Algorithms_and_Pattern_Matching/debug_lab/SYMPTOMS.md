# Debug Lab 16 - Symptoms

> A text-processing service: counting markers, scanning a document, and
> screening against a dictionary of terms. Each matcher is almost right.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom - the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_string_search.py
echo "exit=$?"
```

There are **3** distinct defects.

---

## Symptom 1 - The fast matcher finds fewer markers than the reference scan

```
    text='AAAAAAAA' marker='AA'
    reference scan found : 7 at [0, 1, 2, 3, 4, 5, 6]
    fast matcher found   : 4 at [0, 2, 4, 6]
```

Both are scanning the same string for the same two characters. The reference
scan is a plain slice comparison at every offset and is not in doubt.

Four is not a random number. It is exactly the count you would get under one
particular assumption about what should happen after a match succeeds.

**Ask yourself:** after reporting a match, where should the search resume from?

---

## Symptom 2 - The rolling-hash scan reports more hits than exist

```
    token='ain'
    reference scan found : 7 at [5, 14, 25, 40, 54, 61, 74]
    rolling hash found   : 10 at [5, 14, 24, 25, 40, 54, 60, 61, 73, 74]
```

Every offset the reference scan found is also in the fast list - nothing was
missed. But three extra offsets appear (24, 60, 73), and the token is genuinely
not at those positions in the document.

Check one of them by hand: slice the document at offset 24 and look at the three
characters you get.

**Ask yourself:** what has the fast version actually proved when its inner test
succeeds? Is that the same thing as "the pattern is here"?

---

## Symptom 3 - The content filter misses a term that is plainly present

```
    text='ushers'
    reference scan flagged : ['he', 'hers', 'she']
    filter flagged         : ['hers', 'she']
```

The word `he` appears in `ushers` - twice, in fact, inside both `she` and
`hers`. The filter found the longer terms and not the shorter one contained
within them.

That is a specific kind of blindness: it only fails for terms that are a
*suffix* of a path the automaton is already walking.

**Ask yourself:** when the machine arrives at the node for `she`, what else is
true about the text it has just consumed - and how would the machine ever come
to know it?
