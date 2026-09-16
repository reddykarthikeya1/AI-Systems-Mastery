"""Module 07: W3-Style Interactive File Storage Playground.

Run this script directly in your terminal:
    python try_it_yourself.py
"""

import json
import os

NOTES_FILE = "my_scratchpad_notes.json"

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2)

def main():
    print("=" * 60)
    print("  MODULE 07: INTERACTIVE JSON NOTEPAD PLAYGROUND [NOTE]")
    print("=" * 60)

    notes = load_notes()
    print(f"Loaded {len(notes)} existing notes from {NOTES_FILE}.")

    while True:
        print("\n1. View All Notes")
        print("2. Add a Note")
        print("3. Clear All Notes")
        print("4. Exit")
        cmd = input("Choose (1-4): ").strip()

        if cmd == "1":
            print("\n--- Your Saved Notes ---")
            if not notes:
                print("  (No notes yet!)")
            for i, note in enumerate(notes, 1):
                print(f"  {i}. {note}")
        elif cmd == "2":
            text = input("Type your note: ").strip()
            if text:
                notes.append(text)
                save_notes(notes)
                print("[OK] Saved to disk!")
        elif cmd == "3":
            notes = []
            save_notes(notes)
            print("   Notes cleared!")
        elif cmd == "4":
            print("Great job! Proceed to Module 08.")
            break

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nSession ended. Happy coding!")
