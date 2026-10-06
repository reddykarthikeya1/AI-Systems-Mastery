"""Chapter 17 - Columnar data engineering (pure Python models of what Polars/DuckDB/Arrow do).

1. group_sum: aggregate column-wise, without building row dictionaries.
2. dictionary_encode / dictionary_decode / run_length_encode: the encodings behind columnar compression.
3. column_mean (debugging): the average of a column with NULLs is wrong.
"""

BUGGY = {
    "column_mean": '''def column_mean(values):
    """Mean of the non-None values (zeros count as values). Returns None when there are no non-None values."""
    return sum(v for v in values if v) / len(values)''',
}


def group_sum(columns, key, value):
    """`columns` is {name: list}. Return {key_value: sum of `value` column} computed by zipping the two columns.
    Rows whose value is None are skipped (but the key still appears with 0 if all its values are None)."""
    out = {}
    for k, v in zip(columns[key], columns[value]):
        out.setdefault(k, 0)
        if v is not None:
            out[k] += v
    return out


def dictionary_encode(values):
    """Return (dictionary, codes): dictionary lists distinct values in first-seen order, codes[i] is the dictionary index of values[i]."""
    index, codes = {}, []
    for v in values:
        codes.append(index.setdefault(v, len(index)))
    return list(index), codes


def dictionary_decode(dictionary, codes):
    """Inverse of dictionary_encode."""
    return [dictionary[c] for c in codes]


def run_length_encode(values):
    """[a, a, b, a] -> [(a, 2), (b, 1), (a, 1)]. Empty input gives []."""
    out = []
    for v in values:
        if out and out[-1][0] == v:
            out[-1] = (v, out[-1][1] + 1)
        else:
            out.append((v, 1))
    return out


def column_mean(values):
    """Mean of the non-None values (zeros count as values). Returns None when there are no non-None values."""
    present = [v for v in values if v is not None]
    return sum(present) / len(present) if present else None


def t_group_sum_with_nulls(m):
    cols = {"city": ["a", "b", "a", "c", "b"], "amt": [1, 2, 3, None, 4]}
    assert m.group_sum(cols, "city", "amt") == {"a": 4, "b": 6, "c": 0}
    assert m.group_sum({"k": [], "v": []}, "k", "v") == {}


def t_dictionary_roundtrip(m):
    vals = ["x", "y", "x", "z", "y", "x"]
    d, codes = m.dictionary_encode(vals)
    assert d == ["x", "y", "z"] and codes == [0, 1, 0, 2, 1, 0]
    assert m.dictionary_decode(d, codes) == vals
    assert m.dictionary_encode([]) == ([], [])


def t_run_length(m):
    assert m.run_length_encode(list("aabaaa")) == [("a", 2), ("b", 1), ("a", 3)]
    assert m.run_length_encode([]) == []
    d, codes = m.dictionary_encode(["u"] * 1000)
    assert m.run_length_encode(codes) == [(0, 1000)]


def t_column_mean_nulls_and_zeros(m):
    assert m.column_mean([0, 2, None, 4]) == 2.0
    assert m.column_mean([None, None]) is None and m.column_mean([]) is None
    assert m.column_mean([0, 0]) == 0
