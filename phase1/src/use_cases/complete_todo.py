"""Complete Todo use case.

This module contains the use case for marking a todo as complete/incomplete.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from todo_cli.domain.repository import TodoRepository
    from todo_cli.domain.todo import Todo


class CompleteTodoUseCase:
    """Use case for marking a todo as complete or incomplete."""

    def __init__(self, repository: "TodoRepository") -> None:
        """Initialize the use case.

        Args:
            repository: The Todo repository to use
        """
        self._repository = repository

    def execute(self, todo_id: str, completed: bool = True) -> "Todo":
        """Mark a todo as complete or incomplete.

        Args:
            todo_id: ID of the todo
            completed: True to mark complete, False for incomplete

        Returns:
            The updated todo

        Raises:
            ValueError: If todo not found
        """
        todo = self._repository.get_by_id(todo_id)
        if todo is None:
            raise ValueError(f"Todo with ID {todo_id} not found")

        if completed:
            updated_todo = todo.mark_complete()
        else:
            updated_todo = todo.mark_incomplete()

        return self._repository.update(updated_todo)