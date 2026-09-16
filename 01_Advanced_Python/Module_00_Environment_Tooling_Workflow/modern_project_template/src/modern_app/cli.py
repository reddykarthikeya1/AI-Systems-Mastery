"""Command-line interface for modern_app using rich formatting."""

from __future__ import annotations

import argparse
import sys

from rich.console import Console
from rich.table import Table

from modern_app.core import TaskManager

console = Console()


def create_parser() -> argparse.ArgumentParser:
    """Configure and return the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="modern-app",
        description=(
            "A modern CLI Task Manager demonstrating src-layout and uv tooling."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: add
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task title")
    add_parser.add_argument("--desc", type=str, default="", help="Task description")

    # Command: list
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "--status",
        choices=["pending", "in_progress", "completed"],
        default=None,
        help="Filter by status",
    )

    # Command: complete
    complete_parser = subparsers.add_parser("complete", help="Complete a task by ID")
    complete_parser.add_argument("id", type=int, help="Task ID")

    # Command: demo
    subparsers.add_parser("demo", help="Run interactive demo")

    return parser


def display_tasks(manager: TaskManager, status_filter: str | None = None) -> None:
    """Display tasks in a rich styled table."""
    tasks = manager.list_tasks(status=status_filter)
    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    table = Table(title="Task Catalog", show_header=True, header_style="bold magenta")
    table.add_column("ID", justify="right", style="cyan", width=6)
    table.add_column("Title", style="white", min_width=20)
    table.add_column("Status", justify="center")
    table.add_column("Created", style="dim", width=24)

    for task in tasks:
        status_style = {
            "pending": "[yellow]Pending[/yellow]",
            "in_progress": "[blue]In Progress[/blue]",
            "completed": "[green]Completed[/green]",
        }.get(task.status, task.status)

        table.add_row(
            str(task.id),
            task.title,
            status_style,
            task.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"),
        )

    console.print(table)


def run_demo() -> None:
    """Demonstrate the TaskManager functionality in a rich console."""
    console.print("[bold green]=== Modern App Demo ===[/bold green]\n")
    manager = TaskManager()

    console.print("[cyan]1. Adding tasks...[/cyan]")
    manager.add_task(
        "Set up development environment with uv",
        "Install uv, python 3.12, and configure pyproject.toml",
    )
    manager.add_task(
        "Configure Ruff linter & formatter",
        "Add Ruff config to pyproject.toml with rules E, F, I, UP, B",
    )
    t3 = manager.add_task(
        "Write unit tests with pytest",
        "Achieve 100% test coverage with pytest-cov",
    )

    console.print("[cyan]2. Marking task #3 as completed...[/cyan]")
    manager.complete_task(t3.id)

    console.print("\n[cyan]3. Listing all tasks:[/cyan]")
    display_tasks(manager)


def main(argv: list[str] | None = None) -> int:
    """Main CLI entrypoint."""
    parser = create_parser()
    args = parser.parse_args(argv)

    if args.command == "demo" or args.command is None:
        run_demo()
        return 0

    manager = TaskManager()

    if args.command == "add":
        task = manager.add_task(args.title, args.desc)
        console.print(f"[green]Added task #{task.id}:[/green] {task.title}")
    elif args.command == "list":
        display_tasks(manager, args.status)
    elif args.command == "complete":
        if manager.complete_task(args.id):
            console.print(f"[green]Completed task #{args.id}[/green]")
        else:
            console.print(f"[red]Task #{args.id} not found[/red]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
