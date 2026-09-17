# 🐣 Interactive Foundations Playground: Complexity Analysis & Bit Manipulation

> *"Bits are just 32 tiny light switches inside your computer. On (1) or Off (0)."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import math
```

---

## 1. Bitwise Parity and Power of Two Invariant

Checking if a number is odd or even takes a single bit check on the lowest bit ($n \ \& \ 1$). A power of two in binary has exactly one bit set; subtracting 1 flips all lower bits, so $n \ \& \ (n - 1) == 0$.

```python
val = 16
is_even = (val & 1) == 0
assert is_even is True, "16 must be even"

is_power_of_two = (val > 0) and ((val & (val - 1)) == 0)
assert is_power_of_two is True, "16 is 2^4"
assert ((15 & 14) == 0) is False, "15 is not a power of two"
print(f"val={val}: is_even={is_even}, is_power_of_two={is_power_of_two}")
```

---

## 2. Fast Multiplication and Division via Bit Shifts

Left shift (`<<`) doubles an integer in 1 clock cycle. Right shift (`>>`) halves an integer discarding fractions.

```python
base = 7
doubled = base << 1
halved = base >> 1
assert doubled == 14
assert halved == 3
assert (1 << 10) == 1024, "2^10 must equal 1024"
print(f"base={base}: doubled={doubled}, halved={halved}, 2^10={1 << 10}")
```

---

## 3. The Self-Cancelling XOR Invariant

For any integer $x$, $x \oplus x = 0$ and $x \oplus 0 = x$. XOR is commutative and associative, so duplicate pairs cancel completely leaving only the lone unique item.

```python
nums = [4, 1, 2, 1, 2]
unique = 0
for x in nums:
    unique ^= x

assert unique == 4, "4 is the only unpaired number"
assert (99 ^ 99) == 0
assert (0 ^ 42) == 42
print(f"Array {nums} isolated unique element: {unique}")
```

---
