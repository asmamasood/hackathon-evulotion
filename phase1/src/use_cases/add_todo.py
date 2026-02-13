"""Add Todo use case.

This module contains the use case for adding a new todo.
"""

from typing import TYPE_CHECKING

from todo_cli.domain.todo import Todo

if TYPE_CHECKING:
    from todo_cli.domain.repository import TodoRepository


class AddTodoUseCase:
    """Use case for adding a new todo."""

    def __init__(self, repository: "TodoRepository") -> None:
        """Initialize the use case.

        Args:
            repository: The Todo repository to use
        """
        self._repository = repository

    def execute(self, title: str, description: str = "") -> Todo:
        """Add a new todo.

        Args:
            title: Title of the todo
            description: Optional description

        Returns:
            The created todo

        Raises:
            ValueError: If title is empty or invalid
        """
        todo = Todo(
            id="",  # Repository will generate ID
            title=title,
            description=description,
            completed=False,
        )
        return self._repository.add(todo)