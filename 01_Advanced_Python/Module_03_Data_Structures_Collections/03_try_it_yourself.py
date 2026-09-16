"""Module 03: W3-Style Interactive Collections Playground.

Run this script directly in your terminal:
    python try_it_yourself.py
"""

def todo_list_demo():
    todos = ["Review Python basics", "Drink water"]
    while True:
        print("\n--- Current To-Do List ---")
        for i, item in enumerate(todos, start=1):
            print(f"  {i}. {item}")

        print("\nOptions: [1] Add task, [2] Complete/Remove task, [3] Back")
        cmd = input("Select option: ").strip()
        if cmd == "1":
            new_task = input("Enter new task: ").strip()
            if new_task:
                todos.append(new_task)
                print(f"Added: '{new_task}'")
        elif cmd == "2":
            try:
                idx = int(input("Enter task number to remove: "))
                if 1 <= idx <= len(todos):
                    removed = todos.pop(idx - 1)
                    print(f"Completed & removed: '{removed}'")
                else:
                    print("Invalid task number!")
            except ValueError:
                print("Please enter a number.")
        elif cmd == "3":
            break

def user_directory_demo():
    directory = {
        "alex": {"role": "Frontend Engineer", "location": "London"},
        "sam": {"role": "Backend Engineer", "location": "New York"},
        "jordan": {"role": "DevOps Architect", "location": "Tokyo"}
    }
    while True:
        print("\n--- User Directory Lookup ---")
        name = input("Enter username to search (or 'q' to back): ").strip().lower()
        if name == "q":
            break
        user = directory.get(name)
        if user:
            print(f"User: {name.capitalize()}")
            print(f"  Role:     {user['role']}")
            print(f"  Location: {user['location']}")
        else:
            print(f"User '{name}' not found! Available: {list(directory.keys())}")

def main():
    print("=" * 60)
    print("  MODULE 03: INTERACTIVE COLLECTIONS PLAYGROUND [PKG]")
    print("=" * 60)
    while True:
        print("\nChoose an activity:")
        print("1. Manage an Interactive To-Do List (Lists)")
        print("2. Search User Profiles (Dictionaries)")
        print("3. Exit")
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice == "1":
            todo_list_demo()
        elif choice == "2":
            user_directory_demo()
        elif choice == "3":
            print("Great work! Proceed to Module 04.")
            break

if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nSession ended. Happy coding!")
