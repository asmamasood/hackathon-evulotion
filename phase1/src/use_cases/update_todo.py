"""Update Todo use case.

This module contains the use case for updating a todo.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from todo_cli.domain.repository import TodoRepository
    from todo_cli.domain.todo import Todo


class UpdateTodoUseCase:
    """Use case for updating a todo."""

    def __init__(self, repository: "TodoRepository") -> None:
        """Initialize the use case.

        Args:
            repository: The Todo repository to use
        """
        self._repository = repository

    def execute(
        self,
        todo_id: str,
        title: str | None = None,
        description: str | None = None,
    ) -> "Todo":
        """Update a todo.

        Args:
            todo_id: ID of the todo to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            The updated todo

        Raises:
            ValueError: If todo not found or invalid input
        """
        todo = self._repository.get_by_id(todo_id)
        if todo is None:
            raise ValueError(f"Todo with ID {todo_id} not found")

        updated_todo = todo.update(title=title, description=description)
        return self._repository.update(updated_todo)