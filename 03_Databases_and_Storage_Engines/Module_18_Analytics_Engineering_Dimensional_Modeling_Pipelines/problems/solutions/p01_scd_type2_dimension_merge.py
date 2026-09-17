"""Reference Solution — Problem 01: Scd Type2 Dimension Merge

Topic: 18 Analytics Engineering Dimensional Modeling Pipelines
"""

from __future__ import annotations


def scd_type2_dimension_merge(existing_dims: list[dict], incoming_record: dict, as_of_date: str) -> list[dict]:
    res = [dict(d) for d in existing_dims]
    nk = incoming_record['natural_key']
    matched_idx = -1
    for i, d in enumerate(res):
        if d['natural_key'] == nk and d.get('is_current'):
            matched_idx = i
            break
    if matched_idx != -1:
        if res[matched_idx]['val'] != incoming_record['val']:
            res[matched_idx]['valid_to'] = as_of_date
            res[matched_idx]['is_current'] = False
            new_id = max((d['id'] for d in res), default=0) + 1
            res.append({
                'id': new_id,
                'natural_key': nk,
                'val': incoming_record['val'],
                'valid_from': as_of_date,
                'valid_to': None,
                'is_current': True
            })
    else:
        new_id = max((d['id'] for d in res), default=0) + 1
        res.append({
            'id': new_id,
            'natural_key': nk,
            'val': incoming_record['val'],
            'valid_from': as_of_date,
            'valid_to': None,
            'is_current': True
        })
    return res
