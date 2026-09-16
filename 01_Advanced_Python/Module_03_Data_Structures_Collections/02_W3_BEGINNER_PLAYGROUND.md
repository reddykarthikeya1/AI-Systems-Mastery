# 🐣 W3Schools-Style Playground: Data Structures & Collections

> *"Choosing the right collection is like choosing the right container: use a list for a shopping list, a dictionary for a phone book, and a set for unique tags."*

Welcome to Module 03! In this playground, you will master the 4 built-in Python collections.

---

## 1. Quick Summary of the 4 Collections

| Collection | Syntax | Ordered? | Changeable (Mutable)? | Allows Duplicates? |
| :--- | :---: | :---: | :---: | :---: |
| **List** | `["a", "b"]` | ✅ Yes | ✅ Yes | ✅ Yes |
| **Tuple** | `("a", "b")` | ✅ Yes | ❌ No (Locked) | ✅ Yes |
| **Set** | `{"a", "b"}` | ❌ No | ✅ Yes | ❌ No (Unique only!) |
| **Dictionary** | `{"key": "value"}`| ✅ Yes | ✅ Yes | Keys must be unique |

---

## 2. Lists in Action

```python
tasks = ["Email boss", "Buy milk", "Walk dog"]

# Add to the end:
tasks.append("Schedule dentist")

# Remove an item:
tasks.remove("Buy milk")

# Access by index (starts at 0!):
print(tasks[0])   # "Email boss"
print(tasks[-1])  # "Schedule dentist" (negative index means from the end!)

# Length:
print(len(tasks)) # 3
```

---

## 3. Dictionaries in Action

A dictionary stores pairs of **Keys** and **Values**:

```python
user = {
    "name": "Jordan",
    "email": "jordan@example.com",
    "role": "Admin"
}

# 1. Look up value:
print(user["name"])  # Output: Jordan

# 2. Safe look up with .get() (never crashes on missing key!):
phone = user.get("phone", "Not Provided")
print(phone)  # Output: Not Provided

# 3. Add or update a key:
user["status"] = "Active"
```

---

## 4. Sets in Action (Deduplication)

Need to remove duplicates from a list in 1 line? Cast it to a `set`!

```python
emails = ["a@corp.com", "b@corp.com", "a@corp.com", "c@corp.com"]
unique_emails = list(set(emails))
print(unique_emails)
# Output: ['a@corp.com', 'b@corp.com', 'c@corp.com']
```

---

## 5. Run the Interactive Playground
```bash
python 03_try_it_yourself.py
```
Try managing an interactive task list and querying a mock user dictionary!

---

## 6. Beginner Quick-Check Drills

### Drill 1: Negative Indexing
What does `colors[-1]` return for `colors = ["red", "green", "blue"]`?
<details><summary><b>Show Answer</b></summary>
<b><code>"blue"</code></b> (Index <code>-1</code> always gets the very last item in a sequence).
</details>

---

### Drill 2: Dictionary Safe Access
Why is `dict.get("key")` safer than `dict["key"]`?
<details><summary><b>Show Answer</b></summary>
Because <code>dict["missing"]</code> crashes with a <b>KeyError</b>, while <code>dict.get("missing")</code> safely returns <b>None</b> (or a custom default).
</details>

---

### Drill 3: Adding to a Set
Which method adds a single item to a set?
```python
my_set = {1, 2}
my_set.___(3)
```
<details><summary><b>Show Answer</b></summary>

```python
my_set.add(3)  # Lists use .append(), Sets use .add()!
```
</details>\n