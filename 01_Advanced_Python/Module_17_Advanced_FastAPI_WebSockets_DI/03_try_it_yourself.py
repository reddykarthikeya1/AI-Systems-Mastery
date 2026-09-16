"""
Module 17: Interactive WebSocket Event Broadcaster Simulator
Run: python try_it_yourself.py
"""


class MockWebSocketRoom:
    def __init__(self):
        self.active_clients = set()

    def connect(self, client_name):
        self.active_clients.add(client_name)
        print(f"  [+] {client_name} connected to WebSocket room.")

    def disconnect(self, client_name):
        self.active_clients.discard(client_name)
        print(f"  [-] {client_name} disconnected.")

    def broadcast(self, sender, message):
        print(f"\n[Broadcast from {sender}]: '{message}'")
        for client in self.active_clients:
            if client != sender:
                print(f"    --> Delivered to {client}")


def main():
    print("=" * 60)
    print("  MODULE 17: WEBSOCKET BROADCASTER PLAYGROUND [*]")
    print("=" * 60)

    room = MockWebSocketRoom()
    room.connect("Alice")
    room.connect("Bob")
    room.connect("Charlie")

    room.broadcast("Alice", "Hello everyone in the live room!")
    room.disconnect("Bob")
    room.broadcast("Charlie", "Did Bob just leave?")

    print("\n[OK] Real-time duplex message dispatching simulated!")


if __name__ == "__main__":
    main()
