#!/usr/bin/env python3
"""Module 16: Event Streaming & Dead-Letter Queue (DLQ) Demonstration.

This script demonstrates publishing events and isolating failed poison pill messages
in a Dead-Letter Queue.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EventMessage:
    event_id: str
    topic: str
    payload: dict
    retry_count: int = 0


class EventBroker:
    def __init__(self, max_retries: int = 2) -> None:
        self.topic_queue: list[EventMessage] = []
        self.dlq: list[dict] = []
        self.max_retries = max_retries

    def publish(self, topic: str, event_id: str, payload: dict) -> None:
        self.topic_queue.append(EventMessage(event_id=event_id, topic=topic, payload=payload))

    def consume_all(self, handler) -> list[str]:
        processed = []
        while self.topic_queue:
            msg = self.topic_queue.pop(0)
            try:
                handler(msg)
                processed.append(msg.event_id)
            except Exception as err:
                msg.retry_count += 1
                if msg.retry_count <= self.max_retries:
                    self.topic_queue.append(msg)
                else:
                    self.dlq.append({"event_id": msg.event_id, "error": str(err), "payload": msg.payload})
        return processed


def fragile_event_handler(msg: EventMessage) -> None:
    if msg.payload.get("corrupt"):
        raise ValueError("Unparseable schema corruption!")


def main() -> None:
    print("=" * 60)
    print("  Event Streaming & Dead-Letter Queue Isolation Demo")
    print("=" * 60)

    broker = EventBroker(max_retries=2)
    broker.publish("orders", "EVT-1", {"order_id": 101, "amount": 50.0})
    broker.publish("orders", "EVT-2-BAD", {"order_id": 102, "corrupt": True})
    broker.publish("orders", "EVT-3", {"order_id": 103, "amount": 75.0})

    successful = broker.consume_all(fragile_event_handler)
    print(f"Successfully processed events : {successful}")
    print(f"Events routed to DLQ         : {[d['event_id'] for d in broker.dlq]}")


if __name__ == "__main__":
    main()
