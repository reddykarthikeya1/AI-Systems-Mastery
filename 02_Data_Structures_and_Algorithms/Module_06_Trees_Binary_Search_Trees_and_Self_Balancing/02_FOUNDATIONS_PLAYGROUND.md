# 🐣 Interactive Foundations Playground: Binary Trees

> *"A binary tree is like a family tree turned upside down, where every parent has at most 2 children."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---


## Interactive Algorithm Trace Scrubber

```trace
{
  "title": "Binary Search Tree Key Insertion & Rebalance",
  "algorithm": "BST Search and Traversal",
  "timeComplexity": "O(log n)",
  "spaceComplexity": "O(1)",
  "frames": [
    {
      "step": 1,
      "description": "Root node comparison: Target 25 vs Root 30.",
      "array": [30, 15, 45, 10, 25, 35, 60],
      "pointers": { "curr": 0 },
      "highlights": { "0": "comparing" },
      "variables": { "currKey": 30, "target": 25, "direction": "left" },
      "invariants": "25 < 30: Traverse to left child (index 1)"
    },
    {
      "step": 2,
      "description": "Compare Target 25 with Left Child 15.",
      "array": [30, 15, 45, 10, 25, 35, 60],
      "pointers": { "curr": 1 },
      "highlights": { "1": "comparing" },
      "variables": { "currKey": 15, "target": 25, "direction": "right" },
      "invariants": "25 > 15: Traverse to right child of 15 (index 4)"
    },
    {
      "step": 3,
      "description": "Compare Target 25 with Node 25: Target Matched!",
      "array": [30, 15, 45, 10, 25, 35, 60],
      "pointers": { "curr": 4 },
      "highlights": { "4": "sorted" },
      "variables": { "currKey": 25, "target": 25, "found": true },
      "invariants": "Exact key hit at node 25 in 3 comparisons"
    }
  ]
}
```

## 1. What is a Binary Search Tree (BST)?
A tree where for EVERY node:
- Everything to the **LEFT** is **SMALLER**.
- Everything to the **RIGHT** is **BIGGER**.

```
         ( 8 )
        /     \
     ( 3 )   ( 10 )
     /   \        \
   ( 1 ) ( 6 )    ( 14 )
```