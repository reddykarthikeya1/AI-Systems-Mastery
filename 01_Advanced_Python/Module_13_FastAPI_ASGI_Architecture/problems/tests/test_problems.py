"""Tests for ASGI Trie Path Router."""
from __future__ import annotations

import pytest
from p01_asgi_path_router import match_asgi_route


def test_asgi_path_router():
    routes = {'/users/{id}': 'get_user', '/items': 'list_items'}
    ep, p = match_asgi_route(routes, '/users/42')
    assert ep == 'get_user'
    assert p == {'id': '42'}
    assert match_asgi_route(routes, '/unknown')[0] == ''
