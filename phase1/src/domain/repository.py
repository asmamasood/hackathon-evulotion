"""Todo repository interface.

This module defines the abstract base class for Todo repository implementations.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .todo import Todo


class TodoRepository(ABC):
    """Interface for Todo data access.

    This interface defines the contract for all Todo repository implementations.
    Implementations can be in-memory (Phase I), PostgreSQL (Phase II+), etc.
    """

    @abstractmethod
    def add(self, todo: "Todo") -> "Todo":
        """Add a new todo.

        Args:
            todo: The todo to add

        Returns:
            The added todo with generated ID
        """
        ...

    @abstractmethod
    def get_all(self) -> list["Todo"]:
        """Get all todos.

        Returns:
            List of all todos
        """
        ...

    @abstractmethod
    def get_by_id(self, todo_id: str) -> "Todo | None":
        """Get a todo by ID.

        Args:
            todo_id: The ID of the todo

        Returns:
            The todo if found, None otherwise
        """
        ...

    @abstractmethod
    def update(self, todo: "Todo") -> "Todo":
        """Update a todo.

        Args:
            todo: The todo to update

        Returns:
            The updated todo
        """
        ...

    @abstractmethod
    def delete(self, todo_id: str) -> bool:
        """Delete a todo.

        Args:
            todo_id: The ID of the todo

        Returns:
            True if deleted, False if not found
        """
        ...