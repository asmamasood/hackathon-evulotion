"""CLI command handlers.

This module contains functions for displaying output to the user.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from todo_cli.domain.todo import Todo


def print_success(message: str) -> None:
    """Print a success message.

    Args:
        message: The message to print
    """
    print(f"\033[92m{message}\033[0m")  # Green text


def print_error(message: str) -> None:
    """Print an error message.

    Args:
        message: The message to print
    """
    print(f"\033[91mError: {message}\033[0m")  # Red text


def print_todo(todo: "Todo", show_id: bool = False) -> None:
    """Print a single todo with formatted output.

    Args:
        todo: The todo to print
        show_id: Whether to show the todo ID
    """
    status = "\033[92m[✓]\033[0m" if todo.completed else "\033[90m[ ]\033[0m"

    if show_id:
        print(f"{status} ID: {todo.id[:8]}... - {todo.title}")
    else:
        print(f"{status} {todo.title}")

    if todo.description:
        indent = "    " if not show_id else "       "
        print(f"{indent}{todo.description}")


def print_todos(todos: list["Todo"]) -> None:
    """Print a list of todos with formatted output.

    Args:
        todos: List of todos to print
    """
    if not todos:
        print("No tasks found. Use 'todo add <title>' to create a task.")
        return

    print(f"\nYour tasks ({len(todos)}):")
    print("-" * 50)
    for i, todo in enumerate(todos, 1):
        status = "\033[92m[✓]\033[0m" if todo.completed else "\033[90m[ ]\033[0m"
        print(f"{status} {i}. {todo.title}")
        if todo.description:
            print(f"       {todo.description}")
    print("-" * 50)