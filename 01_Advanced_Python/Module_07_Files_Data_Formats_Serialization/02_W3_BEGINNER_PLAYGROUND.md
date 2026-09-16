# 🐣 W3Schools-Style Playground: Files & Data Serialization

> *"Files are how your program remembers information after you turn off your computer."*

Welcome to Module 07! Let's learn how to read and write text files and JSON data with ease.

---

## 1. Reading and Writing Text Files

Always use the `with` statement so Python automatically closes the file for you:

### Writing to a File (`"w"` mode):
```python
with open("groceries.txt", "w", encoding="utf-8") as f:
    f.write("Apples\n")
    f.write("Bananas\n")
    f.write("Oat Milk\n")
```

### Reading from a File (`"r"` mode):
```python
with open("groceries.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
```

---

## 2. Working with JSON (The Language of the Web)

JSON looks almost identical to Python dictionaries! Use the `json` module:

```python
import json

student_record = {
    "name": "Sarah",
    "gpa": 3.92,
    "courses": ["Algorithms", "Python", "Databases"]
}

# 1. Convert dictionary to JSON string:
json_string = json.dumps(student_record, indent=2)
print(json_string)

# 2. Save dictionary directly to a JSON file:
with open("student.json", "w", encoding="utf-8") as f:
    json.dump(student_record, f, indent=2)

# 3. Read JSON file back into Python dictionary:
with open("student.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)
    print("Loaded Name:", loaded_data["name"])
```

---

## 3. Run the Interactive Playground
```bash
python 03_try_it_yourself.py
```
Try an interactive digital notepad that saves notes to disk and loads them back!

---

## 4. Beginner Quick-Check Drills

### Drill 1: Appending to a File
What file mode flag appends text to the end of an existing file without overwriting it?
```python
with open("log.txt", "___") as f:
    f.write("New entry\n")
```
<details><summary><b>Show Answer</b></summary>
<b><code>"a"</code></b> (for <b>a</b>ppend mode. <code>"w"</code> overwrites the entire file!).
</details>

---

### Drill 2: Parsing JSON Strings
Which function converts a raw JSON text string into a Python dictionary?
```python
import json
data = json.___(raw_json_string)
```
<details><summary><b>Show Answer</b></summary>
<b><code>json.loads()</code></b> (Load <b>S</b>tring).
</details>\n