"""Main entry point for Todo CLI application.

This module provides the command-line interface for the Todo application.
"""

import argparse
import sys

from todo_cli.domain.todo import Todo
from todo_cli.infrastructure import InMemoryTodoRepository
from todo_cli.use_cases import (
    AddTodoUseCase,
    ListTodosUseCase,
    UpdateTodoUseCase,
    DeleteTodoUseCase,
    CompleteTodoUseCase,
)
from todo_cli.cli import print_success, print_error, print_todos


# Create shared repository instance
_repository = InMemoryTodoRepository()


def cmd_add(args: argparse.Namespace) -> None:
    """Handle the add command.

    Args:
        args: Command-line arguments
    """
    use_case = AddTodoUseCase(_repository)
    description = args.description or ""

    try:
        todo = use_case.execute(args.title, description)
        print_success(f"Added: {todo.title}")
    except ValueError as e:
        print_error(str(e))


def cmd_list(args: argparse.Namespace) -> None:  # noqa: ARG001
    """Handle the list command.

    Args:
        args: Command-line arguments (unused)
    """
    use_case = ListTodosUseCase(_repository)
    todos = use_case.execute()
    print_todos(todos)


def cmd_update(args: argparse.Namespace) -> None:
    """Handle the update command.

    Args:
        args: Command-line arguments
    """
    use_case = UpdateTodoUseCase(_repository)

    try:
        # First, get the todo to find its index/ID
        todos = ListTodosUseCase(_repository).execute()

        # Convert 1-based index to 0-based
        index = args.id - 1

        if index < 0 or index >= len(todos):
            print_error(f"Task {args.id} not found")
            return

        todo = todos[index]
        updated = use_case.execute(
            todo_id=todo.id,
            title=args.title,
            description=args.description,
        )
        print_success(f"Updated: {updated.title}")
    except ValueError as e:
        print_error(str(e))


def cmd_delete(args: argparse.Namespace) -> None:
    """Handle the delete command.

    Args:
        args: Command-line arguments
    """
    use_case = DeleteTodoUseCase(_repository)

    try:
        todos = ListTodosUseCase(_repository).execute()
        index = args.id - 1

        if index < 0 or index >= len(todos):
            print_error(f"Task {args.id} not found")
            return

        todo = todos[index]
        success = use_case.execute(todo.id)
        if success:
            print_success(f"Deleted: {todo.title}")
        else:
            print_error(f"Task {args.id} not found")
    except ValueError as e:
        print_error(str(e))


def cmd_complete(args: argparse.Namespace) -> None:
    """Handle the complete command.

    Args:
        args: Command-line arguments
    """
    use_case = CompleteTodoUseCase(_repository)

    try:
        todos = ListTodosUseCase(_repository).execute()
        index = args.id - 1

        if index < 0 or index >= len(todos):
            print_error(f"Task {args.id} not found")
            return

        todo = todos[index]
        updated = use_case.execute(todo.id, completed=True)
        print_success(f"Completed: {updated.title}")
    except ValueError as e:
        print_error(str(e))


def cmd_incomplete(args: argparse.Namespace) -> None:
    """Handle the incomplete command.

    Args:
        args: Command-line arguments
    """
    use_case = CompleteTodoUseCase(_repository)

    try:
        todos = ListTodosUseCase(_repository).execute()
        index = args.id - 1

        if index < 0 or index >= len(todos):
            print_error(f"Task {args.id} not found")
            return

        todo = todos[index]
        updated = use_case.execute(todo.id, completed=False)
        print_success(f"Marked incomplete: {updated.title}")
    except ValueError as e:
        print_error(str(e))


def main() -> int:
    """Main entry point for the CLI application.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = argparse.ArgumentParser(
        description="Console Todo Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  todo add "Buy groceries" --description "Milk, eggs, bread"
  todo list
  todo update 1 --title "Buy groceries and snacks"
  todo delete 1
  todo complete 1
  todo incomplete 1
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument(
        "--description", "-d", help="Optional task description"
    )
    add_parser.set_defaults(func=cmd_add)

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.set_defaults(func=cmd_list)

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", type=int, help="Task number")
    update_parser.add_argument("--title", "-t", help="New title")
    update_parser.add_argument(
        "--description", "-d", help="New description"
    )
    update_parser.set_defaults(func=cmd_update)

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task number")
    delete_parser.set_defaults(func=cmd_delete)

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark task as complete")
    complete_parser.add_argument("id", type=int, help="Task number")
    complete_parser.set_defaults(func=cmd_complete)

    # Incomplete command
    incomplete_parser = subparsers.add_parser(
        "incomplete", help="Mark task as incomplete"
    )
    incomplete_parser.add_argument("id", type=int, help="Task number")
    incomplete_parser.set_defaults(func=cmd_incomplete)

    # Parse arguments
    args = parser.parse_args()

    # If no command is provided, show help
    if args.command is None:
        parser.print_help()
        return 0

    # Execute the command
    try:
        args.func(args)
        return 0
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return 130
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())