# Beginner Playground - Designing a URL Shortener

> *"A cloakroom ticket. The ticket is short because it does not describe your coat - it just has to be unique, and the attendant has the list."*

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
import string
```

---

## 1. Start with the numbers, as always

Say 100 million new links a year, and each link is read about 100 times. That
ratio is the design: this is a read-heavy system, so the answer will be caching
and replicas, not clever write handling.

```python
new_links_per_year = 100_000_000
reads_per_link = 100
SECONDS_PER_YEAR = 31_500_000

write_qps = new_links_per_year / SECONDS_PER_YEAR
read_qps = write_qps * reads_per_link
print(f"writes: {write_qps:>8.0f} per second")
print(f"reads:  {read_qps:>8.0f} per second")
assert round(read_qps / write_qps) == 100
print("100:1 read-heavy. Cache the redirects and this is a small system.")
```

---

## 2. How short can the code be?

Base62 is the digits plus both cases: 62 characters. Seven of them give 62^7
combinations.

Do the arithmetic before choosing the length - it is the one decision that is
painful to change later, because every existing link keeps its old shape.

```python
ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase
assert len(ALPHABET) == 62

for length in (5, 6, 7, 8):
    combos = 62 ** length
    years = combos / new_links_per_year
    print(f"  {length} characters -> {combos:>20,} codes ({years:>12,.0f} years)")

assert 62 ** 7 > 3_500_000_000_000
print("7 characters is 3.5 trillion codes. Comfortably enough.")
```

---

## 3. Counter plus base62: no collisions, by construction

Take a number that only ever goes up and write it in base 62. Two different
numbers cannot produce the same string, so there is nothing to check and nothing
to retry.

Compare that with hashing the URL and taking the first 7 characters, which *can*
collide and therefore needs a database read on every single write to find out.

```python
def to_base62(number):
    if number == 0:
        return ALPHABET[0]
    out = []
    while number:
        number, remainder = divmod(number, 62)
        out.append(ALPHABET[remainder])
    return "".join(reversed(out))


def from_base62(code):
    value = 0
    for character in code:
        value = value * 62 + ALPHABET.index(character)
    return value


for counter in (1, 1_000, 125_000_000):
    code = to_base62(counter)
    print(f"  id {counter:>12,} -> /{code:<6} -> back to {from_base62(code):,}")
    assert from_base62(code) == counter

codes = {to_base62(i) for i in range(50_000)}
assert len(codes) == 50_000, "distinct counters give distinct codes, always"
```

---

## 4. Why hashing needs a round trip that counters do not

Truncate a hash to 7 characters and collisions become possible. Not likely - but
"unlikely" means you must check, and checking means a database read before every
insert.

Measure it on a deliberately short code so the effect is visible rather than
theoretical.

```python
def short_hash(url, length):
    digest = hashlib.sha256(url.encode()).digest()
    number = int.from_bytes(digest[:8], "big")
    return to_base62(number)[:length]


urls = [f"https://example.com/{i}" for i in range(100_000)]
hashed = {}
collisions = 0
for url in urls:
    code = short_hash(url, length=4)
    if code in hashed and hashed[code] != url:
        collisions += 1
    hashed[code] = url

print(f"100,000 URLs into 4-character hashed codes -> {collisions:,} collisions")
assert collisions > 0, "which is why every write must check first"
print("The counter approach needs no check at all. That is the argument for it.")
```

---

## 5. The last two decisions

**301 or 302?** A 301 is permanent, so browsers and proxies cache it and you never
see the click again. A 302 costs you a request every time - and gives you the
analytics. Almost every shortener chooses 302 for exactly that reason.

**How do you scale the counter?** One global counter is the bottleneck you were
avoiding. Hand out *ranges* instead: each server claims a block of a million ids
in one coordination step, then issues from it locally.

```python
class IdRangeAllocator:
    def __init__(self, block=1_000_000):
        self.next_block_start = 1
        self.block = block
        self.coordination_calls = 0

    def claim(self):
        self.coordination_calls += 1
        start = self.next_block_start
        self.next_block_start += self.block
        return range(start, start + self.block)


allocator = IdRangeAllocator()
server_a, server_b = allocator.claim(), allocator.claim()
issued = 2_000_000

print(f"ids available without further coordination: {len(server_a) + len(server_b):,}")
print(f"coordination round trips used: {allocator.coordination_calls}")
assert set(server_a) & set(server_b) == set(), "ranges cannot overlap"
assert allocator.coordination_calls == 2, f"2 calls for {issued:,} ids"
```

---

## 6. Predict before you run

Using lowercase, uppercase and digits, how many distinct 7-character codes
exist? Is that enough for a service issuing a million links a day for ten
years?

Write your answer down first. Being wrong here is the point - a prediction you
had to correct is remembered; a paragraph you agreed with is not.

---

## Where this shows up for real

This is the most common first system design interview question, and the
interesting part is never the hashing. It is the read:write ratio - roughly
100:1 - which tells you the whole architecture before you draw a single box.

**Next:** [`01_README.md`](01_README.md) covers the same ideas with production
detail. When you want to practise diagnosing rather than building, the planted
bugs are in [`debug_lab/SYMPTOMS.md`](debug_lab/SYMPTOMS.md).
