"""Reference solution — Problem 05: Accounts Merge

Pattern:    Union-find over strings
Complexity: Time O(E log E) for the sort, Space O(E)
"""

from __future__ import annotations


def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    # Map each distinct email to an index so union-find can work on integers.
    index: dict[str, int] = {}
    owner: dict[str, str] = {}
    for account in accounts:
        name = account[0]
        for email in account[1:]:
            if email not in index:
                index[email] = len(index)
            owner[email] = name

    parent = list(range(len(index)))

    def find(x: int) -> int:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    # Emails within one account belong together. Names are NOT used to group:
    # two different people can share a name.
    for account in accounts:
        emails = account[1:]
        for email in emails[1:]:
            ra, rb = find(index[emails[0]]), find(index[email])
            if ra != rb:
                parent[rb] = ra

    groups: dict[int, list[str]] = {}
    for email, i in index.items():
        groups.setdefault(find(i), []).append(email)

    out = [[owner[emails[0]], *sorted(emails)] for emails in groups.values()]
    return sorted(out)
