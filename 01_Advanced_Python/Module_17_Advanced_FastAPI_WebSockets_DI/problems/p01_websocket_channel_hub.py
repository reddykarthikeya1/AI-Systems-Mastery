"""Problem 01 — WebSocket Channel Multiplexer

Target: Production-grade implementation

Example:
    >>> hub = ChannelHub()
    >>> hub.subscribe('room1', 'c1')
    >>> hub.subscribe('room1', 'c2')
    >>> hub.broadcast('room1')
    ['c1', 'c2']
    >>> hub.unsubscribe('room1', 'c1')
    >>> hub.broadcast('room1')
    ['c2']

Hints:
    Hint 1: A channel is just a named group of subscribed client ids — no
        client should be able to appear twice in the same channel no matter
        how many times it subscribes.
    Hint 2: Back each channel with a set of client ids in a dict keyed by
        channel name, using `setdefault` to create a channel's set lazily on
        first subscribe.
    Hint 3: `broadcast` on a channel nobody has subscribed to yet must return
        `[]`, not raise a KeyError, and the returned client list needs to be
        sorted since a set has no defined order.
"""

from __future__ import annotations


class ChannelHub:
    def __init__(self):
        raise NotImplementedError('Implement ChannelHub')
