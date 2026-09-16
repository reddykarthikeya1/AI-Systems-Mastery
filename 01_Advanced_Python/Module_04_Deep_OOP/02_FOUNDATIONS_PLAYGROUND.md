# 🐣 Interactive Foundations Playground: Object-Oriented Programming (OOP)

> *"A class is a cookie cutter; an object is the delicious cookie stamped out of it."*

Welcome to Module 04! If OOP has felt intimidating before, let's break it down in plain English.

---

## 1. What is a Class and an Object?

- **Class:** The architectural blueprint (e.g., the blueprint for a House).
- **Object (Instance):** The actual physical house built on Elm Street following that blueprint.
- **Attributes:** What the house *has* (color, number of bedrooms, price).
- **Methods:** What the house *does* (open door, ring doorbell).

---

## 2. The Minimal Class Example

```python
class Dog:
    def __init__(self, name, breed):
        # Setup: attach data to THIS specific dog:
        self.name = name
        self.breed = breed

    def bark(self):
        # A method (action):
        return f"{self.name} says Woof!"

# Create two independent dog objects:
dog1 = Dog("Buddy", "Golden Retriever")
dog2 = Dog("Milo", "Beagle")

print(dog1.bark())  # Buddy says Woof!
print(dog2.bark())  # Milo says Woof!
```

### Demystifying `self` in 10 Seconds:
Notice `def bark(self)`?
When you write `dog1.bark()`, Python secretly translates it into: `Dog.bark(dog1)`.
`self` simply stands for: *"Which specific dog are we talking about right now?"* In this case, `dog1`!

---

## 3. Inheritance: Reusing Code

Children inherit traits from parents:

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        return f"{self.name} is munching food."

# Dog inherits from Animal:
class Dog(Animal):
    def bark(self):
        return f"{self.name} says Woof!"

puppy = Dog("Charlie")
print(puppy.eat())   # Inherited from Animal!
print(puppy.bark())  # Specific to Dog!
```

---

## 4. Run the Interactive Playground
```bash
python 03_try_it_yourself.py
```
Create a bank account, deposit and withdraw virtual funds, and inspect class properties live!

---

## 5. Beginner Quick-Check Drills

### Drill 1: The Initializer Method
What special method runs automatically when a new object is created?
<details><summary><b>Show Answer</b></summary>
<b><code>__init__(self)</code></b> (The constructor/initializer method).
</details>

---

### Drill 2: Inheritance Syntax
How do you declare that class `Car` inherits from class `Vehicle`?
```python
class Car(___):
    pass
```
<details><summary><b>Show Answer</b></summary>

```python
class Car(Vehicle):
    pass
```
</details>

---

### Drill 3: Calling Methods
If `acc = BankAccount()`, how do you call its `deposit(50)` method?
<details><summary><b>Show Answer</b></summary>

```python
acc.deposit(50)
```
</details>\n