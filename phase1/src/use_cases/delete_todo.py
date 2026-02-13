"""Delete Todo use case.

This module contains the use case for deleting a todo.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from todo_cli.domain.repository import TodoRepository


class DeleteTodoUseCase:
    """Use case for deleting a todo."""

    def __init__(self, repository: "TodoRepository") -> None:
        """Initialize the use case.

        Args:
            repository: The Todo repository to use
        """
        self._repository = repository

    def execute(self, todo_id: str) -> bool:
        """Delete a todo.

        Args:
            todo_id: ID of the todo to delete

        Returns:
            True if deleted, False if not found
        """
        return self._repository.delete(todo_id)