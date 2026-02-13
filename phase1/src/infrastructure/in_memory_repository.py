"""In-memory Todo repository implementation.

This module provides an in-memory implementation of the TodoRepository interface.
"""

from datetime import datetime
from typing import TYPE_CHECKING
import uuid

from todo_cli.domain.repository import TodoRepository

if TYPE_CHECKING:
    from todo_cli.domain.todo import Todo


class InMemoryTodoRepository(TodoRepository):
    """In-memory implementation of TodoRepository.

    This implementation stores todos in a Python dictionary.
    Data is not persisted between application runs.
    """

    def __init__(self) -> None:
        """Initialize the in-memory repository."""
        self._todos: dict[str, Todo] = {}

    def add(self, todo: "Todo") -> "Todo":
        """Add a new todo.

        Args:
            todo: The todo to add

        Returns:
            The added todo with generated ID if not provided
        """
        if not todo.id or todo.id == "":
            # Generate a new UUID if ID is not provided
            todo_with_id = type(todo)(
                id=str(uuid.uuid4()),
                title=todo.title,
                description=todo.description,
                completed=todo.completed,
                created_at=todo.created_at,
                updated_at=todo.updated_at,
            )
        else:
            todo_with_id = todo

        self._todos[todo_with_id.id] = todo_with_id
        return todo_with_id

    def get_all(self) -> list["Todo"]:
        """Get all todos.

        Returns:
            List of all todos, sorted by creation time (newest first)
        """
        return list(
            sorted(self._todos.values(), key=lambda t: t.created_at, reverse=True)
        )

    def get_by_id(self, todo_id: str) -> "Todo | None":
        """Get a todo by ID.

        Args:
            todo_id: The ID of the todo

        Returns:
            The todo if found, None otherwise
        """
        return self._todos.get(todo_id)

    def update(self, todo: "Todo") -> "Todo":
        """Update a todo.

        Args:
            todo: The todo to update

        Returns:
            The updated todo

        Raises:
            ValueError: If todo with given ID doesn't exist
        """
        if todo.id not in self._todos:
            raise ValueError(f"Todo with ID {todo.id} not found")

        self._todos[todo.id] = todo
        return todo

    def delete(self, todo_id: str) -> bool:
        """Delete a todo.

        Args:
            todo_id: The ID of the todo

        Returns:
            True if deleted, False if not found
        """
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False

    def clear(self) -> None:
        """Clear all todos (useful for testing)."""
        self._todos.clear()