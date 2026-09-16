# Beginner Playground: String Matching

> *"Finding a word in a book. You do not start from page 1 again every time a
> sentence turns out to be the wrong one - you remember what you have read."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. The slow way, and why it is slow

To find `cat` in `concatenate`, line the word up at position 0, compare, slide
right by one, compare again. That works, and for short text it is fine.

The waste shows up when the pattern repeats itself:

```python
text = "aaaaaaaaab"
pattern = "aaaab"

comparisons = 0
for start in range(len(text) - len(pattern) + 1):
    for i, character in enumerate(pattern):
        comparisons += 1
        if text[start + i] != character:
            break
print("character comparisons:", comparisons)   # 26 for a 10-character text
```

At every offset it compares four `a`s, fails on the `b`, and then throws away
everything it just learned.

---

## 2. The idea: remember what you matched

If you matched `abab` and then failed, you do not have to start over. `ab` at the
end of what you matched is also the *start* of the pattern - so two characters
are still good.

The table that records this is the whole of KMP:

```python
def prefix_table(pattern):
    pi = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = pi[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        pi[i] = k
    return pi

print(prefix_table("ababaca"))     # [0, 0, 1, 2, 3, 0, 1]
```

Read entry 4: the value 3 says *"the first 3 characters of the pattern are also
the last 3 of what you have matched so far"*. So a failure there costs you
nothing - you keep going with 3 already matched.

---

## 3. A hash you can slide

A different trick. Turn each window of text into a number, and update that number
in one step as the window slides - no need to re-read the characters:

```python
text, width = "abcde", 3
base, mod = 257, 1_000_003

value = 0
for character in text[:width]:
    value = (value * base + ord(character)) % mod
print("hash of 'abc':", value)

high = pow(base, width - 1, mod)
value = (value - ord("a") * high) % mod      # drop the 'a'
value = (value * base + ord("d")) % mod      # add the 'd'
print("hash of 'bcd':", value)
```

**The catch, and it matters:** two different strings can produce the same number.
So when the hashes match you must still compare the actual characters. A hash
match means *"worth checking"*, never *"found it"*.

---

## 4. Many words at once

Searching for 500 banned words by running one search 500 times reads the text
500 times. Aho-Corasick reads it once.

It builds a tree of all the words, plus shortcuts that say "if this letter fails,
here is the longest partial word you are still inside". That is the same idea as
the table in section 2, generalised to a whole dictionary.

The bit people get wrong: when the machine finishes `she`, the text also ends
with `he` - and `he` might be on the list too. Both have to be reported.

```python
words = ["he", "she", "hers"]
text = "ushers"
for word in words:
    found = [i for i in range(len(text) - len(word) + 1)
             if text[i:i + len(word)] == word]
    print(f"{word:>5}: {found}")
```

Run it. `he` really is in there, hiding inside both of the others.

---

## 5. Predict before you run

`find_all("aaaa", "aa")` - how many matches? Write your answer down, then run
[`03_try_it_yourself.py`](03_try_it_yourself.py).

Most people say 2. The answer is 3, because matches are allowed to overlap.
Which answer *you* want is a decision you have to make on purpose.

---

## Where this shows up for real

`grep`, your editor's find-in-files, every spam filter, every intrusion detection
rule set, and DNA sequence alignment. When a log-scanning job that was fine in
testing takes six hours in production, it is usually this - a quadratic scan meeting
repetitive data.

**Next:** [`01_README.md`](01_README.md) for the mechanisms in full.
