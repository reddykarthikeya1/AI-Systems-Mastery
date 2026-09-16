"""Unit tests for Streaming Tool Parser."""

from __future__ import annotations

from streaming_tool_parser import StreamingToolParser


def test_streaming_token_feed_early_detection():
    early_events = []

    def on_ready(field_name: str, val: object):
        early_events.append((field_name, val))

    parser = StreamingToolParser(on_field_ready=on_ready)

    tokens = ['{', '"target_ip":', ' "192.168.1.5",', ' "port":', ' 8080,', ' "timeout":', ' 5}']
    for tok in tokens:
        parser.feed_token(tok)

    assert ("target_ip", "192.168.1.5") in early_events
    assert ("port", 8080) in early_events
    assert ("timeout", 5) in early_events
    assert parser.get_final_payload()["port"] == 8080


def test_streaming_incomplete_json_recovery():
    parser = StreamingToolParser()
    parser.feed_token('{"query": "NVIDIA H100 TDP", "max_results": 10')

    extracted = parser.parsed_fields
    assert extracted["query"] == "NVIDIA H100 TDP"
    assert extracted["max_results"] == 10
