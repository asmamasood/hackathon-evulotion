"""List Todos use case.

This module contains the use case for listing all todos.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from todo_cli.domain.repository import TodoRepository
    from todo_cli.domain.todo import Todo


class ListTodosUseCase:
    """Use case for listing all todos."""

    def __init__(self, repository: "TodoRepository") -> None:
        """Initialize the use case.

        Args:
            repository: The Todo repository to use
        """
        self._repository = repository

    def execute(self) -> list["Todo"]:
        """Get all todos.

        Returns:
            List of all todos
        """
        return self._repository.get_all()