# Troubleshooting & Edge Cases: Arrays & Strings

## Production Traps & Performance Pitfalls

### 1. Quadratic String Accumulation in Loops
```python
# ❌ ANTI-PATTERN: O(N^2) Time - copies entire string every iteration!
s = ""
for char in large_text:
    s += char

# ✅ PRODUCTION IDIOM: O(N) Time
buffer = []
for char in large_text:
    buffer.append(char)
s = "".join(buffer)
```

### 2. Modifying Array Length During Iteration
Modifying an array's length (`pop`, `insert`, `remove`) while iterating with an index or for-loop causes skipped elements or out-of-bounds crashes. Always iterate over a copy or use two-pointer in-place filtering.

### 3. Prefix Sum with Negative Integers
Do not use Sliding Window for problems like LeetCode 560 (*Subarray Sum Equals K*) when numbers can be negative. Sliding window requires monotonic sum growth. Use **Prefix Sum + Hash Map** instead.

### 4. Two Pointers Duplicate Handling
In problems like *3Sum*, failing to skip identical adjacent elements causes duplicate triplet outputs. Ensure pointer shifts bypass duplicates:
```python
while left < right and nums[left] == nums[left + 1]:
    left += 1
while left < right and nums[right] == nums[right - 1]:
    right -= 1
```
