from .models import Problem

def get_problems_01_15() -> list[Problem]:
    problems = []

    # ----------------------------------------------------
    # Problem 1: Two Sum
    # ----------------------------------------------------
    def trace_p01():
        nums = [2, 7, 11, 15]
        target = 9
        seen = {}
        out = [
            f"Input: nums = {nums}, target = {target}",
            f"{'Step':<5} | {'i':<3} | {'num':<5} | {'complement':<12} | {'seen map':<20} | {'Action':<15}",
            "-" * 68
        ]
        for i, num in enumerate(nums):
            comp = target - num
            if comp in seen:
                out.append(f"{i+1:<5} | {i:<3} | {num:<5} | {comp:<12} | {str(seen):<20} | Found! [{seen[comp]}, {i}]")
                break
            else:
                out.append(f"{i+1:<5} | {i:<3} | {num:<5} | {comp:<12} | {str(seen):<20} | Insert {num} -> {i}")
                seen[num] = i
        return "\n".join(out)

    problems.append(Problem(
        id=1,
        slug="p01_two_sum",
        title="Two Sum",
        category="Arrays & Hashing",
        difficulty="Easy",
        statement="Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. Each input has exactly one solution, and you may not use the same element twice.",
        brute_force="Iterate through all pairs $(i, j)$ with nested loops and check if `nums[i] + nums[j] == target`. Time: $O(N^2)$, Space: $O(1)$.",
        key_insight="As we scan each number $x$, the required complement is $target - x$. Store visited numbers and their indices in a hash map for $O(1)$ lookup time.",
        func_name="two_sum",
        stub_code="""def two_sum(nums: list[int], target: int) -> list[int]:
    \"\"\"Finds indices of two numbers that add up to target.
    
    Time: O(N), Space: O(N)
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def two_sum(nums: list[int], target: int) -> list[int]:
    \"\"\"Finds indices of two numbers that add up to target.
    
    Time: O(N), Space: O(N)
    \"\"\"
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
""",
        tests_code="""assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 2, 4], 6) == [1, 2]
assert two_sum([3, 3], 6) == [0, 1]
assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4]
""",
        time_complexity="$O(N)$ single-pass linear scan across $N$ elements.",
        space_complexity="$O(N)$ to store up to $N$ elements in the hash map.",
        follow_up="What if the input array is already sorted? Use Two Pointers (left = 0, right = N - 1) for $O(N)$ time and $O(1)$ auxiliary space.",
        run_trace=trace_p01
    ))

    # ----------------------------------------------------
    # Problem 2: Contains Duplicate
    # ----------------------------------------------------
    def trace_p02():
        nums = [1, 2, 3, 1]
        seen = set()
        out = [
            f"Input: nums = {nums}",
            f"{'Step':<5} | {'num':<5} | {'seen set':<18} | {'Status':<15}",
            "-" * 48
        ]
        for i, num in enumerate(nums):
            if num in seen:
                out.append(f"{i+1:<5} | {num:<5} | {str(sorted(list(seen))):<18} | Duplicate detected! True")
                break
            else:
                out.append(f"{i+1:<5} | {num:<5} | {str(sorted(list(seen))):<18} | Added to set")
                seen.add(num)
        return "\n".join(out)

    problems.append(Problem(
        id=2,
        slug="p02_contains_duplicate",
        title="Contains Duplicate",
        category="Arrays & Hashing",
        difficulty="Easy",
        statement="Given an integer array `nums`, return `True` if any value appears at least twice in the array, and return `False` if every element is distinct.",
        brute_force="Compare every pair with nested loops ($O(N^2)$ time, $O(1)$ space) or sort the array and check adjacent elements ($O(N \\log N)$ time, $O(1)$ space).",
        key_insight="Insert elements into a hash set. If an element is already in the set, a duplicate is found immediately in $O(1)$ average time.",
        func_name="contains_duplicate",
        stub_code="""def contains_duplicate(nums: list[int]) -> bool:
    \"\"\"Checks if any element appears at least twice.
    
    Time: O(N), Space: O(N)
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def contains_duplicate(nums: list[int]) -> bool:
    \"\"\"Checks if any element appears at least twice.
    
    Time: O(N), Space: O(N)
    \"\"\"
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
""",
        tests_code="""assert contains_duplicate([1, 2, 3, 1]) is True
assert contains_duplicate([1, 2, 3, 4]) is False
assert contains_duplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) is True
assert contains_duplicate([]) is False
""",
        time_complexity="$O(N)$ average time to scan array and insert into set.",
        space_complexity="$O(N)$ memory to store unique elements in the set.",
        follow_up="What if space must be $O(1)$ and modifying input is allowed? Sort in-place in $O(N \\log N)$ time and check adjacent items.",
        run_trace=trace_p02
    ))

    # ----------------------------------------------------
    # Problem 3: Valid Anagram
    # ----------------------------------------------------
    def trace_p03():
        s, t = "anagram", "nagaram"
        counts = {}
        for ch in s:
            counts[ch] = counts.get(ch, 0) + 1
        out = [
            f"Input: s = '{s}', t = '{t}'",
            f"Initial counts from s: {counts}",
            f"{'Char':<6} | {'Counts state after decrement':<35} | {'Valid?':<10}",
            "-" * 55
        ]
        c = dict(counts)
        for ch in t:
            c[ch] -= 1
            out.append(f"{ch:<6} | {str(c):<35} | {c[ch] >= 0}")
        out.append(f"All counts zero: {all(v == 0 for v in c.values())}")
        return "\n".join(out)

    problems.append(Problem(
        id=3,
        slug="p03_valid_anagram",
        title="Valid Anagram",
        category="Arrays & Hashing",
        difficulty="Easy",
        statement="Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise.",
        brute_force="Sort both strings and compare character-by-character. Time: $O(N \\log N)$, Space: $O(N)$ or $O(1)$ depending on sort implementation.",
        key_insight="An anagram has identical character frequency distributions. Compare frequency counters using an array of size 26 or a hash map.",
        func_name="is_anagram",
        stub_code="""def is_anagram(s: str, t: str) -> bool:
    \"\"\"Checks if t is an anagram of s.
    
    Time: O(N), Space: O(1) assuming fixed 26-char alphabet.
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def is_anagram(s: str, t: str) -> bool:
    \"\"\"Checks if t is an anagram of s.
    
    Time: O(N), Space: O(1) assuming fixed 26-char alphabet.
    \"\"\"
    if len(s) != len(t):
        return False
    counts: dict[str, int] = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in t:
        if ch not in counts or counts[ch] == 0:
            return False
        counts[ch] -= 1
    return True
""",
        tests_code="""assert is_anagram("anagram", "nagaram") is True
assert is_anagram("rat", "car") is False
assert is_anagram("a", "ab") is False
assert is_anagram("", "") is True
""",
        time_complexity="$O(N)$ where $N = \\text{len}(s)$. Single pass over both strings.",
        space_complexity="$O(1)$ auxiliary space since alphabet size is bounded by 26 ASCII characters ($O(k)$ for general Unicode).",
        follow_up="What if the inputs contain Unicode characters? Use a general hash map `dict[str, int]` instead of a fixed 26-element array.",
        run_trace=trace_p03
    ))

    # ----------------------------------------------------
    # Problem 4: Group Anagrams
    # ----------------------------------------------------
    def trace_p04():
        strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
        out = [
            f"Input: {strs}",
            f"{'Word':<6} | {'Key (Sorted/Tuple)':<20} | {'Groups Count':<12}",
            "-" * 42
        ]
        groups = {}
        for w in strs:
            key = "".join(sorted(w))
            groups.setdefault(key, []).append(w)
            out.append(f"{w:<6} | {key:<20} | {len(groups):<12}")
        out.append(f"Result: {list(groups.values())}")
        return "\n".join(out)

    problems.append(Problem(
        id=4,
        slug="p04_group_anagrams",
        title="Group Anagrams",
        category="Arrays & Hashing",
        difficulty="Medium",
        statement="Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.",
        brute_force="For each pair of strings, check if they are anagrams. Time: $O(N^2 \\cdot K)$, Space: $O(N \\cdot K)$.",
        key_insight="Anagrams share the exact same character frequency counts. Use a 26-character count tuple (or sorted string) as the hash map key to bucket words.",
        func_name="group_anagrams",
        stub_code="""def group_anagrams(strs: list[str]) -> list[list[str]]:
    \"\"\"Groups strings that are anagrams of each other.
    
    Time: O(N * K), Space: O(N * K)
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def group_anagrams(strs: list[str]) -> list[list[str]]:
    \"\"\"Groups strings that are anagrams of each other.
    
    Time: O(N * K), Space: O(N * K)
    \"\"\"
    groups: dict[tuple[int, ...], list[str]] = {}
    for s in strs:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1
        key = tuple(count)
        groups.setdefault(key, []).append(s)
    return list(groups.values())
""",
        tests_code="""res1 = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
assert sorted([sorted(g) for g in res1]) == sorted([["bat"], ["nat", "tan"], ["ate", "eat", "tea"]])
assert group_anagrams([""]) == [[""]]
assert group_anagrams(["a"]) == [["a"]]
""",
        time_complexity="$O(N \\cdot K)$ where $N$ is number of strings and $K$ is maximum string length.",
        space_complexity="$O(N \\cdot K)$ to store strings grouped in the hash table.",
        follow_up="What if character set is arbitrary UTF-8 strings? Sort each word in $O(K \\log K)$ to form the key, yielding $O(N K \\log K)$ time.",
        run_trace=trace_p04
    ))

    # ----------------------------------------------------
    # Problem 5: Top K Frequent Elements
    # ----------------------------------------------------
    def trace_p05():
        nums, k = [1, 1, 1, 2, 2, 3], 2
        counts = {1: 3, 2: 2, 3: 1}
        buckets = [[] for _ in range(len(nums) + 1)]
        for val, freq in counts.items():
            buckets[freq].append(val)
        out = [
            f"Input: nums = {nums}, k = {k}",
            f"Frequencies: {counts}",
            f"Buckets (index = frequency):",
        ]
        for f in range(len(buckets) - 1, 0, -1):
            if buckets[f]:
                out.append(f"  Freq {f}: {buckets[f]}")
        out.append("Extracting top 2 elements from highest frequency downwards: [1, 2]")
        return "\n".join(out)

    problems.append(Problem(
        id=5,
        slug="p05_top_k_frequent",
        title="Top K Frequent Elements",
        category="Arrays & Hashing",
        difficulty="Medium",
        statement="Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.",
        brute_force="Count frequencies with a hash map, then sort all unique items by frequency in descending order. Time: $O(N \\log N)$, Space: $O(N)$.",
        key_insight="Use Bucket Sort where index represents frequency (from $0$ to $N$). Since maximum frequency is $N$, filling and reverse-scanning buckets takes strictly $O(N)$ linear time.",
        func_name="top_k_frequent",
        stub_code="""def top_k_frequent(nums: list[int], k: int) -> list[int]:
    \"\"\"Returns the k most frequent elements using bucket sort.
    
    Time: O(N), Space: O(N)
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def top_k_frequent(nums: list[int], k: int) -> list[int]:
    \"\"\"Returns the k most frequent elements using bucket sort.
    
    Time: O(N), Space: O(N)
    \"\"\"
    counts: dict[int, int] = {}
    for num in nums:
        counts[num] = counts.get(num, 0) + 1
    
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for val, freq in counts.items():
        buckets[freq].append(val)
    
    res: list[int] = []
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            res.append(num)
            if len(res) == k:
                return res
    return res
""",
        tests_code="""assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
assert top_k_frequent([1], 1) == [1]
assert sorted(top_k_frequent([4, 1, -1, 2, -1, 2, 3], 2)) == [-1, 2]
""",
        time_complexity="$O(N)$ time using frequency bucket sorting.",
        space_complexity="$O(N)$ space for count hash map and frequency buckets.",
        follow_up="What if $k \\ll N$ and data is streaming? Maintain a min-heap of size $k$ in $O(N \\log k)$ time and $O(k)$ memory.",
        run_trace=trace_p05
    ))

    # ----------------------------------------------------
    # Problem 6: Product of Array Except Self
    # ----------------------------------------------------
    def trace_p06():
        nums = [1, 2, 3, 4]
        n = len(nums)
        res = [1] * n
        prefix = 1
        out = [
            f"Input: {nums}",
            "--- Prefix Pass (left-to-right) ---"
        ]
        for i in range(n):
            res[i] = prefix
            out.append(f"i = {i} | res[{i}] = prefix ({prefix}) | prefix *= nums[{i}] -> {prefix * nums[i]}")
            prefix *= nums[i]
        out.append(f"res after prefix: {res}")
        out.append("--- Suffix Pass (right-to-left) ---")
        suffix = 1
        for i in range(n - 1, -1, -1):
            out.append(f"i = {i} | res[{i}] = res[{i}] * suffix ({res[i]} * {suffix} = {res[i] * suffix})")
            res[i] *= suffix
            suffix *= nums[i]
        out.append(f"Final output: {res}")
        return "\n".join(out)

    problems.append(Problem(
        id=6,
        slug="p06_product_except_self",
        title="Product of Array Except Self",
        category="Arrays & Hashing",
        difficulty="Medium",
        statement="Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`. Must run in $O(N)$ time without using division.",
        brute_force="For each index $i$, iterate through all other indices $j \\ne i$ and multiply their values. Time: $O(N^2)$, Space: $O(1)$.",
        key_insight="Any element's product except self equals $(\\text{prefix product to left of } i) \\times (\\text{suffix product to right of } i)$. Build the result in-place using two sequential passes.",
        func_name="product_except_self",
        stub_code="""def product_except_self(nums: list[int]) -> list[int]:
    \"\"\"Computes product of array except self without division.
    
    Time: O(N), Space: O(1) auxiliary (output array excluded)
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def product_except_self(nums: list[int]) -> list[int]:
    \"\"\"Computes product of array except self without division.
    
    Time: O(N), Space: O(1) auxiliary (output array excluded)
    \"\"\"
    n = len(nums)
    res = [1] * n
    
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]
        
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
        
    return res
""",
        tests_code="""assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
assert product_except_self([2, 3]) == [3, 2]
""",
        time_complexity="$O(N)$ with two linear passes.",
        space_complexity="$O(1)$ auxiliary memory (output array does not count toward space complexity).",
        follow_up="How to handle multiple zeros in the array? The prefix/suffix logic naturally handles zero, one, or multiple zeros without divide-by-zero errors.",
        run_trace=trace_p06
    ))

    # ----------------------------------------------------
    # Problem 7: Encode and Decode Strings
    # ----------------------------------------------------
    def trace_p07():
        strs = ["lint", "code", "love", "you"]
        encoded = "".join(f"{len(s)}#{s}" for s in strs)
        out = [
            f"Input strings: {strs}",
            f"Encoded string: '{encoded}'",
            f"{'Step':<5} | {'Delimiter Pos':<15} | {'Length':<8} | {'Extracted Word':<15}",
            "-" * 48
        ]
        i = 0
        step = 1
        while i < len(encoded):
            j = encoded.find("#", i)
            length = int(encoded[i:j])
            word = encoded[j + 1 : j + 1 + length]
            out.append(f"{step:<5} | {j:<15} | {length:<8} | '{word}'")
            i = j + 1 + length
            step += 1
        return "\n".join(out)

    problems.append(Problem(
        id=7,
        slug="p07_encode_and_decode_strings",
        title="Encode and Decode Strings",
        category="Arrays & Hashing",
        difficulty="Medium",
        statement="Design an algorithm to encode a list of strings to a single string, and decode that string back to the original list of strings. The strings can contain any possible characters, including delimiters like '#' and commas.",
        brute_force="Using a fixed delimiter like comma or semicolon breaks immediately if strings contain that delimiter.",
        key_insight="Prefix each string with its length and a delimiter: `<length>#<string>`. When decoding, reading `<length>` tells exactly how many subsequent bytes belong to the word regardless of characters inside it.",
        func_name="encode_decode",
        stub_code="""class Codec:
    def encode(self, strs: list[str]) -> str:
        raise NotImplementedError
    def decode(self, s: str) -> list[str]:
        raise NotImplementedError
""",
        solution_code="""class Codec:
    def encode(self, strs: list[str]) -> str:
        \"\"\"Encodes a list of strings to a single string.\"\"\"
        res = []
        for s in strs:
            res.append(f"{len(s)}#{s}")
        return "".join(res)

    def decode(self, s: str) -> list[str]:
        \"\"\"Decodes a single string to a list of strings.\"\"\"
        res = []
        i = 0
        while i < len(s):
            j = s.find("#", i)
            length = int(s[i:j])
            word = s[j + 1 : j + 1 + length]
            res.append(word)
            i = j + 1 + length
        return res
""",
        tests_code="""c = Codec()
assert c.decode(c.encode(["lint", "code", "love", "you"])) == ["lint", "code", "love", "you"]
assert c.decode(c.encode(["#", "##", "3#cat"])) == ["#", "##", "3#cat"]
assert c.decode(c.encode(["", ""])) == ["", ""]
assert c.decode(c.encode([])) == []
""",
        time_complexity="$O(N)$ total characters processed during encode and decode.",
        space_complexity="$O(1)$ auxiliary space beyond storing the output strings.",
        follow_up="How does this protocol compare to HTTP chunked transfer encoding? It uses the exact same framing principle (hex length + CRLF + payload).",
        run_trace=trace_p07
    ))

    # ----------------------------------------------------
    # Problem 8: Longest Consecutive Sequence
    # ----------------------------------------------------
    def trace_p08():
        nums = [100, 4, 200, 1, 3, 2]
        num_set = set(nums)
        out = [
            f"Input: {nums}",
            f"Set: {num_set}",
            f"{'Num':<5} | {'Is Sequence Start? (x-1 not in set)':<35} | {'Streak Length':<15}",
            "-" * 60
        ]
        longest = 0
        for num in nums:
            is_start = (num - 1) not in num_set
            streak = 0
            if is_start:
                curr = num
                while curr in num_set:
                    curr += 1
                    streak += 1
                longest = max(longest, streak)
                out.append(f"{num:<5} | {str(is_start):<35} | {streak} (explored {list(range(num, curr))})")
            else:
                out.append(f"{num:<5} | {str(is_start):<35} | Skipped")
        out.append(f"Max streak: {longest}")
        return "\n".join(out)

    problems.append(Problem(
        id=8,
        slug="p08_longest_consecutive_sequence",
        title="Longest Consecutive Sequence",
        category="Arrays & Hashing",
        difficulty="Medium",
        statement="Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence. Must run in $O(N)$ time.",
        brute_force="Sort the array and count longest adjacent run. Time: $O(N \\log N)$, Space: $O(1)$ or $O(N)$.",
        key_insight="Insert all numbers into a hash set. Only begin counting a streak if `num - 1` is NOT in the set (i.e. `num` is the start of a streak). Each number is visited at most twice.",
        func_name="longest_consecutive",
        stub_code="""def longest_consecutive(nums: list[int]) -> int:
    \"\"\"Finds length of longest consecutive sequence in O(N) time.\"\"\"
    raise NotImplementedError
""",
        solution_code="""def longest_consecutive(nums: list[int]) -> int:
    \"\"\"Finds length of longest consecutive sequence in O(N) time.\"\"\"
    num_set = set(nums)
    longest = 0
    
    for num in num_set:
        # Check if num is the start of a sequence
        if (num - 1) not in num_set:
            current_num = num
            current_streak = 1
            while (current_num + 1) in num_set:
                current_num += 1
                current_streak += 1
            longest = max(longest, current_streak)
            
    return longest
""",
        tests_code="""assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
assert longest_consecutive([]) == 0
assert longest_consecutive([1, 2, 0, 1]) == 3
""",
        time_complexity="$O(N)$ time because each number is only checked as a sequence start once.",
        space_complexity="$O(N)$ memory to store unique numbers in the hash set.",
        follow_up="Could you use Union-Find (Disjoint Set Union) instead? Yes, union `num` with `num + 1` if present, maintaining component sizes in $O(N \\alpha(N))$ time.",
        run_trace=trace_p08
    ))

    # ----------------------------------------------------
    # Problem 9: Valid Palindrome
    # ----------------------------------------------------
    def trace_p09():
        s = "A man, a plan, a canal: Panama"
        out = [
            f"Input: '{s}'",
            f"{'left':<5} | {'ch[left]':<10} | {'right':<5} | {'ch[right]':<10} | {'Match?':<10}",
            "-" * 48
        ]
        l, r = 0, len(s) - 1
        while l < r:
            while l < r and not s[l].isalnum():
                l += 1
            while l < r and not s[r].isalnum():
                r -= 1
            if l < r:
                match = s[l].lower() == s[r].lower()
                out.append(f"{l:<5} | '{s[l]}' ({s[l].lower()}) | {r:<5} | '{s[r]}' ({s[r].lower()}) | {match}")
                l += 1
                r -= 1
        return "\n".join(out)

    problems.append(Problem(
        id=9,
        slug="p09_valid_palindrome",
        title="Valid Palindrome",
        category="Two Pointers",
        difficulty="Easy",
        statement="A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.",
        brute_force="Filter the string into a new cleaned string and reverse it. Time: $O(N)$, Space: $O(N)$ extra memory.",
        key_insight="Use two pointers starting at left and right extremes. Advance inward skipping non-alphanumeric characters, comparing lowercased characters in-place with $O(1)$ space.",
        func_name="is_palindrome",
        stub_code="""def is_palindrome(s: str) -> bool:
    \"\"\"Checks if string is palindrome ignoring non-alphanumeric chars.
    
    Time: O(N), Space: O(1)
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def is_palindrome(s: str) -> bool:
    \"\"\"Checks if string is palindrome ignoring non-alphanumeric chars.
    
    Time: O(N), Space: O(1)
    \"\"\"
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
""",
        tests_code="""assert is_palindrome("A man, a plan, a canal: Panama") is True
assert is_palindrome("race a car") is False
assert is_palindrome(" ") is True
assert is_palindrome("0P") is False
""",
        time_complexity="$O(N)$ single pass across length $N$.",
        space_complexity="$O(1)$ auxiliary space without allocating a cleaned string.",
        follow_up="What if you are allowed to remove at most one character to form a valid palindrome? Recursively check the two branches (`left + 1` or `right - 1`) on first mismatch.",
        run_trace=trace_p09
    ))

    # ----------------------------------------------------
    # Problem 10: 3Sum
    # ----------------------------------------------------
    def trace_p10():
        nums = [-1, 0, 1, 2, -1, -4]
        nums.sort()
        out = [
            f"Sorted input: {nums}",
            f"{'i':<3} | {'nums[i]':<8} | {'left':<5} | {'right':<5} | {'Sum':<6} | {'Action':<25}",
            "-" * 55
        ]
        res = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            l, r = i + 1, len(nums) - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s == 0:
                    out.append(f"{i:<3} | {nums[i]:<8} | {l:<5} | {r:<5} | {s:<6} | Found! [{nums[i]},{nums[l]},{nums[r]}]")
                    res.append([nums[i], nums[l], nums[r]])
                    l += 1
                    r -= 1
                    while l < r and nums[l] == nums[l - 1]:
                        l += 1
                    while l < r and nums[r] == nums[r + 1]:
                        r -= 1
                elif s < 0:
                    out.append(f"{i:<3} | {nums[i]:<8} | {l:<5} | {r:<5} | {s:<6} | sum < 0 -> left++")
                    l += 1
                else:
                    out.append(f"{i:<3} | {nums[i]:<8} | {l:<5} | {r:<5} | {s:<6} | sum > 0 -> right--")
                    r -= 1
        return "\n".join(out)

    problems.append(Problem(
        id=10,
        slug="p10_three_sum",
        title="3Sum",
        category="Two Pointers",
        difficulty="Medium",
        statement="Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`. The solution set must not contain duplicate triplets.",
        brute_force="Generate all triplets with 3 nested loops and store them in a set to avoid duplicates. Time: $O(N^3)$, Space: $O(N)$.",
        key_insight="Sort the array in $O(N \\log N)$. Fix element $i$, then use two pointers (`left = i + 1`, `right = N - 1`) to find pairs adding to `-nums[i]`. Skip duplicate adjacent elements to avoid duplicate triplets.",
        func_name="three_sum",
        stub_code="""def three_sum(nums: list[int]) -> list[list[int]]:
    \"\"\"Finds all unique triplets that sum to zero.
    
    Time: O(N^2), Space: O(1) auxiliary
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def three_sum(nums: list[int]) -> list[list[int]]:
    \"\"\"Finds all unique triplets that sum to zero.
    
    Time: O(N^2), Space: O(1) auxiliary
    \"\"\"
    nums.sort()
    res: list[list[int]] = []
    
    for i in range(len(nums) - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue
            
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                res.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
                
    return res
""",
        tests_code="""assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
assert three_sum([0, 1, 1]) == []
assert three_sum([0, 0, 0]) == [[0, 0, 0]]
""",
        time_complexity="$O(N^2)$ time ($O(N \\log N)$ sort + $N$ iterations of two-pointer scans).",
        space_complexity="$O(1)$ auxiliary space (or $O(N)$ depending on sorting algorithm implementation).",
        follow_up="How to extend to 4Sum or KSum? Recursively reduce KSum to $(K-1)\\text{Sum}$ until reaching 2Sum base case with two pointers in $O(N^{K-1})$.",
        run_trace=trace_p10
    ))

    # ----------------------------------------------------
    # Problem 11: Container With Most Water
    # ----------------------------------------------------
    def trace_p11():
        height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
        l, r = 0, len(height) - 1
        max_a = 0
        out = [
            f"Input: {height}",
            f"{'Step':<5} | {'left':<5} | {'right':<5} | {'h[l]':<5} | {'h[r]':<5} | {'width':<6} | {'area':<6} | {'max_area':<9} | {'Move':<10}",
            "-" * 65
        ]
        step = 1
        while l < r:
            w = r - l
            h = min(height[l], height[r])
            area = w * h
            max_a = max(max_a, area)
            move = "left++" if height[l] < height[r] else "right--"
            out.append(f"{step:<5} | {l:<5} | {r:<5} | {height[l]:<5} | {height[r]:<5} | {w:<6} | {area:<6} | {max_a:<9} | {move:<10}")
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
            step += 1
        return "\n".join(out)

    problems.append(Problem(
        id=11,
        slug="p11_container_with_most_water",
        title="Container With Most Water",
        category="Two Pointers",
        difficulty="Medium",
        statement="You are given an integer array `height` of length $n$. Find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store.",
        brute_force="Compute area for all pairs $(i, j)$ where $\\text{area} = (j - i) \\times \\min(h[i], h[j])$. Time: $O(N^2)$, Space: $O(1)$.",
        key_insight="The width is initially maximized by placing pointers at $0$ and $N - 1$. The height is constrained by the shorter wall. Moving the taller wall can only decrease width without increasing height. Therefore, greedily advance the shorter wall inward.",
        func_name="max_area",
        stub_code="""def max_area(height: list[int]) -> int:
    \"\"\"Finds maximum water container capacity using two pointers.
    
    Time: O(N), Space: O(1)
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def max_area(height: list[int]) -> int:
    \"\"\"Finds maximum water container capacity using two pointers.
    
    Time: O(N), Space: O(1)
    \"\"\"
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)
        
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
            
    return max_water
""",
        tests_code="""assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
assert max_area([1, 1]) == 1
assert max_area([4, 3, 2, 1, 4]) == 16
assert max_area([1, 2, 1]) == 2
""",
        time_complexity="$O(N)$ single pass as pointers move inward until they meet.",
        space_complexity="$O(1)$ constant memory.",
        follow_up="What if you need to return the container indices instead of just area? Track the `(best_left, best_right)` pair whenever `max_water` updates.",
        run_trace=trace_p11
    ))

    # ----------------------------------------------------
    # Problem 12: Trapping Rain Water (FIXED EXACT TRACE)
    # ----------------------------------------------------
    def trace_p12():
        height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
        left, right = 0, len(height) - 1
        max_left, max_right = 0, 0
        total_water = 0
        step = 1
        out = [
            f"Input: height = {height}",
            f"{'Step':<5} | {'Branch':<7} | {'left':<4} | {'right':<5} | {'h[l]':<4} | {'h[r]':<4} | {'max_l':<5} | {'max_r':<5} | {'Added':<5} | {'Total':<5}",
            "-" * 70
        ]
        while left < right:
            if height[left] < height[right]:
                if height[left] >= max_left:
                    max_left = height[left]
                    added = 0
                else:
                    added = max_left - height[left]
                    total_water += added
                out.append(f"{step:<5} | {'Left':<7} | {left:<4} | {right:<5} | {height[left]:<4} | {height[right]:<4} | {max_left:<5} | {max_right:<5} | {added:<5} | {total_water:<5}")
                left += 1
            else:
                if height[right] >= max_right:
                    max_right = height[right]
                    added = 0
                else:
                    added = max_right - height[right]
                    total_water += added
                out.append(f"{step:<5} | {'Right':<7} | {left:<4} | {right:<5} | {height[left]:<4} | {height[right]:<4} | {max_left:<5} | {max_right:<5} | {added:<5} | {total_water:<5}")
                right -= 1
            step += 1
        out.append(f"Final Trapped Water: {total_water}")
        return "\n".join(out)

    problems.append(Problem(
        id=12,
        slug="p12_trapping_rain_water",
        title="Trapping Rain Water",
        category="Two Pointers",
        difficulty="Hard",
        statement="Given $n$ non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        brute_force="For each bar $i$, find the maximum to its left and maximum to its right with linear scans: $\\text{water}[i] = \\max(0, \\min(L_{\\max}, R_{\\max}) - h[i])$. Time: $O(N^2)$, Space: $O(1)$.",
        key_insight="Water trapped at index $i$ depends strictly on $\\min(\\text{max\\_left}, \\text{max\\_right})$. With two pointers, whichever side has the smaller running maximum determines the water bound, allowing in-place computation with $O(1)$ space.",
        func_name="trap_rain_water",
        stub_code="""def trap_rain_water(height: list[int]) -> int:
    \"\"\"Computes trapped rain water in O(N) time and O(1) space.
    
    Time: O(N), Space: O(1)
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def trap_rain_water(height: list[int]) -> int:
    \"\"\"Computes trapped rain water in O(N) time and O(1) space.
    
    Time: O(N), Space: O(1)
    \"\"\"
    if not height:
        return 0

    left, right = 0, len(height) - 1
    max_left, max_right = 0, 0
    total_water = 0

    while left < right:
        if height[left] < height[right]:
            if height[left] >= max_left:
                max_left = height[left]
            else:
                total_water += max_left - height[left]
            left += 1
        else:
            if height[right] >= max_right:
                max_right = height[right]
            else:
                total_water += max_right - height[right]
            right -= 1

    return total_water
""",
        tests_code="""assert trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
assert trap_rain_water([4, 2, 0, 3, 2, 5]) == 9
assert trap_rain_water([]) == 0
assert trap_rain_water([3, 3, 3]) == 0
""",
        time_complexity="$O(N)$ linear time; every bar is processed exactly once.",
        space_complexity="$O(1)$ space using two pointers.",
        follow_up="How to solve Trapping Rain Water in 2D (a 2D elevation grid)? Use a Min-Heap initialized with all boundary cells; pop the lowest boundary wall and traverse neighbors (Dijkstra's variant) in $O(R \\cdot C \\log(R \\cdot C))$ time.",
        run_trace=trace_p12
    ))

    # ----------------------------------------------------
    # Problem 13: Best Time to Buy and Sell Stock
    # ----------------------------------------------------
    def trace_p13():
        prices = [7, 1, 5, 3, 6, 4]
        min_p = float("inf")
        max_p = 0
        out = [
            f"Input: prices = {prices}",
            f"{'Day':<5} | {'Price':<6} | {'Min Price Seen':<16} | {'Potential Profit':<18} | {'Max Profit':<12}",
            "-" * 65
        ]
        for day, p in enumerate(prices):
            min_p = min(min_p, p)
            profit = p - min_p
            max_p = max(max_p, profit)
            out.append(f"{day+1:<5} | {p:<6} | {min_p:<16} | {profit:<18} | {max_p:<12}")
        return "\n".join(out)

    problems.append(Problem(
        id=13,
        slug="p13_best_time_to_buy_and_sell_stock",
        title="Best Time to Buy and Sell Stock",
        category="Sliding Window",
        difficulty="Easy",
        statement="You are given an array `prices` where `prices[i]` is the price of a given stock on the $i^{\\text{th}}$ day. Maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.",
        brute_force="Try every pair $(i, j)$ with $i < j$ and compute $\\text{profit} = \\text{prices}[j] - \\text{prices}[i]$. Time: $O(N^2)$, Space: $O(1)$.",
        key_insight="Maintain the running minimum purchase price seen so far. At each day $i$, the maximum profit attainable by selling on day $i$ is $\\text{prices}[i] - \\text{min\\_price}$.",
        func_name="max_profit",
        stub_code="""def max_profit(prices: list[int]) -> int:
    \"\"\"Calculates maximum profit from a single buy and sell transaction.
    
    Time: O(N), Space: O(1)
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def max_profit(prices: list[int]) -> int:
    \"\"\"Calculates maximum profit from a single buy and sell transaction.
    
    Time: O(N), Space: O(1)
    \"\"\"
    min_price = float("inf")
    max_profit = 0
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
    return max_profit
""",
        tests_code="""assert max_profit([7, 1, 5, 3, 6, 4]) == 5
assert max_profit([7, 6, 4, 3, 1]) == 0
assert max_profit([1, 2]) == 1
assert max_profit([]) == 0
""",
        time_complexity="$O(N)$ single pass over array.",
        space_complexity="$O(1)$ constant auxiliary memory.",
        follow_up="What if you can complete as many transactions as you like (Stock II)? Accumulate every positive adjacent price increment: $\\sum \\max(0, prices[i] - prices[i-1])$.",
        run_trace=trace_p13
    ))

    # ----------------------------------------------------
    # Problem 14: Longest Substring Without Repeating Characters
    # ----------------------------------------------------
    def trace_p14():
        s = "abcabcbb"
        last_seen = {}
        left = 0
        max_l = 0
        out = [
            f"Input: '{s}'",
            f"{'right':<5} | {'char':<5} | {'left':<5} | {'last_seen[char]':<18} | {'Window Substring':<18} | {'max_len':<8}",
            "-" * 68
        ]
        for right, ch in enumerate(s):
            prev = last_seen.get(ch, None)
            if ch in last_seen and last_seen[ch] >= left:
                left = last_seen[ch] + 1
            last_seen[ch] = right
            window = s[left : right + 1]
            max_l = max(max_l, len(window))
            out.append(f"{right:<5} | '{ch}'   | {left:<5} | {str(prev):<18} | '{window}'{' '*(16-len(window))} | {max_l:<8}")
        return "\n".join(out)

    problems.append(Problem(
        id=14,
        slug="p14_longest_substring_without_repeating_characters",
        title="Longest Substring Without Repeating Characters",
        category="Sliding Window",
        difficulty="Medium",
        statement="Given a string `s`, find the length of the longest substring without duplicate characters.",
        brute_force="Generate all substrings $O(N^2)$ and check if each has unique characters $O(N)$. Time: $O(N^3)$, Space: $O(N)$.",
        key_insight="Maintain a dynamic sliding window $[\\text{left}, \\text{right}]$ and a hash map of characters to their most recent index. When character $s[\\text{right}]$ is seen inside the window, jump $\\text{left}$ to $\\text{last\\_seen}[c] + 1$.",
        func_name="length_of_longest_substring",
        stub_code="""def length_of_longest_substring(s: str) -> int:
    \"\"\"Finds length of longest substring without duplicate characters.
    
    Time: O(N), Space: O(min(N, M))
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def length_of_longest_substring(s: str) -> int:
    \"\"\"Finds length of longest substring without duplicate characters.
    
    Time: O(N), Space: O(min(N, M))
    \"\"\"
    last_seen: dict[str, int] = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len
""",
        tests_code="""assert length_of_longest_substring("abcabcbb") == 3
assert length_of_longest_substring("bbbbb") == 1
assert length_of_longest_substring("pwwkew") == 3
assert length_of_longest_substring("") == 0
""",
        time_complexity="$O(N)$ linear time; both pointers advance strictly to the right.",
        space_complexity="$O(\\min(N, M))$ where $M$ is alphabet size.",
        follow_up="What if at most $K$ distinct characters are permitted? Use a frequency counter hash map; shrink window while $\\text{len}(\\text{counts}) > K$.",
        run_trace=trace_p14
    ))

    # ----------------------------------------------------
    # Problem 15: Longest Repeating Character Replacement
    # ----------------------------------------------------
    def trace_p15():
        s = "AABABBA"
        k = 1
        counts = {}
        left = 0
        max_f = 0
        max_l = 0
        out = [
            f"Input: s = '{s}', k = {k}",
            f"{'right':<5} | {'char':<5} | {'counts':<16} | {'max_freq':<9} | {'Window Len':<11} | {'Valid?':<7} | {'left':<5}",
            "-" * 65
        ]
        for right, ch in enumerate(s):
            counts[ch] = counts.get(ch, 0) + 1
            max_f = max(max_f, counts[ch])
            window_len = right - left + 1
            valid = (window_len - max_f) <= k
            if not valid:
                counts[s[left]] -= 1
                left += 1
            max_l = max(max_l, right - left + 1)
            out.append(f"{right:<5} | '{ch}'   | {str(counts):<16} | {max_f:<9} | {window_len:<11} | {str(valid):<7} | {left:<5}")
        return "\n".join(out)

    problems.append(Problem(
        id=15,
        slug="p15_longest_repeating_character_replacement",
        title="Longest Repeating Character Replacement",
        category="Sliding Window",
        difficulty="Medium",
        statement="You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character at most `k` times. Return the length of the longest substring containing the same letter you can get after performing above operations.",
        brute_force="Examine every substring, count frequencies, and verify if $(\\text{length} - \\text{max\\_freq}) \\le k$. Time: $O(N^2 \\cdot 26)$, Space: $O(26)$.",
        key_insight="A window $[\\text{left}, \\text{right}]$ is valid if $\\text{window\\_size} - \\text{max\\_frequency} \\le k$. When this condition is violated, shrink the window from the left by one step.",
        func_name="character_replacement",
        stub_code="""def character_replacement(s: str, k: int) -> int:
    \"\"\"Finds longest repeating character substring after at most k replacements.
    
    Time: O(N), Space: O(1)
    \"\"\"
    raise NotImplementedError
""",
        solution_code="""def character_replacement(s: str, k: int) -> int:
    \"\"\"Finds longest repeating character substring after at most k replacements.
    
    Time: O(N), Space: O(1)
    \"\"\"
    counts: dict[str, int] = {}
    left = 0
    max_freq = 0
    max_len = 0
    
    for right in range(len(s)):
        ch = s[right]
        counts[ch] = counts.get(ch, 0) + 1
        max_freq = max(max_freq, counts[ch])
        
        while (right - left + 1) - max_freq > k:
            counts[s[left]] -= 1
            left += 1
            
        max_len = max(max_len, right - left + 1)
        
    return max_len
""",
        tests_code="""assert character_replacement("ABAB", 2) == 4
assert character_replacement("AABABBA", 1) == 4
assert character_replacement("AAAA", 2) == 4
assert character_replacement("ABBB", 2) == 4
""",
        time_complexity="$O(N)$ since both pointers only advance forward.",
        space_complexity="$O(1)$ auxiliary space bounded by 26 English uppercase characters.",
        follow_up="Do we need to decrement `max_freq` when shrinking the window? No! A new maximum window length can only be achieved if `max_freq` strictly increases beyond its previous peak.",
        run_trace=trace_p15
    ))

    return problems
