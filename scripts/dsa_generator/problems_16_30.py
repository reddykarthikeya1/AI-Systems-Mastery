from .models import Problem

def get_problems_16_30() -> list[Problem]:
    problems = []

    # ----------------------------------------------------
    # Problem 16: Minimum Window Substring
    # ----------------------------------------------------
    def trace_p16():
        s, t = "ADOBECODEBANC", "ABC"
        need = {}
        for c in t:
            need[c] = need.get(c, 0) + 1
        have = {}
        matched = 0
        left = 0
        min_len = float("inf")
        best = ""
        out = [
            f"Input: s = '{s}', t = '{t}'",
            f"Required characters: {need}",
            f"{'right':<5} | {'char':<5} | {'matched':<8} | {'left':<5} | {'Window':<15} | {'Action':<25}",
            "-" * 70
        ]
        for right, char in enumerate(s):
            have[char] = have.get(char, 0) + 1
            if char in need and have[char] == need[char]:
                matched += 1
            while matched == len(need):
                if (right - left + 1) < min_len:
                    min_len = right - left + 1
                    best = s[left : right + 1]
                out.append(f"{right:<5} | '{char}'   | {matched:<8} | {left:<5} | '{s[left:right+1]}' | Shrink left (best: '{best}')")
                have[s[left]] -= 1
                if s[left] in need and have[s[left]] < need[s[left]]:
                    matched -= 1
                left += 1
        out.append(f"Resulting minimum window: '{best}'")
        return "\n".join(out)

    problems.append(Problem(
        id=16,
        slug="p16_minimum_window_substring",
        title="Minimum Window Substring",
        category="Sliding Window",
        difficulty="Hard",
        statement="Given two strings `s` and `t` of lengths $m$ and $n$ respectively, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If no such substring exists, return empty string `\"\"`.",
        brute_force="Examine every substring of $s$ ($O(N^2)$) and check if it contains all characters of $t$ in required frequencies ($O(N)$). Time: $O(N^3)$, Space: $O(M)$.",
        key_insight="Maintain required counts `need` and current window counts `have`. Keep a count `matched` of how many distinct characters satisfy their requirement. Expand `right` until `matched == len(need)`, then greedily contract `left` while maintaining validity.",
        func_name="min_window",
        stub_code="""def min_window(s: str, t: str) -> str:
    \"\"\"Finds minimum window substring of s containing all characters of t.
    
    Time: O(M + N), Space: O(M + N)
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def min_window(s: str, t: str) -> str:
    \"\"\"Finds minimum window substring of s containing all characters of t.
    
    Time: O(M + N), Space: O(M + N)
    \"\"\"
    if not s or not t:
        return ""
        
    need: dict[str, int] = {}
    for c in t:
        need[c] = need.get(c, 0) + 1
        
    have: dict[str, int] = {}
    matched = 0
    left = 0
    min_len = float("inf")
    res_indices = (-1, -1)
    
    for right in range(len(s)):
        char = s[right]
        have[char] = have.get(char, 0) + 1
        
        if char in need and have[char] == need[char]:
            matched += 1
            
        while matched == len(need):
            if (right - left + 1) < min_len:
                min_len = right - left + 1
                res_indices = (left, right)
                
            left_char = s[left]
            have[left_char] -= 1
            if left_char in need and have[left_char] < need[left_char]:
                matched -= 1
            left += 1
            
    l, r = res_indices
    return s[l : r + 1] if min_len != float("inf") else ""
""",
        tests_code="""assert min_window("ADOBECODEBANC", "ABC") == "BANC"
assert min_window("a", "a") == "a"
assert min_window("a", "aa") == ""
assert min_window("ab", "b") == "b"
""",
        time_complexity="$O(M + N)$ where $M = \\text{len}(s)$ and $N = \\text{len}(t)$. Each character is visited at most twice.",
        space_complexity="$O(M + N)$ to store character frequency maps.",
        follow_up="What if $s$ contains billions of characters and can only be streamed? Keep only the filtered indices and characters that appear in $t$, reducing memory footprint to $O(N)$.",
        run_trace=trace_p16
    ))

    # ----------------------------------------------------
    # Problem 17: Valid Parentheses
    # ----------------------------------------------------
    def trace_p17():
        s = "()[]{}"
        stack = []
        matching = {')': '(', '}': '{', ']': '['}
        out = [
            f"Input: '{s}'",
            f"{'Step':<5} | {'char':<5} | {'Action':<15} | {'Stack state':<15}",
            "-" * 45
        ]
        valid = True
        for i, ch in enumerate(s):
            if ch in "({[":
                stack.append(ch)
                out.append(f"{i+1:<5} | '{ch}'   | Push open       | {str(stack):<15}")
            else:
                if not stack or stack[-1] != matching[ch]:
                    valid = False
                    out.append(f"{i+1:<5} | '{ch}'   | Mismatch!       | {str(stack):<15}")
                    break
                stack.pop()
                out.append(f"{i+1:<5} | '{ch}'   | Pop match       | {str(stack):<15}")
        out.append(f"Is valid: {valid and len(stack) == 0}")
        return "\n".join(out)

    problems.append(Problem(
        id=17,
        slug="p17_valid_parentheses",
        title="Valid Parentheses",
        category="Stack",
        difficulty="Easy",
        statement="Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.",
        brute_force="Repeatedly replace occurrences of `\"()\"`, `\"[]\"`, and `\"{}\"` with `\"\"` until no more replacements are possible. Time: $O(N^2)$, Space: $O(N)$.",
        key_insight="A LIFO stack matches the most recently opened bracket with the next closing bracket. Push opening brackets; on closing brackets, pop and check if it matches.",
        func_name="is_valid_parentheses",
        stub_code="""def is_valid_parentheses(s: str) -> bool:
    \"\"\"Checks if bracket sequence is properly nested and closed.
    
    Time: O(N), Space: O(N)
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def is_valid_parentheses(s: str) -> bool:
    \"\"\"Checks if bracket sequence is properly nested and closed.
    
    Time: O(N), Space: O(N)
    \"\"\"
    stack: list[str] = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
            
    return not stack
""",
        tests_code="""assert is_valid_parentheses("()") is True
assert is_valid_parentheses("()[]{}") is True
assert is_valid_parentheses("(]") is False
assert is_valid_parentheses("([)]") is False
assert is_valid_parentheses("{[]}") is True
""",
        time_complexity="$O(N)$ single pass across length $N$.",
        space_complexity="$O(N)$ to hold opening brackets on stack in worst case.",
        follow_up="What if brackets include wildcards like `*` which can be `'('`, `')'`, or empty? Use two counters for minimum and maximum possible open bracket counts (Greedy Range Tracking).",
        run_trace=trace_p17
    ))

    # ----------------------------------------------------
    # Problem 18: Daily Temperatures
    # ----------------------------------------------------
    def trace_p18():
        temps = [73, 74, 75, 71, 69, 72, 76, 73]
        stack = []
        res = [0] * len(temps)
        out = [
            f"Input: {temps}",
            f"{'i':<3} | {'temp':<5} | {'Stack [(idx, temp)]':<25} | {'Popped idx & wait time':<25}",
            "-" * 65
        ]
        for i, t in enumerate(temps):
            popped_actions = []
            while stack and temps[stack[-1]] < t:
                prev_i = stack.pop()
                res[prev_i] = i - prev_i
                popped_actions.append(f"idx {prev_i} waited {res[prev_i]}d")
            stack.append(i)
            action_str = ", ".join(popped_actions) if popped_actions else "None"
            stack_repr = str([(idx, temps[idx]) for idx in stack])
            out.append(f"{i:<3} | {t:<5} | {stack_repr:<25} | {action_str:<25}")
        out.append(f"Result: {res}")
        return "\n".join(out)

    problems.append(Problem(
        id=18,
        slug="p18_daily_temperatures",
        title="Daily Temperatures",
        category="Stack",
        difficulty="Medium",
        statement="Given an array of integers `temperatures` represents the daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the $i^{\\text{th}}$ day to get a warmer temperature. If there is no future day for which this is possible, keep `answer[i] == 0`.",
        brute_force="For each day $i$, scan ahead $j = i+1 \\dots N$ until finding a higher temperature. Time: $O(N^2)$, Space: $O(1)$.",
        key_insight="Maintain a **Monotonic Decreasing Stack** storing indices of unresolved cold days. When today's temperature is warmer than the top of the stack, pop and record the elapsed days.",
        func_name="daily_temperatures",
        stub_code="""def daily_temperatures(temperatures: list[int]) -> list[int]:
    \"\"\"Calculates days until warmer temperature using monotonic stack.
    
    Time: O(N), Space: O(N)
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def daily_temperatures(temperatures: list[int]) -> list[int]:
    \"\"\"Calculates days until warmer temperature using monotonic stack.
    
    Time: O(N), Space: O(N)
    \"\"\"
    n = len(temperatures)
    res = [0] * n
    stack: list[int] = []  # Stores indices
    
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            prev_i = stack.pop()
            res[prev_i] = i - prev_i
        stack.append(i)
        
    return res
""",
        tests_code="""assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
assert daily_temperatures([30, 60, 90]) == [1, 1, 0]
assert daily_temperatures([]) == []
""",
        time_complexity="$O(N)$ linear time; every index is pushed and popped at most once.",
        space_complexity="$O(N)$ auxiliary space for the stack.",
        follow_up="Can this be solved in $O(1)$ extra space? Iterate backwards from the end of the array, using the already-computed answers to jump forward.",
        run_trace=trace_p18
    ))

    # ----------------------------------------------------
    # Problem 19: Largest Rectangle in Histogram
    # ----------------------------------------------------
    def trace_p19():
        heights = [2, 1, 5, 6, 2, 3]
        stack = []
        max_area = 0
        h_ext = heights + [0]
        out = [
            f"Input heights: {heights} (with appended sentinel 0: {h_ext})",
            f"{'i':<3} | {'h[i]':<5} | {'Stack [(idx, h)]':<22} | {'Popped & Evaluated Area':<30}",
            "-" * 65
        ]
        for i, h in enumerate(h_ext):
            evals = []
            while stack and stack[-1][1] > h:
                idx, height = stack.pop()
                width = i if not stack else (i - stack[-1][0] - 1)
                area = height * width
                max_area = max(max_area, area)
                evals.append(f"h={height}*w={width}->area={area}")
            stack.append((i, h))
            eval_str = ", ".join(evals) if evals else "None"
            out.append(f"{i:<3} | {h:<5} | {str(stack):<22} | {eval_str:<30}")
        out.append(f"Maximum Rectangle Area: {max_area}")
        return "\n".join(out)

    problems.append(Problem(
        id=19,
        slug="p19_largest_rectangle_in_histogram",
        title="Largest Rectangle in Histogram",
        category="Stack",
        difficulty="Hard",
        statement="Given an array of integers `heights` representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.",
        brute_force="For each pair of bars $(i, j)$, find the minimum height between them and multiply by $(j - i + 1)$. Time: $O(N^2)$, Space: $O(1)$.",
        key_insight="Maintain a **Monotonic Increasing Stack** of `(index, height)`. When a shorter bar is encountered, pop previous bars because they cannot extend further right. The popped bar's width extends between the current index and the new stack top.",
        func_name="largest_rectangle_area",
        stub_code="""def largest_rectangle_area(heights: list[int]) -> int:
    \"\"\"Computes maximum rectangle area using a monotonic increasing stack.
    
    Time: O(N), Space: O(N)
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def largest_rectangle_area(heights: list[int]) -> int:
    \"\"\"Computes maximum rectangle area using a monotonic increasing stack.
    
    Time: O(N), Space: O(N)
    \"\"\"
    stack: list[tuple[int, int]] = []  # (index, height)
    max_area = 0
    
    for i, h in enumerate(heights):
        start = i
        while stack and stack[-1][1] > h:
            idx, height = stack.pop()
            max_area = max(max_area, height * (i - idx))
            start = idx
        stack.append((start, h))
        
    for idx, height in stack:
        max_area = max(max_area, height * (len(heights) - idx))
        
    return max_area
""",
        tests_code="""assert largest_rectangle_area([2, 1, 5, 6, 2, 3]) == 10
assert largest_rectangle_area([2, 4]) == 4
assert largest_rectangle_area([1]) == 1
assert largest_rectangle_area([]) == 0
""",
        time_complexity="$O(N)$ linear time; each bar is pushed and popped at most once.",
        space_complexity="$O(N)$ stack memory.",
        follow_up="How to solve Maximal Rectangle in a 2D binary matrix? Convert each row into a histogram of consecutive 1s and run this algorithm row-by-row in $O(R \\cdot C)$.",
        run_trace=trace_p19
    ))

    # ----------------------------------------------------
    # Problem 20: Binary Search
    # ----------------------------------------------------
    def trace_p20():
        nums, target = [-1, 0, 3, 5, 9, 12], 9
        l, r = 0, len(nums) - 1
        out = [
            f"Input: nums = {nums}, target = {target}",
            f"{'Step':<5} | {'left':<5} | {'right':<5} | {'mid':<5} | {'nums[mid]':<10} | {'Action':<15}",
            "-" * 55
        ]
        step = 1
        while l <= r:
            mid = l + (r - l) // 2
            if nums[mid] == target:
                out.append(f"{step:<5} | {l:<5} | {r:<5} | {mid:<5} | {nums[mid]:<10} | Target found at {mid}!")
                break
            elif nums[mid] < target:
                out.append(f"{step:<5} | {l:<5} | {r:<5} | {mid:<5} | {nums[mid]:<10} | mid < target -> l = mid+1")
                l = mid + 1
            else:
                out.append(f"{step:<5} | {l:<5} | {r:<5} | {mid:<5} | {nums[mid]:<10} | mid > target -> r = mid-1")
                r = mid - 1
            step += 1
        return "\n".join(out)

    problems.append(Problem(
        id=20,
        slug="p20_binary_search",
        title="Binary Search",
        category="Binary Search",
        difficulty="Easy",
        statement="Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return `-1`.",
        brute_force="Linear scan through the array. Time: $O(N)$, Space: $O(1)$.",
        key_insight="Because the array is sorted, comparing `target` with the midpoint `mid` eliminates half the remaining search space on every iteration.",
        func_name="binary_search",
        stub_code="""def binary_search(nums: list[int], target: int) -> int:
    \"\"\"Searches for target in sorted nums in O(log N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def binary_search(nums: list[int], target: int) -> int:
    \"\"\"Searches for target in sorted nums in O(log N) time.\"\"\"
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1
""",
        tests_code="""assert binary_search([-1, 0, 3, 5, 9, 12], 9) == 4
assert binary_search([-1, 0, 3, 5, 9, 12], 2) == -1
assert binary_search([5], 5) == 0
assert binary_search([], 3) == -1
""",
        time_complexity="$O(\\log N)$ logarithmic time.",
        space_complexity="$O(1)$ constant auxiliary space.",
        follow_up="Why write `mid = left + (right - left) // 2` instead of `(left + right) // 2`? To avoid 32-bit integer overflow in languages like C++/Java when `left + right > 2^{31} - 1`.",
        run_trace=trace_p20
    ))

    # ----------------------------------------------------
    # Problem 21: Search in Rotated Sorted Array
    # ----------------------------------------------------
    def trace_p21():
        nums, target = [4, 5, 6, 7, 0, 1, 2], 0
        l, r = 0, len(nums) - 1
        out = [
            f"Input: nums = {nums}, target = {target}",
            f"{'Step':<5} | {'left':<5} | {'right':<5} | {'mid':<5} | {'nums[mid]':<10} | {'Sorted Half':<15} | {'Action':<15}",
            "-" * 70
        ]
        step = 1
        while l <= r:
            mid = l + (r - l) // 2
            if nums[mid] == target:
                out.append(f"{step:<5} | {l:<5} | {r:<5} | {mid:<5} | {nums[mid]:<10} | -               | Found index {mid}!")
                break
            if nums[l] <= nums[mid]:
                half = "Left [l..mid]"
                if nums[l] <= target < nums[mid]:
                    action = "r = mid - 1"
                    r = mid - 1
                else:
                    action = "l = mid + 1"
                    l = mid + 1
            else:
                half = "Right [mid..r]"
                if nums[mid] < target <= nums[r]:
                    action = "l = mid + 1"
                    l = mid + 1
                else:
                    action = "r = mid - 1"
                    r = mid - 1
            out.append(f"{step:<5} | {l:<5} | {r:<5} | {mid:<5} | {nums[mid]:<10} | {half:<15} | {action:<15}")
            step += 1
        return "\n".join(out)

    problems.append(Problem(
        id=21,
        slug="p21_search_in_rotated_sorted_array",
        title="Search in Rotated Sorted Array",
        category="Binary Search",
        difficulty="Medium",
        statement="There is an integer array `nums` sorted in ascending order (with distinct values), rotated at an unknown pivot index. Given `nums` and a `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.",
        brute_force="Linear search $O(N)$ across all elements. Space: $O(1)$.",
        key_insight="In any rotated sorted array, splitting at `mid` always leaves at least one half strictly sorted. Determine which half is sorted, check if `target` lies within that half's boundary, and bisect accordingly in $O(\\log N)$.",
        func_name="search_rotated",
        stub_code="""def search_rotated(nums: list[int], target: int) -> int:
    \"\"\"Searches for target in rotated sorted array in O(log N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def search_rotated(nums: list[int], target: int) -> int:
    \"\"\"Searches for target in rotated sorted array in O(log N) time.\"\"\"
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
            
        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
                
    return -1
""",
        tests_code="""assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1
assert search_rotated([1], 0) == -1
assert search_rotated([1, 3], 3) == 1
""",
        time_complexity="$O(\\log N)$ time logarithmic search.",
        space_complexity="$O(1)$ auxiliary memory.",
        follow_up="What if duplicate elements are allowed? Worst case degrades to $O(N)$ when `nums[left] == nums[mid] == nums[right]` because neither half can be guaranteed sorted.",
        run_trace=trace_p21
    ))

    # ----------------------------------------------------
    # Problem 22: Find Minimum in Rotated Sorted Array
    # ----------------------------------------------------
    def trace_p22():
        nums = [4, 5, 6, 7, 0, 1, 2]
        l, r = 0, len(nums) - 1
        out = [
            f"Input: nums = {nums}",
            f"{'Step':<5} | {'left':<5} | {'right':<5} | {'mid':<5} | {'nums[mid]':<10} | {'nums[right]':<12} | {'Action':<15}",
            "-" * 65
        ]
        step = 1
        while l < r:
            mid = l + (r - l) // 2
            if nums[mid] > nums[r]:
                action = "l = mid + 1 (inflection right)"
                out.append(f"{step:<5} | {l:<5} | {r:<5} | {mid:<5} | {nums[mid]:<10} | {nums[r]:<12} | {action:<15}")
                l = mid + 1
            else:
                action = "r = mid (inflection at or left)"
                out.append(f"{step:<5} | {l:<5} | {r:<5} | {mid:<5} | {nums[mid]:<10} | {nums[r]:<12} | {action:<15}")
                r = mid
            step += 1
        out.append(f"Minimum element at index {l} is {nums[l]}")
        return "\n".join(out)

    problems.append(Problem(
        id=22,
        slug="p22_find_minimum_in_rotated_sorted_array",
        title="Find Minimum in Rotated Sorted Array",
        category="Binary Search",
        difficulty="Medium",
        statement="Suppose an array of length $n$ sorted in ascending order is rotated between 1 and $n$ times. Given the sorted rotated array `nums` of unique elements, return the minimum element of this array. Must run in $O(\\log N)$ time.",
        brute_force="Linear scan to find the minimum element in $O(N)$ time. Space: $O(1)$.",
        key_insight="Compare `nums[mid]` with `nums[right]`. If `nums[mid] > nums[right]`, the rotation pivot point (and minimum element) lies strictly to the right (`left = mid + 1`). Otherwise, the minimum is at `mid` or to the left (`right = mid`).",
        func_name="find_min",
        stub_code="""def find_min(nums: list[int]) -> int:
    \"\"\"Finds minimum element in rotated sorted array in O(log N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def find_min(nums: list[int]) -> int:
    \"\"\"Finds minimum element in rotated sorted array in O(log N) time.\"\"\"
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
            
    return nums[left]
""",
        tests_code="""assert find_min([3, 4, 5, 1, 2]) == 1
assert find_min([4, 5, 6, 7, 0, 1, 2]) == 0
assert find_min([11, 13, 15, 17]) == 11
assert find_min([2, 1]) == 1
""",
        time_complexity="$O(\\log N)$ binary search time.",
        space_complexity="$O(1)$ constant space.",
        follow_up="How many times was the array rotated? The index of the minimum element equals the number of clockwise rotation shifts.",
        run_trace=trace_p22
    ))

    # ----------------------------------------------------
    # Problem 23: Reverse Linked List
    # ----------------------------------------------------
    def trace_p23():
        vals = [1, 2, 3, 4, 5]
        out = [
            f"Input linked list: {' -> '.join(map(str, vals))} -> None",
            f"{'Step':<5} | {'curr':<6} | {'prev':<6} | {'next_node':<10} | {'Action':<25}",
            "-" * 55
        ]
        prev = None
        for i, val in enumerate(vals):
            next_node = vals[i + 1] if i + 1 < len(vals) else "None"
            out.append(f"{i+1:<5} | {val:<6} | {str(prev):<6} | {str(next_node):<10} | curr.next = prev, prev = curr")
            prev = val
        out.append(f"Reversed list head: {prev}")
        return "\n".join(out)

    problems.append(Problem(
        id=23,
        slug="p23_reverse_linked_list",
        title="Reverse Linked List",
        category="Linked List",
        difficulty="Easy",
        statement="Given the `head` of a singly linked list, reverse the list, and return the reversed list.",
        brute_force="Store all node values into an array, reverse the array, and reconstruct the linked list. Time: $O(N)$, Space: $O(N)$.",
        key_insight="Iterate through the list with three pointers: `prev`, `curr`, and `next_node`. Invert each pointer (`curr.next = prev`) in-place in $O(1)$ space.",
        func_name="reverse_list",
        stub_code="""class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    \"\"\"Reverses singly linked list in-place in O(N) time, O(1) space.\"\"\"
    raise NotImplementedError
""",
        solution_code="""class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    \"\"\"Reverses singly linked list in-place in O(N) time, O(1) space.\"\"\"
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
""",
        tests_code="""# Helper to build and read
def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

def from_list(vals):
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next

assert to_list(reverse_list(from_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
assert to_list(reverse_list(from_list([1, 2]))) == [2, 1]
assert to_list(reverse_list(from_list([]))) == []
""",
        time_complexity="$O(N)$ single linear pass.",
        space_complexity="$O(1)$ in-place iterative pointer manipulation.",
        follow_up="How to implement this recursively? Base case: if `head is None or head.next is None`, return `head`. Recursive step: `new_head = reverse_list(head.next); head.next.next = head; head.next = None; return new_head` ($O(N)$ stack space).",
        run_trace=trace_p23
    ))

    # ----------------------------------------------------
    # Problem 24: Merge Two Sorted Lists
    # ----------------------------------------------------
    def trace_p24():
        l1, l2 = [1, 2, 4], [1, 3, 4]
        out = [
            f"Input: list1 = {l1}, list2 = {l2}",
            f"{'Step':<5} | {'p1 val':<8} | {'p2 val':<8} | {'Picked Node':<12} | {'Merged Result':<20}",
            "-" * 55
        ]
        i, j = 0, 0
        merged = []
        step = 1
        while i < len(l1) and j < len(l2):
            if l1[i] <= l2[j]:
                merged.append(l1[i])
                out.append(f"{step:<5} | {l1[i]:<8} | {l2[j]:<8} | {l1[i]:<12} | {str(merged):<20}")
                i += 1
            else:
                merged.append(l2[j])
                out.append(f"{step:<5} | {l1[i]:<8} | {l2[j]:<8} | {l2[j]:<12} | {str(merged):<20}")
                j += 1
            step += 1
        while i < len(l1):
            merged.append(l1[i])
            out.append(f"{step:<5} | {l1[i]:<8} | None     | {l1[i]:<12} | {str(merged):<20}")
            i += 1
            step += 1
        while j < len(l2):
            merged.append(l2[j])
            out.append(f"{step:<5} | None     | {l2[j]:<8} | {l2[j]:<12} | {str(merged):<20}")
            j += 1
            step += 1
        return "\n".join(out)

    problems.append(Problem(
        id=24,
        slug="p24_merge_two_sorted_lists",
        title="Merge Two Sorted Lists",
        category="Linked List",
        difficulty="Easy",
        statement="You are given the heads of two sorted linked lists `list1` and `list2`. Merge the two lists into one sorted list by splicing together the nodes of the first two lists. Return the head of the merged linked list.",
        brute_force="Dump all elements into an array, sort the array, and create a new linked list. Time: $O((N + M) \\log(N + M))$, Space: $O(N + M)$.",
        key_insight="Use a `dummy` pre-head node and a pointer `tail`. Repeatedly attach whichever node has the smaller value (`tail.next = list1` or `list2`) in strictly $O(N + M)$ time and $O(1)$ memory.",
        func_name="merge_two_lists",
        stub_code="""def merge_two_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    \"\"\"Merges two sorted linked lists in O(N + M) time, O(1) space.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def merge_two_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    \"\"\"Merges two sorted linked lists in O(N + M) time, O(1) space.\"\"\"
    dummy = ListNode(0)
    tail = dummy
    
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
        
    tail.next = list1 if list1 else list2
    return dummy.next
""",
        tests_code="""assert to_list(merge_two_lists(from_list([1, 2, 4]), from_list([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]
assert to_list(merge_two_lists(from_list([]), from_list([]))) == []
assert to_list(merge_two_lists(from_list([]), from_list([0]))) == [0]
""",
        time_complexity="$O(N + M)$ where $N$ and $M$ are the lengths of the two lists.",
        space_complexity="$O(1)$ auxiliary memory by relinking existing nodes.",
        follow_up="What if one list is substantially longer than the other? Attach the remainder in $O(1)$ pointer assignment without looping.",
        run_trace=trace_p24
    ))

    # ----------------------------------------------------
    # Problem 25: Reorder List
    # ----------------------------------------------------
    def trace_p25():
        nodes = [1, 2, 3, 4, 5]
        out = [
            f"Original list: {nodes}",
            "Step 1: Find middle using fast/slow pointers -> middle node is 3",
            f"Step 2: Split into two halves: [1, 2, 3] and [4, 5]",
            f"Step 3: Reverse second half: [5, 4]",
            "Step 4: Interleave two halves: 1 -> 5 -> 2 -> 4 -> 3",
            "Result: [1, 5, 2, 4, 3]"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=25,
        slug="p25_reorder_list",
        title="Reorder List",
        category="Linked List",
        difficulty="Medium",
        statement="You are given the head of a singly linked-list: $L_0 \\to L_1 \\to \\dots \\to L_{n - 1} \\to L_n$. Reorder the list to: $L_0 \\to L_n \\to L_1 \\to L_{n - 1} \\to L_2 \\to L_{n - 2} \\dots$ in-place without modifying node values.",
        brute_force="Store all nodes in an array for random access, then rebuild pointers with two indices from front and back. Time: $O(N)$, Space: $O(N)$.",
        key_insight="Decompose into three classic sub-problems in $O(1)$ space: 1) Find middle node with fast/slow pointers, 2) Reverse second half, 3) Interleave merge the two halves.",
        func_name="reorder_list",
        stub_code="""def reorder_list(head: Optional[ListNode]) -> None:
    \"\"\"Reorders list in-place to L0 -> Ln -> L1 -> Ln-1 ...\"\"\"
    raise NotImplementedError
""",
        solution_code="""def reorder_list(head: Optional[ListNode]) -> None:
    \"\"\"Reorders list in-place to L0 -> Ln -> L1 -> Ln-1 ...\"\"\"
    if not head or not head.next:
        return
        
    # 1. Find middle node
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
    # 2. Reverse second half
    second = slow.next
    slow.next = None
    prev = None
    while second:
        nxt = second.next
        second.next = prev
        prev = second
        second = nxt
        
    # 3. Interleave two halves
    first, second = head, prev
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first, second = tmp1, tmp2
""",
        tests_code="""h1 = from_list([1, 2, 3, 4])
reorder_list(h1)
assert to_list(h1) == [1, 4, 2, 3]

h2 = from_list([1, 2, 3, 4, 5])
reorder_list(h2)
assert to_list(h2) == [1, 5, 2, 4, 3]

h3 = from_list([1])
reorder_list(h3)
assert to_list(h3) == [1]
""",
        time_complexity="$O(N)$ total across find-mid, reverse, and merge passes.",
        space_complexity="$O(1)$ strictly in-place pointer mutations.",
        follow_up="How to test if a linked list is a Palindrome using the same building blocks? Find mid, reverse second half, compare node values from both heads, then restore list.",
        run_trace=trace_p25
    ))

    # ----------------------------------------------------
    # Problem 26: Remove Nth Node From End of List
    # ----------------------------------------------------
    def trace_p26():
        vals = [1, 2, 3, 4, 5]
        n = 2
        out = [
            f"Input: {vals}, n = {n}",
            f"Dummy node (0) placed before head (1)",
            f"Fast advances {n+1} steps ahead of Slow:",
            f"  Fast at node 3 (idx 3), Slow at dummy (idx 0) - Gap of 3 nodes",
            "Advance Fast and Slow together until Fast reaches None:",
            "  Step 1: Slow at 1, Fast at 4",
            "  Step 2: Slow at 2, Fast at 5",
            "  Step 3: Slow at 3, Fast at None (End reached!)",
            "Remove target: slow.next = slow.next.next (bypasses node 4)",
            "Result: [1, 2, 3, 5]"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=26,
        slug="p26_remove_nth_from_end",
        title="Remove Nth Node From End of List",
        category="Linked List",
        difficulty="Medium",
        statement="Given the `head` of a linked list, remove the $n^{\\text{th}}$ node from the end of the list and return its head in one single pass.",
        brute_force="First pass: count length $L$. Second pass: advance to node $(L - n)$ and delete next node. Time: $O(N)$ (two passes), Space: $O(1)$.",
        key_insight="Maintain two pointers with a fixed gap of $n$ nodes. Advance `fast` $n$ steps ahead. Then move both `fast` and `slow` together until `fast` reaches the end; `slow` will sit directly before the node to delete.",
        func_name="remove_nth_from_end",
        stub_code="""def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    \"\"\"Removes nth node from end of list in a single pass.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    \"\"\"Removes nth node from end of list in a single pass.\"\"\"
    dummy = ListNode(0, head)
    slow = dummy
    fast = head
    
    # Advance fast by n steps
    for _ in range(n):
        if fast:
            fast = fast.next
            
    while fast:
        slow = slow.next
        fast = fast.next
        
    slow.next = slow.next.next
    return dummy.next
""",
        tests_code="""assert to_list(remove_nth_from_end(from_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
assert to_list(remove_nth_from_end(from_list([1]), 1)) == []
assert to_list(remove_nth_from_end(from_list([1, 2]), 1)) == [1]
assert to_list(remove_nth_from_end(from_list([1, 2]), 2)) == [2]
""",
        time_complexity="$O(N)$ single pass.",
        space_complexity="$O(1)$ constant auxiliary space.",
        follow_up="Why is a dummy node essential? It cleanly handles deleting the head node without adding a special branch condition.",
        run_trace=trace_p26
    ))

    # ----------------------------------------------------
    # Problem 27: Linked List Cycle
    # ----------------------------------------------------
    def trace_p27():
        out = [
            "List: 3 -> 2 -> 0 -> -4 -> (loops back to node 2)",
            f"{'Step':<5} | {'Slow Node':<10} | {'Fast Node':<10} | {'Status':<25}",
            "-" * 55,
            f"{'0':<5} | {'3 (idx 0)':<10} | {'3 (idx 0)':<10} | {'Start':<25}",
            f"{'1':<5} | {'2 (idx 1)':<10} | {'0 (idx 2)':<10} | {'Fast moved 2, Slow 1':<25}",
            f"{'2':<5} | {'0 (idx 2)':<10} | {'2 (idx 1)':<10} | {'Fast wrapped around':<25}",
            f"{'3':<5} | {'-4 (idx 3)':<10} | {'-4 (idx 3)':<10} | {'Collision detected! Cycle!':<25}"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=27,
        slug="p27_linked_list_cycle",
        title="Linked List Cycle",
        category="Linked List",
        difficulty="Easy",
        statement="Given `head`, the head of a linked list, determine if the linked list has a cycle in it using $O(1)$ memory.",
        brute_force="Store visited node references in a hash set. If a node is seen again, a cycle exists. Time: $O(N)$, Space: $O(N)$ memory.",
        key_insight="Floyd's Tortoise and Hare algorithm: Move `slow` by 1 step and `fast` by 2 steps. If a cycle exists, `fast` catches up to `slow` by closing the gap by 1 node per iteration.",
        func_name="has_cycle",
        stub_code="""def has_cycle(head: Optional[ListNode]) -> bool:
    \"\"\"Detects cycle using Floyd's Tortoise and Hare algorithm in O(1) space.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def has_cycle(head: Optional[ListNode]) -> bool:
    \"\"\"Detects cycle using Floyd's Tortoise and Hare algorithm in O(1) space.\"\"\"
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
            
    return False
""",
        tests_code="""n1, n2, n3, n4 = ListNode(3), ListNode(2), ListNode(0), ListNode(-4)
n1.next, n2.next, n3.next, n4.next = n2, n3, n4, n2
assert has_cycle(n1) is True

n_no_cycle = from_list([1, 2, 3])
assert has_cycle(n_no_cycle) is False
assert has_cycle(None) is False
""",
        time_complexity="$O(N)$ linear time.",
        space_complexity="$O(1)$ constant space without allocating memory.",
        follow_up="How to find the exact node where the cycle begins (Linked List Cycle II)? When `slow` and `fast` collide, reset one pointer to `head`; move both 1 step at a time; their next meeting point is the cycle start.",
        run_trace=trace_p27
    ))

    # ----------------------------------------------------
    # Problem 28: Merge K Sorted Lists
    # ----------------------------------------------------
    def trace_p28():
        lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
        out = [
            f"Input lists: {lists}",
            "Min-heap initialized with heads of each list: [(1, list0), (1, list1), (2, list2)]",
            f"{'Step':<5} | {'Popped (val, list_id)':<25} | {'Merged List':<25}",
            "-" * 60
        ]
        import heapq
        heap = []
        for i, lst in enumerate(lists):
            if lst:
                heapq.heappush(heap, (lst[0], i, 0))
        merged = []
        step = 1
        while heap:
            val, list_id, idx = heapq.heappop(heap)
            merged.append(val)
            out.append(f"{step:<5} | ({val}, list {list_id}){' '*13} | {str(merged):<25}")
            if idx + 1 < len(lists[list_id]):
                heapq.heappush(heap, (lists[list_id][idx + 1], list_id, idx + 1))
            step += 1
        return "\n".join(out)

    problems.append(Problem(
        id=28,
        slug="p28_merge_k_sorted_lists",
        title="Merge K Sorted Lists",
        category="Linked List",
        difficulty="Hard",
        statement="You are given an array of $k$ linked-lists `lists`, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.",
        brute_force="Iteratively merge lists one by one using 2-list merge. Time: $O(k \\cdot N)$ where $N$ is total number of nodes.",
        key_insight="Maintain a Min-Heap of size $k$ containing the current heads of all $k$ lists. Popping the smallest element and pushing its `next` node takes $O(\\log k)$ per node, yielding $O(N \\log k)$ total time.",
        func_name="merge_k_lists",
        stub_code="""def merge_k_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    \"\"\"Merges k sorted linked lists using a min-heap in O(N log k) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""import heapq

def merge_k_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    \"\"\"Merges k sorted linked lists using a min-heap in O(N log k) time.\"\"\"
    dummy = ListNode(0)
    curr = dummy
    heap: list[tuple[int, int, ListNode]] = []
    
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
            
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
            
    return dummy.next
""",
        tests_code="""l1 = from_list([1, 4, 5])
l2 = from_list([1, 3, 4])
l3 = from_list([2, 6])
assert to_list(merge_k_lists([l1, l2, l3])) == [1, 1, 2, 3, 4, 4, 5, 6]
assert to_list(merge_k_lists([])) == []
assert to_list(merge_k_lists([None])) == []
""",
        time_complexity="$O(N \\log k)$ where $N$ is total nodes and $k$ is number of lists.",
        space_complexity="$O(k)$ heap memory holding $k$ elements.",
        follow_up="Could you achieve the same complexity without a heap? Yes, using Divide and Conquer: pair up and merge $k$ lists recursively like merge sort in $O(N \\log k)$ time and $O(1)$ heap memory.",
        run_trace=trace_p28
    ))

    # ----------------------------------------------------
    # Problem 29: Invert Binary Tree
    # ----------------------------------------------------
    def trace_p29():
        out = [
            "Input tree: [4, 2, 7, 1, 3, 6, 9]",
            "Step 1: Invert node 4 children -> left becomes 7, right becomes 2",
            "Step 2: Recursively invert left subtree (root 7) -> children 6 and 9 swap to 9 and 6",
            "Step 3: Recursively invert right subtree (root 2) -> children 1 and 3 swap to 3 and 1",
            "Output tree: [4, 7, 2, 9, 6, 3, 1]"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=29,
        slug="p29_invert_binary_tree",
        title="Invert Binary Tree",
        category="Trees",
        difficulty="Easy",
        statement="Given the `root` of a binary tree, invert the tree (mirror reflection), and return its root.",
        brute_force="Reconstruct tree using level-order serialization mirrored. Time: $O(N)$, Space: $O(N)$.",
        key_insight="Post-order or pre-order recursive traversal: for every node, swap its left and right child pointers, then recursively invert both subtrees.",
        func_name="invert_tree",
        stub_code="""class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    \"\"\"Inverts binary tree recursively in O(N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    \"\"\"Inverts binary tree recursively in O(N) time.\"\"\"
    if not root:
        return None
        
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
""",
        tests_code="""root = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(7, TreeNode(6), TreeNode(9)))
inverted = invert_tree(root)
assert inverted.val == 4
assert inverted.left.val == 7
assert inverted.right.val == 2
assert inverted.left.left.val == 9
assert invert_tree(None) is None
""",
        time_complexity="$O(N)$ linear time visiting all $N$ nodes.",
        space_complexity="$O(H)$ recursion stack space where $H$ is tree height ($O(\\log N)$ balanced, $O(N)$ skewed).",
        follow_up="How to solve this iteratively without recursion? Use a BFS queue: pop node, swap its children, and push both non-null children onto the queue.",
        run_trace=trace_p29
    ))

    # ----------------------------------------------------
    # Problem 30: Maximum Depth of Binary Tree
    # ----------------------------------------------------
    def trace_p30():
        out = [
            "Tree: [3, 9, 20, null, null, 15, 7]",
            "DFS recursive calls:",
            "  max_depth(node 15) = 1 + max(0, 0) = 1",
            "  max_depth(node 7)  = 1 + max(0, 0) = 1",
            "  max_depth(node 20) = 1 + max(depth(15), depth(7)) = 1 + 1 = 2",
            "  max_depth(node 9)  = 1 + max(0, 0) = 1",
            "  max_depth(node 3)  = 1 + max(depth(9), depth(20)) = 1 + 2 = 3",
            "Maximum depth: 3"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=30,
        slug="p30_maximum_depth_of_binary_tree",
        title="Maximum Depth of Binary Tree",
        category="Trees",
        difficulty="Easy",
        statement="Given the `root` of a binary tree, return its maximum depth (number of nodes along the longest path from root to farthest leaf).",
        brute_force="Find all root-to-leaf paths and take the maximum length. Time: $O(N)$, Space: $O(N)$.",
        key_insight="Depth of node $N$ equals $1 + \\max(\\text{depth}(N.\\text{left}), \\text{depth}(N.\\text{right}))$. Base case: depth of `None` is 0.",
        func_name="max_depth",
        stub_code="""def max_depth(root: Optional[TreeNode]) -> int:
    \"\"\"Calculates maximum depth of binary tree in O(N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def max_depth(root: Optional[TreeNode]) -> int:
    \"\"\"Calculates maximum depth of binary tree in O(N) time.\"\"\"
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
""",
        tests_code="""root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
assert max_depth(root) == 3
assert max_depth(TreeNode(1, None, TreeNode(2))) == 2
assert max_depth(None) == 0
""",
        time_complexity="$O(N)$ visiting every node once.",
        space_complexity="$O(H)$ recursion call stack space.",
        follow_up="How to calculate minimum depth? Be careful with single-child nodes: if one child is `None`, depth is determined by the non-null child, not `min(0, right)`.",
        run_trace=trace_p30
    ))

    return problems
