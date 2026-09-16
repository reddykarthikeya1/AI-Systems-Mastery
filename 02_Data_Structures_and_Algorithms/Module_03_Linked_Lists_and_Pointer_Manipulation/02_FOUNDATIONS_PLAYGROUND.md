# 🐣 Interactive Foundations Playground: Linked Lists

> *"Think of a Linked List like a treasure hunt: each clue tells you where to find the next clue."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---

## 1. What is a Node?
A Node is just a box with two compartments:
1. **Value**: The data you care about (e.g. `42`).
2. **Next**: An arrow pointing to the next box in memory.

```
[ 10 | next ] ---> [ 20 | next ] ---> [ 30 | None ]
```

---

## 2. Reversing a List (Turn the Arrows Around!)
Imagine 3 people holding hands facing forward. To turn around:
- Don't move the people!
- Just let go of your right hand and grab the hand behind you!

```
Before:  A ---> B ---> C
After:   A <--- B <--- C
```
