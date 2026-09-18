"""Problem 01 — WebSocket Channel Multiplexer

Target: Production-grade implementation
"""

from __future__ import annotations


class ChannelHub:
    def __init__(self):
        self.channels = {}
    def subscribe(self, channel: str, client_id: str):
        self.channels.setdefault(channel, set()).add(client_id)
    def unsubscribe(self, channel: str, client_id: str):
        if channel in self.channels:
            self.channels[channel].discard(client_id)
    def broadcast(self, channel: str) -> list[str]:
        return sorted(list(self.channels.get(channel, set())))
