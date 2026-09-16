# 🐣 Interactive Foundations Playground: Environment & Tooling Basics

> *"The terminal is just a text chat where you type commands to your computer instead of clicking icons with a mouse."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

Welcome to your very first hands-on playground! In this guide, you will master the absolute basics of talking to your computer using terminal commands.

---

## 1. The 3 Essential Terminal Commands

Open PowerShell (Windows) or Terminal (macOS/Linux) and try these:

### Command 1: Where Am I?
- **Command:**
  ```bash
  # Windows PowerShell / Linux / Mac:
  pwd
  ```
- **What it stands for:** **P**rint **W**orking **D**irectory.
- **Output example:** `C:\Users\Alex\Projects` (Shows which folder you are currently inside).

---

### Command 2: What is in this Folder?
- **Command:**
  ```bash
  # Windows:
  dir
  # Mac/Linux or PowerShell:
  ls
  ```
- **What it stands for:** **L**i**s**t files / **Dir**ectory listing.
- **Output:** A list of every file and subfolder inside your current location.

---

### Command 3: Change to Another Folder
- **Command:**
  ```bash
  cd Module_00_Environment_Tooling_Workflow
  ```
- **What it stands for:** **C**hange **D**irectory.
- **How to go back up one folder:**
  ```bash
  cd ..
  ```
  *(Two dots `..` always means "the parent folder above me".)*

---

## 2. Checking Your Python Installation

Type this into your terminal:

```bash
python --version
```

### Expected Output:
```text
Python 3.11.x (or 3.12.x / 3.13.x)
```

> [!NOTE]
> If you get `'python' is not recognized as an internal or external command`:
> It means Python is not yet added to your system's PATH. Re-run the Python installer and ensure the box **"Add Python to PATH"** is checked!

---

## 3. Creating & Running Your Very First Python Script

1. Create a new text file named `hello.py`.
2. Type this single line inside it:
```python
print("I am officially a Python programmer!")
```
3. Save the file.
4. Run it in your terminal:
   ```bash
   python hello.py
   ```
5. You will see:
   ```text
   I am officially a Python programmer!
   ```

---

## 4. What is `pip`? (The App Store for Python)

Just like your phone has an App Store, Python has a global warehouse called **PyPI** (Python Package Index) with hundreds of thousands of free packages.

- To install a package:
  ```bash
  pip install rich
  ```
- To use it in Python:
```python
from rich import print
print("[bold green]This is colorful text![/bold green]")
```

---

## 5. Instant Interactive Sandbox: `03_try_it_yourself.py`

We have built a single-file, zero-dependency playground inside this folder!
Run it now:

```bash
python 03_try_it_yourself.py
```

It will detect your operating system, verify your Python version, and let you test your first interactive terminal program!

---

## 6. Beginner Self-Check Drills

### Drill 1: Checking Python Version
Which terminal command checks the version of Python installed on your computer?
```bash
python ___
```
<details><summary><b>Show Answer</b></summary>

```bash
python --version
```
</details>

---

### Drill 2: Running a Script
If your file is named `script.py`, what command runs it?
```bash
___ script.py
```
<details><summary><b>Show Answer</b></summary>

```bash
python script.py
```
</details>

---

### Drill 3: Going Up One Directory
Which command moves your terminal up to the parent directory?
```bash
cd ___
```
<details><summary><b>Show Answer</b></summary>

```bash
cd ..
```
</details>\n