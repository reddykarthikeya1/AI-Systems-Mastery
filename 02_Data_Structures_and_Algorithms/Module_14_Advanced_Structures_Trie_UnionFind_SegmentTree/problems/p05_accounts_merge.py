"""Problem 05 — Accounts Merge

Pattern:    Union-find over strings
Difficulty: Hard
Target:     Time O(E log E) for the sort, Space O(E)

Each account is ``[name, email1, email2, ...]``. Two accounts belong to the same
person if they share **any** email. Merge them.

Return each merged account as ``[name, *sorted_emails]``, and the list of
accounts sorted.

Constraints
- ``1 <= len(accounts) <= 1000``
- names may repeat across genuinely different people

Example
    [["John","a@x.com","b@x.com"], ["John","b@x.com","c@x.com"], ["Mary","m@x.com"]]
    -> [["John","a@x.com","b@x.com","c@x.com"], ["Mary","m@x.com"]]

Example:
    >>> accounts = [["John", "a@x.com", "b@x.com"], ["John", "b@x.com", "c@x.com"], ["Mary", "m@x.com"]]
    >>> accounts_merge(accounts)
    [['John', 'a@x.com', 'b@x.com', 'c@x.com'], ['Mary', 'm@x.com']]

Hints — read one at a time, and try again between each.

    Hint 1: Do NOT group by name - two different people can share a name. The emails are the identity.
    Hint 2: Union every email in an account with the account's first email. Then each connected component of emails is one person.
    Hint 3: Union-find over strings works by mapping each email to an integer index first. Keep an email -> name map to recover the name at the end.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations


def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    raise NotImplementedError("implement accounts_merge")
