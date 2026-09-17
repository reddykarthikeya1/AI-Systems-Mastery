"""Unit tests for SequenceDPEngine."""
from sequence_dp_engine import SequenceDPEngine


def test_longest_increasing_subsequence():
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    length, subseq = SequenceDPEngine.longest_increasing_subsequence(nums)
    assert length == 4
    assert len(subseq) == 4
    # Check that reconstructed subsequence is strictly increasing
    for i in range(len(subseq) - 1):
        assert subseq[i] < subseq[i + 1]

def test_coin_change_with_reconstruction():
    coins = [1, 2, 5]
    amount = 11
    count, chosen = SequenceDPEngine.coin_change_min_coins(coins, amount)
    assert count == 3
    assert sum(chosen) == 11
    assert set(chosen).issubset(set(coins))

    impossible_count, _ = SequenceDPEngine.coin_change_min_coins([2], 3)
    assert impossible_count == -1

def test_word_break():
    assert SequenceDPEngine.word_break("leetcode", ["leet", "code"])
    assert SequenceDPEngine.word_break("applepenapple", ["apple", "pen"])
    assert not SequenceDPEngine.word_break("catsandog", ["cats", "dog", "sand", "and", "cat"])

def test_lis_empty_and_single():
    assert SequenceDPEngine.longest_increasing_subsequence([]) == (0, [])
    assert SequenceDPEngine.longest_increasing_subsequence([42]) == (1, [42])

def test_coin_change_zero_amount():
    count, chosen = SequenceDPEngine.coin_change_min_coins([1, 2, 5], 0)
    assert count == 0
    assert chosen == []

def test_coin_change_negative_amount():
    count, chosen = SequenceDPEngine.coin_change_min_coins([1, 2, 5], -5)
    assert count == -1
    assert chosen == []
def test_lis_empty_and_duplicates_edge_cases():
    dp = SequenceDPEngine()
    assert dp.longest_increasing_subsequence([]) == (0, [])
    length, items = dp.longest_increasing_subsequence([42])
    assert length == 1
    assert items == [42]
    # Strictly increasing: duplicates cannot extend LIS
    assert dp.longest_increasing_subsequence([7, 7, 7, 7])[0] == 1
    # Strictly decreasing
    assert dp.longest_increasing_subsequence([5, 4, 3, 2, 1])[0] == 1


def test_coin_change_boundary_edge_cases():
    dp = SequenceDPEngine()
    # Amount 0 requires 0 coins
    assert dp.coin_change_min_coins([1, 2, 5], 0) == (0, [])
    # Amount cannot be formed
    assert dp.coin_change_min_coins([2], 3)[0] == -1
    # Exact single coin match
    assert dp.coin_change_min_coins([1, 5, 10], 10)[0] == 1



def test_word_break_edge_cases():
    dp = SequenceDPEngine()
    assert dp.word_break("", ["a", "b"]) is True
    assert dp.word_break("apple", ["orange", "banana"]) is False
    assert dp.word_break("aaaaaaa", ["aaaa", "aaa"]) is True
