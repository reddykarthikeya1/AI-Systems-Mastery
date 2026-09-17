# 🐣 Interactive Foundations Playground: Dynamic Programming (1D)

> *"Dynamic Programming is just remembering the past so you don't repeat your mistakes."*


> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

---


## Interactive Algorithm Trace Scrubber

```trace
{
  "title": "Kadane's Algorithm Maximum Subarray Sum",
  "algorithm": "Dynamic Programming: Kadane",
  "timeComplexity": "O(n)",
  "spaceComplexity": "O(1)",
  "frames": [
    {
      "step": 1,
      "description": "Index 0: val = -2. currentMax = -2, globalMax = -2.",
      "array": [-2, 1, -3, 4, -1, 2, 1, -5, 4],
      "pointers": { "i": 0 },
      "highlights": { "0": "active" },
      "variables": { "num": -2, "currentMax": -2, "globalMax": -2 },
      "invariants": "Initialize Kadane window with first element"
    },
    {
      "step": 2,
      "description": "Index 1: val = 1. max(1, -2 + 1) = 1. Reset window! globalMax = 1.",
      "array": [-2, 1, -3, 4, -1, 2, 1, -5, 4],
      "pointers": { "i": 1 },
      "highlights": { "1": "sorted" },
      "variables": { "num": 1, "currentMax": 1, "globalMax": 1 },
      "invariants": "Starting new subarray at index 1 is strictly better than extending -2"
    },
    {
      "step": 3,
      "description": "Index 3 to 6: Accumulated contiguous sum [4, -1, 2, 1] = 6.",
      "array": [-2, 1, -3, 4, -1, 2, 1, -5, 4],
      "pointers": { "start": 3, "end": 6 },
      "highlights": { "3": "sorted", "4": "sorted", "5": "sorted", "6": "sorted" },
      "variables": { "subArraySum": 6, "globalMax": 6 },
      "invariants": "Max contiguous subarray sum identified: 6 (indices [3..6])"
    }
  ]
}
```

## 1. What is DP? (The 1 + 1 + 1 Story)
- Write on a paper: `1 + 1 + 1 + 1 + 1 = 5`.
- Ask a friend: *"What does that equal?"* They count: *"Five!"*
- Add another `+ 1` to the end.
- Ask: *"What does it equal now?"*
- They answer instantly: *"Six!"*
- How did they know? **They didn't recount from scratch. They remembered it was 5 and added 1!** That is DP.