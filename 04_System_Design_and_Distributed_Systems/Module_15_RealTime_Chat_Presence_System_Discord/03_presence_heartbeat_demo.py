#!/usr/bin/env python3
"""Module 15 Demo: Live Cross-Gateway Chat Routing & Heartbeat Presence Simulation."""

import sys
import time
from pathlib import Path

# Add project_solution to sys.path
sys.path.insert(0, str(Path(__file__).parent / "project_solution"))

from chat_presence_platform import (
    DistributedChatPlatform,
    WebSocketGatewayNode,
)


def main() -> None:
    print("=" * 72)
    print("  MODULE 15: REAL-TIME DISTRIBUTED CHAT & PRESENCE DEMO")
    print("=" * 72)

    platform = DistributedChatPlatform(presence_timeout=2.0)
    gw_tokyo = WebSocketGatewayNode("gw-tokyo")
    gw_london = WebSocketGatewayNode("gw-london")

    platform.register_gateway(gw_tokyo)
    platform.register_gateway(gw_london)

    # 1. Connect Users to Separate Gateways
    print("\n--- 1. Client WebSocket Connections to Edge Gateways ---")
    platform.user_connect("kenji", "gw-tokyo")
    platform.user_connect("oliver", "gw-london")
    print(f"User 'kenji' connected to '{platform.session_registry['kenji']}' | Status: {platform.presence.get_status('kenji').value}")
    print(f"User 'oliver' connected to '{platform.session_registry['oliver']}' | Status: {platform.presence.get_status('oliver').value}")

    # 2. Cross-Gateway Routing
    print("\n--- 2. Real-Time Cross-Gateway Message Transmission ---")
    msg1 = platform.send_message(
        sender_id="kenji",
        recipient_id="oliver",
        conversation_id="dm:kenji:oliver",
        content="Good afternoon Oliver! Checking in on the deployment.",
    )
    print(f"Kenji -> Oliver: '{msg1.content}'")
    print(f"  Delivered to London Gateway inbox: {len(gw_london.connected_users['oliver'])} message(s)")

    # 3. Offline Mailbox Staging
    print("\n--- 3. Offline User Mailbox Staging & Flush ---")
    print("Sending message to offline user 'sarah'...")
    platform.send_message(
        sender_id="kenji",
        recipient_id="sarah",
        conversation_id="dm:kenji:sarah",
        content="Meeting rescheduled to 3 PM UTC.",
    )
    print(f"  Staged in offline mailbox: {len(platform.offline_mailboxes['sarah'])} pending message(s)")

    print("\nSarah comes online and connects to 'gw-london'...")
    platform.user_connect("sarah", "gw-london")
    print(f"  Offline mailbox flushed! Sarah received {len(gw_london.connected_users['sarah'])} message: '{gw_london.connected_users['sarah'][0].content}'")

    # 4. Presence Timeout
    print("\n--- 4. Heartbeat Expiry Simulation ---")
    print("Kenji stops sending heartbeats (2.0s timeout)...")
    time.sleep(1.1)
    print(f"  After 1.1s: Kenji status = {platform.presence.get_status('kenji').value}")
    time.sleep(1.0)
    print(f"  After 2.1s: Kenji status = {platform.presence.get_status('kenji').value}")

    print("\n" + "=" * 72)


if __name__ == "__main__":
    main()
