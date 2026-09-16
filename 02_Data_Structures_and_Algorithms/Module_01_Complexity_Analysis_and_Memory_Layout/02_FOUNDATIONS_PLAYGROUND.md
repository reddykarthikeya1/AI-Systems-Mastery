# 🐣 Interactive Foundations Playground: Complexity & Bit Manipulation

> *"Bits are just 32 tiny light switches inside your computer. On (1) or Off (0)."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. What is Big-O in Plain English?

Imagine sending a 10 GB file:
- **Case A: Upload via Internet**. Takes 1 hour for 10 GB. Takes 10 hours for 100 GB. -> **$O(N)$ Linear Time**.
- **Case B: Mail a USB thumb drive**. Takes 24 hours to deliver 10 GB. Takes 24 hours to deliver 1,000 GB! -> **$O(1)$ Constant Time**.

For small files, internet is faster. For massive files, postal mail wins! That is Big-O: how time grows as $N$ gets huge.

---

## 2. Bit Tricks Every Programmer Must Know

```python
# Check if number is Odd or Even (Check the last light switch!)
num = 7
if num & 1:
    print("Odd number!")
else:
    print("Even number!")

# Multiply by 2 instantly using Left Shift (<<)
print(5 << 1)  # Output: 10

# Divide by 2 instantly using Right Shift (>>)
print(10 >> 1) # Output: 5
```

---

## 3. The Magic XOR Trick: The Cancelling Pair
```python
# XOR-ing the same number twice makes it vanish!
print(5 ^ 5)       # 0
print(0 ^ 42)      # 42
print(7 ^ 99 ^ 7)  # 99! (7 cancelled itself out!)
```
