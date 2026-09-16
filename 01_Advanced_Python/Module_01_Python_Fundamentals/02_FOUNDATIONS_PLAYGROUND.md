# 🐣 Interactive Foundations Playground: Python Fundamentals

> *"A variable is just a name tag stuck on an object in your computer's memory."*

Welcome to the Module 01 Playground! Here we explore variables, data types, math, decisions (`if`/`else`), and loops through bite-sized examples.

---

## 1. Variables and Data Types in 30 Seconds

```python
# Integer (whole number)
age = 25

# Float (decimal number)
height = 1.75

# String (text)
name = "Taylor"

# Boolean (True or False)
is_student = True
```

### Line-by-Line Breakdown:
- `age = 25`: Python creates the number `25` in memory and sticks the name tag `age` onto it.
- `=` is the **assignment operator**. It copies the right side into the left name tag.
- Variable names should use `snake_case` (lowercase letters separated by underscores).

---

## 2. Common Math Operators

```python
x = 10
y = 3

print(x + y)   # 13  (Add)
print(x - y)   # 7   (Subtract)
print(x * y)   # 30  (Multiply)
print(x / y)   # 3.3333333333333335 (True Float Division)
print(x // y)  # 3   (Floor Division: drops the decimal remainder!)
print(x % y)   # 1   (Modulo: remainder when 10 is divided by 3)
print(x ** y)  # 1000 (Exponent: 10 * 10 * 10)
```

---

## 3. String Formatting with f-Strings

Instead of ugly string additions like `"Hello " + name + "!"`, always use modern **f-strings**:

```python
item = "Espresso"
price = 3.50
quantity = 2

# Put an 'f' before the quote, and put variables inside {}:
bill = f"You ordered {quantity}x {item} for a total of ${quantity * price:.2f}."
print(bill)
# Output: You ordered 2x Espresso for a total of $7.00.
```

---

## 4. Making Decisions (`if`, `elif`, `else`)

```python
temperature = 28

if temperature > 30:
    print("It's scorching hot!")
elif temperature >= 20:
    print("The weather is pleasant.")
else:
    print("It's chilly, bring a jacket!")
```

> [!WARNING]
> **Don't Forget the Colon `:`**  
> Every `if`, `elif`, and `else` line MUST end with a colon `:`. The next line MUST be indented with 4 spaces!

---

## 5. Repeating Actions: Loops

### The `for` Loop (Counted Repetitions)
```python
# range(1, 6) counts: 1, 2, 3, 4, 5 (stops BEFORE 6!)
for step in range(1, 6):
    print(f"Pushup #{step}")
```

### The `while` Loop (Condition-Based)
```python
fuel = 3
while fuel > 0:
    print(f"Driving... Fuel remaining: {fuel}")
    fuel -= 1

print("Out of gas!")
```

---

## 6. Run the Interactive Playground
Launch the standalone terminal script right now:
```bash
python 03_try_it_yourself.py
```
It includes a live temperature converter and a guess-the-number game you can play directly!

---

## 7. Beginner Quick-Check Drills

### Drill 1: Remainder Math
What is the output of `print(14 % 4)`?
<details><summary><b>Show Answer</b></summary>
<b>2</b> (Because 4 fits into 14 three times (12), with a remainder of 2).
</details>

---

### Drill 2: String to Float Conversion
Convert the text `"19.99"` into a real decimal float:
```python
price = ___("19.99")
```
<details><summary><b>Show Answer</b></summary>

```python
price = float("19.99")
```
</details>

---

### Drill 3: Modulo Even/Odd Check
How do you check if a number `n` is even?
```python
if n % 2 ___ 0:
    print("Even!")
```
<details><summary><b>Show Answer</b></summary>

```python
if n % 2 == 0:
    print("Even!")
```
</details>\n