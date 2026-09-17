"""Tests for WebSocket Channel Multiplexer."""
from __future__ import annotations

import pytest
from p01_websocket_channel_hub import ChannelHub


def test_websocket_channel_hub():
    hub = ChannelHub()
    hub.subscribe('room1', 'c1')
    hub.subscribe('room1', 'c2')
    assert hub.broadcast('room1') == ['c1', 'c2']
    hub.unsubscribe('room1', 'c1')
    assert hub.broadcast('room1') == ['c2']
    assert hub.broadcast('empty') == []
