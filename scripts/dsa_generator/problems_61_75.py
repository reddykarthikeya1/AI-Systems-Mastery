from .models import Problem

def get_problems_61_75() -> list[Problem]:
    problems = []

    # ----------------------------------------------------
    # Problem 61: Combination Sum IV
    # ----------------------------------------------------
    def trace_p61():
        nums = [1, 2, 3]
        target = 4
        dp = [1] + [0] * target
        for i in range(1, target + 1):
            for n in nums:
                if i - n >= 0:
                    dp[i] += dp[i - n]
        out = [
            f"Input: nums = {nums}, target = {target}",
            "1D DP Permutation count: dp[i] = sum(dp[i - n] for n in nums)",
            f"{'Target sum i':<15} | {'dp[i] combinations count':<25}",
            "-" * 45
        ]
        for i in range(1, target + 1):
            out.append(f"{i:<15} | {dp[i]:<25}")
        out.append(f"Total combinations for {target}: {dp[target]}")
        return "\n".join(out)

    problems.append(Problem(
        id=61,
        slug="p61_combination_sum_iv",
        title="Combination Sum IV",
        category="Dynamic Programming",
        difficulty="Medium",
        statement="Given an array of distinct integers `nums` and a target integer `target`, return the number of possible combinations (permutations) that add up to `target`.",
        brute_force="Recursively branch over all elements on every step: $O(N^T)$.",
        key_insight="Because order matters (e.g. `(1, 2)` and `(2, 1)` are distinct), this is a permutation DP. Transition: `dp[i] = sum(dp[i - num] for num in nums if i >= num)` with base case `dp[0] = 1`.",
        func_name="combination_sum_4",
        stub_code="""def combination_sum_4(nums: list[int], target: int) -> int:
    \"\"\"Finds number of permutations adding up to target in O(target * len(nums)).\"\"\"
    raise NotImplementedError
""",
        solution_code="""def combination_sum_4(nums: list[int], target: int) -> int:
    \"\"\"Finds number of permutations adding up to target in O(target * len(nums)).\"\"\"
    dp = [0] * (target + 1)
    dp[0] = 1
    
    for i in range(1, target + 1):
        for num in nums:
            if i - num >= 0:
                dp[i] += dp[i - num]
                
    return dp[target]
""",
        tests_code="""assert combination_sum_4([1, 2, 3], 4) == 7
assert combination_sum_4([9], 3) == 0
assert combination_sum_4([1, 2], 3) == 3 # (1,1,1), (1,2), (2,1)
assert combination_sum_4([4, 2], 0) == 1
""",
        time_complexity="$O(T \\cdot N)$ where $T$ is target and $N$ is array length.",
        space_complexity="$O(T)$ DP array of size $T+1$.",
        follow_up="What if negative numbers were allowed in `nums`? Cycles of arbitrary length could sum to zero, creating infinite combinations. A maximum path length limit would be required.",
        run_trace=trace_p61
    ))

    # ----------------------------------------------------
    # Problem 62: Decode Ways
    # ----------------------------------------------------
    def trace_p62():
        s = "226"
        out = [
            f"Input: '{s}'",
            "DP decoding steps (single digit '1'-'9', double digit '10'-'26'):",
            "  i = 0 ('2'): single valid '2' ('B') -> 1 way",
            "  i = 1 ('2'): single '2' ('BB') or double '22' ('V') -> 2 ways",
            "  i = 2 ('6'): single '6' ('BBF', 'VF') or double '26' ('BZ') -> 3 ways",
            "Total decode ways: 3"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=62,
        slug="p62_decode_ways",
        title="Decode Ways",
        category="Dynamic Programming",
        difficulty="Medium",
        statement="A message containing letters from A-Z can be encoded into numbers using the mapping `'A' -> 1, 'B' -> 2, ... 'Z' -> 26`. Given a string `s` containing only digits, return the number of ways to decode it.",
        brute_force="Explore all 1-character and 2-character splits recursively: $O(2^N)$ time.",
        key_insight="At index $i$, check two transitions: 1) Single digit $s[i-1]$ (valid if $\\ne '0'$), adding $dp[i-1]$; 2) Two digits $s[i-2:i]$ (valid if between 10 and 26), adding $dp[i-2]$.",
        func_name="num_decodings",
        stub_code="""def num_decodings(s: str) -> int:
    \"\"\"Calculates number of ways to decode string of digits in O(N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def num_decodings(s: str) -> int:
    \"\"\"Calculates number of ways to decode string of digits in O(N) time.\"\"\"
    if not s or s[0] == "0":
        return 0
        
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    
    for i in range(2, n + 1):
        # One digit check
        if s[i - 1] != "0":
            dp[i] += dp[i - 1]
            
        # Two digit check
        two_digit = int(s[i - 2 : i])
        if 10 <= two_digit <= 26:
            dp[i] += dp[i - 2]
            
    return dp[n]
""",
        tests_code="""assert num_decodings("12") == 2
assert num_decodings("226") == 3
assert num_decodings("06") == 0 # Leading zero cannot be decoded
assert num_decodings("10") == 1
assert num_decodings("27") == 1
""",
        time_complexity="$O(N)$ single linear pass.",
        space_complexity="$O(N)$ or $O(1)$ by storing only the previous two states.",
        follow_up="What if `*` characters represent any digit from 1 to 9 (Decode Ways II)? Branch cases taking into account possibilities for `*` alone (9 ways) and paired with adjacent digits.",
        run_trace=trace_p62
    ))

    # ----------------------------------------------------
    # Problem 63: Unique Paths (2D Dynamic Programming)
    # ----------------------------------------------------
    def trace_p63():
        m, n = 3, 3
        dp = [[1] * n for _ in range(m)]
        out = [
            f"Input grid: m = {m}, n = {n}",
            "2D Grid DP table: dp[r][c] = dp[r-1][c] + dp[r][c-1]",
            "Grid progression:"
        ]
        for r in range(1, m):
            for c in range(1, n):
                dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
        for r in range(m):
            out.append(f"  Row {r}: {dp[r]}")
        out.append(f"Unique paths to bottom-right ({m-1}, {n-1}): {dp[m-1][n-1]}")
        return "\n".join(out)

    problems.append(Problem(
        id=63,
        slug="p63_unique_paths",
        title="Unique Paths",
        category="Dynamic Programming",
        difficulty="Medium",
        statement="There is a robot on an $m \\times n$ grid. The robot is initially located at the top-left corner and tries to move to the bottom-right corner. The robot can only move either down or right at any point in time. Return the number of possible unique paths.",
        brute_force="Recursive DFS moving down or right: $O(2^{m+n})$.",
        key_insight="To reach cell $(r, c)$, the robot comes from above $(r-1, c)$ or left $(r, c-1)$. Transition: `dp[r][c] = dp[r-1][c] + dp[r][c-1]`. Rolling 1D array achieves $O(n)$ space.",
        func_name="unique_paths",
        stub_code="""def unique_paths(m: int, n: int) -> int:
    \"\"\"Finds unique paths in m x n grid using 2D DP in O(m * n) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def unique_paths(m: int, n: int) -> int:
    \"\"\"Finds unique paths in m x n grid using 2D DP in O(m * n) time.\"\"\"
    row = [1] * n
    
    for _ in range(m - 1):
        new_row = [1] * n
        for c in range(1, n):
            new_row[c] = new_row[c - 1] + row[c]
        row = new_row
        
    return row[-1]
""",
        tests_code="""assert unique_paths(3, 7) == 28
assert unique_paths(3, 2) == 3
assert unique_paths(1, 1) == 1
assert unique_paths(3, 3) == 6
""",
        time_complexity="$O(m \\cdot n)$ filling the table.",
        space_complexity="$O(n)$ space using a rolling single row.",
        follow_up="Can this be computed in $O(m)$ without dynamic programming? Yes, using combinatorics: the robot must make exactly $(m - 1)$ down steps and $(n - 1)$ right steps, which equals $\\binom{m + n - 2}{m - 1}$.",
        run_trace=trace_p63
    ))

    # ----------------------------------------------------
    # Problem 64: Longest Common Subsequence (2D DP)
    # ----------------------------------------------------
    def trace_p64():
        text1, text2 = "abcde", "ace"
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = 1 + dp[i - 1][j - 1]
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        out = [
            f"Input: text1 = '{text1}', text2 = '{text2}'",
            "2D DP Table dp[i][j] (length of LCS of text1[:i] and text2[:j]):",
            f"{'':>4} | {'':>4} " + " ".join(f"{c:>4}" for c in text2),
            "-" * 25
        ]
        for i in range(m + 1):
            prefix_char = text1[i - 1] if i > 0 else " "
            row_vals = " ".join(f"{dp[i][j]:>4}" for j in range(n + 1))
            out.append(f"{prefix_char:>4} | {row_vals}")
        out.append(f"Longest Common Subsequence Length: {dp[m][n]}")
        return "\n".join(out)

    problems.append(Problem(
        id=64,
        slug="p64_longest_common_subsequence",
        title="Longest Common Subsequence",
        category="Dynamic Programming",
        difficulty="Medium",
        statement="Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return `0`.",
        brute_force="Generate all $2^M$ subsequences of `text1` and check if they are in `text2`. Time: $O(2^M \\cdot N)$.",
        key_insight="2D Dynamic Programming: if characters match (`text1[i] == text2[j]`), `dp[i][j] = 1 + dp[i-1][j-1]`. Otherwise, discard one character from either string: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.",
        func_name="longest_common_subsequence",
        stub_code="""def longest_common_subsequence(text1: str, text2: str) -> int:
    \"\"\"Computes LCS length in O(M * N) time using 2D DP.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def longest_common_subsequence(text1: str, text2: str) -> int:
    \"\"\"Computes LCS length in O(M * N) time using 2D DP.\"\"\"
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    return dp[m][n]
""",
        tests_code="""assert longest_common_subsequence("abcde", "ace") == 3
assert longest_common_subsequence("abc", "abc") == 3
assert longest_common_subsequence("abc", "def") == 0
assert longest_common_subsequence("", "a") == 0
""",
        time_complexity="$O(M \\cdot N)$ filling an $M \\times N$ grid.",
        space_complexity="$O(M \\cdot N)$ or $O(\\min(M, N))$ space using rolling rows.",
        follow_up="How to reconstruct the actual LCS string? Backtrack through the DP table from $(m, n)$: if characters match, prepend to string and move diagonally; else move in the direction of the larger neighbor.",
        run_trace=trace_p64
    ))

    # ----------------------------------------------------
    # Problem 65: Edit Distance (2D DP)
    # ----------------------------------------------------
    def trace_p65():
        w1, w2 = "horse", "ros"
        m, n = len(w1), len(w2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if w1[i - 1] == w2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        out = [
            f"Input: word1 = '{w1}', word2 = '{w2}'",
            "Levenshtein Distance 2D DP Table:",
            f"{'':>4} | {'':>3} " + " ".join(f"{c:>3}" for c in w2),
            "-" * 25
        ]
        for i in range(m + 1):
            ch = w1[i - 1] if i > 0 else " "
            row_vals = " ".join(f"{dp[i][j]:>3}" for j in range(n + 1))
            out.append(f"{ch:>4} | {row_vals}")
        out.append(f"Minimum Edit Distance: {dp[m][n]}")
        return "\n".join(out)

    problems.append(Problem(
        id=65,
        slug="p65_edit_distance",
        title="Edit Distance",
        category="Dynamic Programming",
        difficulty="Medium",
        statement="Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`. You have three operations permitted on a word: insert a character, delete a character, or replace a character.",
        brute_force="Try all 3 operations at every character recursively: $O(3^{\\max(M, N)})$.",
        key_insight="Classic Levenshtein 2D DP: if characters match (`word1[i-1] == word2[j-1]`), cost is $0$: `dp[i][j] = dp[i-1][j-1]`. If they differ, take $1 + \\min(\\text{insert}: dp[i][j-1], \\text{delete}: dp[i-1][j], \\text{replace}: dp[i-1][j-1])$.",
        func_name="min_distance",
        stub_code="""def min_distance(word1: str, word2: str) -> int:
    \"\"\"Calculates edit distance between word1 and word2 in O(M * N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def min_distance(word1: str, word2: str) -> int:
    \"\"\"Calculates edit distance between word1 and word2 in O(M * N) time.\"\"\"
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1]   # Replace
                )
                
    return dp[m][n]
""",
        tests_code="""assert min_distance("horse", "ros") == 3
assert min_distance("intention", "execution") == 5
assert min_distance("", "abc") == 3
assert min_distance("same", "same") == 0
""",
        time_complexity="$O(M \\cdot N)$ time filling the matrix.",
        space_complexity="$O(M \\cdot N)$ or $O(\\min(M, N))$ space with rolling row optimization.",
        follow_up="What if character weights differ (e.g. deletion costs 2, replacement costs 3)? Modify the constants inside the `min(...)` branch accordingly.",
        run_trace=trace_p65
    ))

    # ----------------------------------------------------
    # Problem 66: Partition Equal Subset Sum (0/1 Knapsack)
    # ----------------------------------------------------
    def trace_p66():
        nums = [1, 5, 11, 5]
        total = sum(nums)
        target = total // 2
        out = [
            f"Input: {nums}, total sum = {total}",
            f"Target subset sum: {target}",
            "0/1 Knapsack DP (reverse set state update):",
            "  Start reachable sums: {0}",
            "  Process 1: {0, 1}",
            "  Process 5: {0, 1, 5, 6}",
            "  Process 11: {0, 1, 5, 6, 11, 12, 16, 17}",
            f"  Target {target} reached! Subset exists (e.g. [1, 5, 5] and [11])",
            "Result: True"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=66,
        slug="p66_partition_equal_subset_sum",
        title="Partition Equal Subset Sum",
        category="Dynamic Programming",
        difficulty="Medium",
        statement="Given an integer array `nums`, return `True` if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or `False` otherwise.",
        brute_force="Generate all subsets and compare subset sums: $O(2^N)$.",
        key_insight="Total sum must be even; target sum for each subset is $\\text{target} = \\text{total} // 2$. This is classic **0/1 Knapsack**: can we pick a subset of elements that sums exactly to `target`? Maintain a hash set of reachable sums.",
        func_name="can_partition",
        stub_code="""def can_partition(nums: list[int]) -> bool:
    \"\"\"Determines if array can be partitioned into two equal subsets.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def can_partition(nums: list[int]) -> bool:
    \"\"\"Determines if array can be partitioned into two equal subsets.\"\"\"
    total = sum(nums)
    if total % 2 != 0:
        return False
        
    target = total // 2
    dp = {0}
    
    for num in nums:
        next_dp = set(dp)
        for t in dp:
            if t + num == target:
                return True
            if t + num < target:
                next_dp.add(t + num)
        dp = next_dp
        
    return target in dp
""",
        tests_code="""assert can_partition([1, 5, 11, 5]) is True
assert can_partition([1, 2, 3, 5]) is False
assert can_partition([2, 2]) is True
assert can_partition([1]) is False
""",
        time_complexity="$O(N \\cdot \\text{target})$ pseudo-polynomial time.",
        space_complexity="$O(\\text{target})$ space to store reachable sums up to target.",
        follow_up="How to optimize space to a bitset? Represent the DP state with a single integer: `dp |= (dp << num)`; check if bit at `target` is set in $O(N \\cdot \\text{target} / 64)$.",
        run_trace=trace_p66
    ))

    # ----------------------------------------------------
    # Problem 67: Jump Game
    # ----------------------------------------------------
    def trace_p67():
        nums = [2, 3, 1, 1, 4]
        out = [
            f"Input: {nums}",
            "Greedy max reachable index tracker:",
            f"{'i':<3} | {'nums[i]':<8} | {'Max Reachable (max(reach, i + nums[i]))':<40}",
            "-" * 55
        ]
        reach = 0
        for i, jump in enumerate(nums):
            reach = max(reach, i + jump)
            out.append(f"{i:<3} | {jump:<8} | max_reach = {reach}")
        out.append(f"Reached destination index {len(nums)-1}: True")
        return "\n".join(out)

    problems.append(Problem(
        id=67,
        slug="p67_jump_game",
        title="Jump Game",
        category="Dynamic Programming",
        difficulty="Medium",
        statement="You are given an integer array `nums`. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position. Return `True` if you can reach the last index, or `False` otherwise.",
        brute_force="Recursively explore every jump choice from current position: $O(2^N)$.",
        key_insight="Maintain the maximum index reachable so far `max_reach`. As you scan $i = 0 \\dots N-1$, if $i > \\text{max\\_reach}$, you are stranded and cannot proceed. Otherwise, update $\\text{max\\_reach} = \\max(\\text{max\\_reach}, i + nums[i])$.",
        func_name="can_jump",
        stub_code="""def can_jump(nums: list[int]) -> bool:
    \"\"\"Determines if last index is reachable in O(N) time, O(1) space.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def can_jump(nums: list[int]) -> bool:
    \"\"\"Determines if last index is reachable in O(N) time, O(1) space.\"\"\"
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
    return True
""",
        tests_code="""assert can_jump([2, 3, 1, 1, 4]) is True
assert can_jump([3, 2, 1, 0, 4]) is False
assert can_jump([0]) is True
assert can_jump([2, 0, 0]) is True
""",
        time_complexity="$O(N)$ single pass over array.",
        space_complexity="$O(1)$ constant auxiliary memory.",
        follow_up="How to compute the MINIMUM number of jumps needed to reach the end (Jump Game II)? Use BFS window intervals $[\\text{curr\\_end}, \\text{farthest}]$ in $O(N)$ time and $O(1)$ space.",
        run_trace=trace_p67
    ))

    # ----------------------------------------------------
    # Problem 68: Insert Interval
    # ----------------------------------------------------
    def trace_p68():
        intervals = [[1, 3], [6, 9]]
        newInterval = [2, 5]
        out = [
            f"Input: intervals = {intervals}, newInterval = {newInterval}",
            "Step 1: Intervals completely before newInterval (end < 2):",
            "  None (interval [1, 3] overlaps since 3 >= 2)",
            "Step 2: Merge overlapping intervals (start <= new_end):",
            "  Merge [1, 3] with [2, 5] -> [min(1, 2), max(3, 5)] = [1, 5]",
            "Step 3: Intervals completely after merged [1, 5] (start > 5):",
            "  Append [6, 9]",
            "Result: [[1, 5], [6, 9]]"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=68,
        slug="p68_insert_interval",
        title="Insert Interval",
        category="Intervals",
        difficulty="Medium",
        statement="You are given an array of non-overlapping intervals `intervals` where `intervals[i] = [start_i, end_i]` sorted in ascending order by `start_i`. You are also given an interval `newInterval`. Insert `newInterval` into `intervals` such that `intervals` is still sorted and non-overlapping (merge overlapping intervals if necessary).",
        brute_force="Append `newInterval` to `intervals`, sort in $O(N \\log N)$, and run merge intervals.",
        key_insight="Since the input is already sorted, execute in three linear phases: 1) Add all intervals ending before `newInterval.start`, 2) Merge all intervals overlapping with `newInterval`, 3) Add all intervals starting after `newInterval.end`.",
        func_name="insert_interval",
        stub_code="""def insert_interval(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    \"\"\"Inserts and merges new_interval into sorted non-overlapping intervals in O(N).\"\"\"
    raise NotImplementedError
""",
        solution_code="""def insert_interval(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    \"\"\"Inserts and merges new_interval into sorted non-overlapping intervals in O(N).\"\"\"
    res: list[list[int]] = []
    i = 0
    n = len(intervals)
    
    # 1. Before new_interval
    while i < n and intervals[i][1] < new_interval[0]:
        res.append(intervals[i])
        i += 1
        
    # 2. Overlapping merges
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    res.append(new_interval)
    
    # 3. After new_interval
    while i < n:
        res.append(intervals[i])
        i += 1
        
    return res
""",
        tests_code="""assert insert_interval([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
assert insert_interval([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [[1, 2], [3, 10], [12, 16]]
assert insert_interval([], [5, 7]) == [[5, 7]]
""",
        time_complexity="$O(N)$ single linear pass.",
        space_complexity="$O(N)$ output array memory.",
        follow_up="Could binary search be used to find insertion positions? Yes, binary search finds start and end indices in $O(\\log N)$, but splicing the array still requires $O(N)$ time.",
        run_trace=trace_p68
    ))

    # ----------------------------------------------------
    # Problem 69: Merge Intervals
    # ----------------------------------------------------
    def trace_p69():
        intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
        out = [
            f"Input intervals (sorted): {intervals}",
            f"{'Step':<5} | {'Interval':<12} | {'Current Merged State':<30} | {'Action':<25}",
            "-" * 75,
            f"{'1':<5} | {'[1, 3]':<12} | {'[[1, 3]]':<30} | {'Initial interval':<25}",
            f"{'2':<5} | {'[2, 6]':<12} | {'[[1, 6]]':<30} | {'Overlap (2 <= 3): merge':<25}",
            f"{'3':<5} | {'[8, 10]':<12} | {'[[1, 6], [8, 10]]':<30} | {'Disjoint (8 > 6): append':<25}",
            f"{'4':<5} | {'[15, 18]':<12} | {'[[1, 6], [8, 10], [15, 18]]':<30} | {'Disjoint (15 > 10): append':<25}",
            "Final merged intervals: [[1, 6], [8, 10], [15, 18]]"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=69,
        slug="p69_merge_intervals",
        title="Merge Intervals",
        category="Intervals",
        difficulty="Medium",
        statement="Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.",
        brute_force="Graph connected components: represent intervals as nodes, overlap as edges, and find connected components. Time: $O(N^2)$.",
        key_insight="Sort intervals by start time. Iterate through sorted intervals: if the current interval starts before or at the end of the previous interval (`curr[0] <= prev[1]`), merge them by extending `prev[1] = max(prev[1], curr[1])`. Otherwise, append `curr` as a new interval.",
        func_name="merge_intervals",
        stub_code="""def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    \"\"\"Merges overlapping intervals in O(N log N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    \"\"\"Merges overlapping intervals in O(N log N) time.\"\"\"
    if not intervals:
        return []
        
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for current in intervals[1:]:
        prev = merged[-1]
        if current[0] <= prev[1]:
            prev[1] = max(prev[1], current[1])
        else:
            merged.append(current)
            
    return merged
""",
        tests_code="""assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]
assert merge_intervals([]) == []
assert merge_intervals([[1, 4], [0, 4]]) == [[0, 4]]
""",
        time_complexity="$O(N \\log N)$ dominated by sorting.",
        space_complexity="$O(N)$ for output list and sorting memory.",
        follow_up="What if input intervals are an unbounded data stream? Maintain an Interval Tree or Segment Tree to support dynamic insertion and merging.",
        run_trace=trace_p69
    ))

    # ----------------------------------------------------
    # Problem 70: Non-overlapping Intervals
    # ----------------------------------------------------
    def trace_p70():
        intervals = [[1, 2], [2, 3], [3, 4], [1, 3]]
        intervals_sorted = sorted(intervals, key=lambda x: x[1])
        out = [
            f"Input: {intervals}",
            f"Greedy sort by END times: {intervals_sorted}",
            "Selection step:",
            "  Pick [1, 2] (prev_end = 2)",
            "  Pick [2, 3] (start 2 >= prev_end 2 -> compatible! prev_end = 3)",
            "  Skip [1, 3] (start 1 < prev_end 3 -> conflict! Removed)",
            "  Pick [3, 4] (start 3 >= prev_end 3 -> compatible! prev_end = 4)",
            "Total intervals removed: 1"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=70,
        slug="p70_non_overlapping_intervals",
        title="Non-overlapping Intervals",
        category="Intervals",
        difficulty="Medium",
        statement="Given an array of intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.",
        brute_force="Generate all subsets of intervals and check if they are pairwise non-overlapping. Time: $O(2^N)$.",
        key_insight="This is Interval Scheduling Maximization: to maximize the count of mutually compatible intervals, greedily pick intervals that **end earliest**. Sort by end time, and greedily remove any interval that starts before the previously kept interval ends.",
        func_name="erase_overlap_intervals",
        stub_code="""def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    \"\"\"Finds minimum intervals to remove for no overlaps in O(N log N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    \"\"\"Finds minimum intervals to remove for no overlaps in O(N log N) time.\"\"\"
    if not intervals:
        return 0
        
    intervals.sort(key=lambda x: x[1])
    removals = 0
    prev_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < prev_end:
            removals += 1
        else:
            prev_end = intervals[i][1]
            
    return removals
""",
        tests_code="""assert erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]) == 1
assert erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]) == 2
assert erase_overlap_intervals([[1, 2], [2, 3]]) == 0
""",
        time_complexity="$O(N \\log N)$ sorting time.",
        space_complexity="$O(1)$ auxiliary memory.",
        follow_up="Why does sorting by END time work greedily while sorting by START time does not? An interval ending early leaves maximum room for future intervals.",
        run_trace=trace_p70
    ))

    # ----------------------------------------------------
    # Problem 71: Meeting Rooms
    # ----------------------------------------------------
    def trace_p71():
        intervals = [[0, 30], [5, 10], [15, 20]]
        intervals.sort(key=lambda x: x[0])
        out = [
            f"Input meetings sorted by start time: {intervals}",
            f"{'Pair':<15} | {'Meeting A end':<15} | {'Meeting B start':<15} | {'Overlap?':<10}",
            "-" * 55,
            f"{'[0, 30] vs [5, 10]':<15} | {30:<15} | {5:<15} | Conflict! (30 > 5)",
            "Person cannot attend all meetings: False"
        ]
        return "\n".join(out)

    problems.append(Problem(
        id=71,
        slug="p71_meeting_rooms",
        title="Meeting Rooms",
        category="Intervals",
        difficulty="Easy",
        statement="Given an array of meeting time intervals where `intervals[i] = [start_i, end_i]`, determine if a person could attend all meetings without overlap.",
        brute_force="Compare all pairs $(i, j)$ and check if they overlap. Time: $O(N^2)$, Space: $O(1)$.",
        key_insight="Sort meetings by start time. A person can attend all meetings if and only if every meeting starts after or at the exact time the previous meeting concludes (`intervals[i][0] >= intervals[i-1][1]`).",
        func_name="can_attend_meetings",
        stub_code="""def can_attend_meetings(intervals: list[list[int]]) -> bool:
    \"\"\"Determines if a person can attend all meetings in O(N log N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def can_attend_meetings(intervals: list[list[int]]) -> bool:
    \"\"\"Determines if a person can attend all meetings in O(N log N) time.\"\"\"
    intervals.sort(key=lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False
    return True
""",
        tests_code="""assert can_attend_meetings([[0, 30], [5, 10], [15, 20]]) is False
assert can_attend_meetings([[7, 10], [2, 4]]) is True
assert can_attend_meetings([]) is True
assert can_attend_meetings([[1, 5], [5, 10]]) is True # Adjacent meetings permitted
""",
        time_complexity="$O(N \\log N)$ sorting time.",
        space_complexity="$O(1)$ auxiliary space.",
        follow_up="What if meeting times are given as timestamps with timezones? Convert all timestamps into UTC Unix epoch milliseconds before sorting.",
        run_trace=trace_p71
    ))

    # ----------------------------------------------------
    # Problem 72: Meeting Rooms II
    # ----------------------------------------------------
    def trace_p72():
        intervals = [[0, 30], [5, 10], [15, 20]]
        intervals.sort(key=lambda x: x[0])
        import heapq
        rooms = []
        out = [
            f"Sorted meetings: {intervals}",
            "Min-heap stores end times of active meeting rooms:",
            f"{'Meeting':<12} | {'Earliest End in Heap':<22} | {'Heap State':<22} | {'Action':<20}",
            "-" * 75
        ]
        for m in intervals:
            if rooms and rooms[0] <= m[0]:
                earliest = rooms[0]
                heapq.heappop(rooms)
                action = "Reuse room (pop earliest)"
            else:
                earliest = rooms[0] if rooms else "None"
                action = "Allocate new room"
            heapq.heappush(rooms, m[1])
            out.append(f"{str(m):<12} | {str(earliest):<22} | {str(rooms):<22} | {action:<20}")
        out.append(f"Minimum conference rooms required: {len(rooms)}")
        return "\n".join(out)

    problems.append(Problem(
        id=72,
        slug="p72_meeting_rooms_ii",
        title="Meeting Rooms II",
        category="Intervals",
        difficulty="Medium",
        statement="Given an array of meeting time intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the minimum number of conference rooms required.",
        brute_force="For every minute in time, count how many meetings are active and find the peak. Time: $O(T \\cdot N)$ where $T$ is time range.",
        key_insight="Sort meetings by start time and maintain a **Min-Heap** of meeting end times. When a new meeting starts, check if the room with the earliest end time has freed up (`heap[0] <= meeting[0]`). If so, reuse that room; otherwise, allocate a new room.",
        func_name="min_meeting_rooms",
        stub_code="""def min_meeting_rooms(intervals: list[list[int]]) -> int:
    \"\"\"Finds minimum meeting rooms needed using min-heap in O(N log N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""import heapq

def min_meeting_rooms(intervals: list[list[int]]) -> int:
    \"\"\"Finds minimum meeting rooms needed using min-heap in O(N log N) time.\"\"\"
    if not intervals:
        return 0
        
    intervals.sort(key=lambda x: x[0])
    rooms: list[int] = []  # Min-heap of end times
    
    for meeting in intervals:
        if rooms and rooms[0] <= meeting[0]:
            heapq.heappop(rooms)
        heapq.heappush(rooms, meeting[1])
        
    return len(rooms)
""",
        tests_code="""assert min_meeting_rooms([[0, 30], [5, 10], [15, 20]]) == 2
assert min_meeting_rooms([[7, 10], [2, 4]]) == 1
assert min_meeting_rooms([[1, 5], [2, 6], [3, 7], [4, 8]]) == 4
assert min_meeting_rooms([]) == 0
""",
        time_complexity="$O(N \\log N)$ time for sorting and heap operations.",
        space_complexity="$O(N)$ heap memory.",
        follow_up="Could this be solved with the Line Sweep Algorithm? Yes, split intervals into start (+1) and end (-1) timestamp events, sort events, and track the maximum running prefix sum in $O(N \\log N)$.",
        run_trace=trace_p72
    ))

    # ----------------------------------------------------
    # Problem 73: Number of 1 Bits
    # ----------------------------------------------------
    def trace_p73():
        n = 11  # 1011 in binary
        out = [
            f"Input: n = {n} (binary: {bin(n)})",
            "Brian Kernighan's Algorithm (n &= n - 1 clears lowest set bit):",
            f"{'Step':<5} | {'n (decimal)':<12} | {'n (binary)':<12} | {'n - 1 (binary)':<15} | {'n & (n - 1) (binary)':<20}",
            "-" * 65
        ]
        count = 0
        curr = n
        while curr:
            count += 1
            n_minus_1 = curr - 1
            next_curr = curr & (curr - 1)
            out.append(f"{count:<5} | {curr:<12} | {bin(curr)[2:]:>10}   | {bin(n_minus_1)[2:]:>12}    | {bin(next_curr)[2:]:>15}")
            curr = next_curr
        out.append(f"Total set bits (Hamming Weight): {count}")
        return "\n".join(out)

    problems.append(Problem(
        id=73,
        slug="p73_number_of_1_bits",
        title="Number of 1 Bits",
        category="Bit Manipulation",
        difficulty="Easy",
        statement="Given a positive integer `n`, write a function that returns the number of set bits (1s) it has (also known as the Hamming weight).",
        brute_force="Loop through all 32 bits and count how many times `n & 1` is 1 by shifting `n >>= 1`. Takes 32 iterations.",
        key_insight="**Brian Kernighan's Algorithm**: the operation `n & (n - 1)` clears the lowest set bit of `n`. Looping `while n: n &= (n - 1)` executes in exactly $O(K)$ iterations where $K$ is the number of 1-bits.",
        func_name="hamming_weight",
        stub_code="""def hamming_weight(n: int) -> int:
    \"\"\"Counts set bits in integer using Brian Kernighan's algorithm.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def hamming_weight(n: int) -> int:
    \"\"\"Counts set bits in integer using Brian Kernighan's algorithm.\"\"\"
    count = 0
    while n:
        n &= (n - 1)
        count += 1
    return count
""",
        tests_code="""assert hamming_weight(11) == 3 # 1011
assert hamming_weight(128) == 1 # 10000000
assert hamming_weight(2147483645) == 30
assert hamming_weight(0) == 0
""",
        time_complexity="$O(K)$ where $K$ is number of set bits (at most 32 or 64 operations).",
        space_complexity="$O(1)$ constant auxiliary memory.",
        follow_up="How does CPython / hardware implement this? Modern x86 processors have a dedicated `POPCNT` instruction that executes in 1 clock cycle.",
        run_trace=trace_p73
    ))

    # ----------------------------------------------------
    # Problem 74: Counting Bits
    # ----------------------------------------------------
    def trace_p74():
        n = 5
        dp = [0] * (n + 1)
        out = [
            f"Input: n = {n}",
            "Bit DP relation: dp[i] = dp[i >> 1] + (i & 1)",
            f"{'i':<3} | {'Binary':<8} | {'i >> 1':<8} | {'dp[i >> 1]':<12} | {'i & 1':<8} | {'dp[i]':<6}",
            "-" * 50
        ]
        for i in range(1, n + 1):
            dp[i] = dp[i >> 1] + (i & 1)
            out.append(f"{i:<3} | {bin(i)[2:]:>6}   | {i >> 1:<8} | {dp[i >> 1]:<12} | {i & 1:<8} | {dp[i]:<6}")
        out.append(f"Result for n = {n}: {dp}")
        return "\n".join(out)

    problems.append(Problem(
        id=74,
        slug="p74_counting_bits",
        title="Counting Bits",
        category="Bit Manipulation",
        difficulty="Easy",
        statement="Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` ($0 \\le i \\le n$), `ans[i]` is the number of 1's in the binary representation of `i`. Must run in $O(N)$ linear time.",
        brute_force="Compute `hamming_weight(i)` independently for each number from $0$ to $n$: $O(N \\log N)$.",
        key_insight="Dynamic Programming with bit shifting: right shifting $i$ by 1 (`i >> 1`) removes its least significant bit. The number of 1-bits in $i$ is simply `dp[i >> 1] + (i & 1)`.",
        func_name="count_bits",
        stub_code="""def count_bits(n: int) -> list[int]:
    \"\"\"Counts set bits for all integers 0 to n in linear O(N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def count_bits(n: int) -> list[int]:
    \"\"\"Counts set bits for all integers 0 to n in linear O(N) time.\"\"\"
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
""",
        tests_code="""assert count_bits(2) == [0, 1, 1]
assert count_bits(5) == [0, 1, 1, 2, 1, 2]
assert count_bits(0) == [0]
""",
        time_complexity="$O(N)$ linear time single pass.",
        space_complexity="$O(1)$ auxiliary memory (output array excluded).",
        follow_up="Could you also compute this using Most Significant Bit (MSB)? Yes, `dp[i] = 1 + dp[i - offset]` where `offset` doubles whenever $i$ reaches a power of 2.",
        run_trace=trace_p74
    ))

    # ----------------------------------------------------
    # Problem 75: Missing Number
    # ----------------------------------------------------
    def trace_p75():
        nums = [3, 0, 1]
        n = len(nums)
        xor_sum = n
        out = [
            f"Input: nums = {nums}, n = {n}",
            "XOR cancellation property: a ^ a = 0 and a ^ 0 = a",
            f"Initial xor_sum = {n} (binary {bin(n)})",
            f"{'i':<3} | {'nums[i]':<8} | {'XOR with i and nums[i]':<25} | {'Running xor_sum':<15}",
            "-" * 55
        ]
        for i, num in enumerate(nums):
            xor_sum ^= i ^ num
            out.append(f"{i:<3} | {num:<8} | xor ^= ({i} ^ {num}){' '*10} | {xor_sum} ({bin(xor_sum)})")
        out.append(f"Missing Number: {xor_sum}")
        return "\n".join(out)

    problems.append(Problem(
        id=75,
        slug="p75_missing_number",
        title="Missing Number",
        category="Bit Manipulation",
        difficulty="Easy",
        statement="Given an array `nums` containing $n$ distinct numbers in the range $[0, n]$, return the only number in the range that is missing from the array.",
        brute_force="Sort array in $O(N \\log N)$ or use a hash set in $O(N)$ space.",
        key_insight="XOR self-cancellation: $a \\oplus a = 0$ and $a \\oplus 0 = a$. XORing all expected numbers $0 \\dots n$ with all actual numbers in `nums` causes every present number to cancel out, leaving strictly the missing number in $O(1)$ space.",
        func_name="missing_number",
        stub_code="""def missing_number(nums: list[int]) -> int:
    \"\"\"Finds missing number in O(N) time, O(1) space using XOR.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def missing_number(nums: list[int]) -> int:
    \"\"\"Finds missing number in O(N) time, O(1) space using XOR.\"\"\"
    res = len(nums)
    for i, num in enumerate(nums):
        res ^= i ^ num
    return res
""",
        tests_code="""assert missing_number([3, 0, 1]) == 2
assert missing_number([0, 1]) == 2
assert missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
assert missing_number([0]) == 1
""",
        time_complexity="$O(N)$ single pass over array.",
        space_complexity="$O(1)$ constant space without risk of integer overflow.",
        follow_up="Could Gauss's summation formula $\\frac{n(n+1)}{2} - \\sum nums$ be used instead? Yes, though in fixed-width integers (C++/Java) XOR is safer as it eliminates integer overflow risks.",
        run_trace=trace_p75
    ))

    return problems
