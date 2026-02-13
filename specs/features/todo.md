# Todo Feature Specification

> Last Updated: 2026-02-12
> Version: 1.0.0

## Overview

This specification defines the core Todo feature that exists across all phases of the application.

## References

- @specs/overview.md
- @specs/phases/phase1.md

## Domain Model

### Todo Entity

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Todo:
    """Core Todo entity representing a task.

    Attributes:
        id: Unique identifier for the todo
        title: Title of the todo (required)
        description: Optional detailed description
        completed: Whether the todo is completed
        created_at: Timestamp when the todo was created
        updated_at: Timestamp when the todo was last updated
        user_id: Owner of the todo (Phase II+)
    """
    id: str
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None
    user_id: str | None = None  # Phase II+

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
```

## Repository Interface

```python
from abc import ABC, abstractmethod
from typing import Optional, List


class TodoRepository(ABC):
    """Interface for Todo data access.

    This interface defines the contract for all Todo repository implementations.
    Implementations can be in-memory (Phase I), PostgreSQL (Phase II+), etc.
    """

    @abstractmethod
    def add(self, todo: Todo) -> Todo:
        """Add a new todo.

        Args:
            todo: The todo to add

        Returns:
            The added todo with generated ID
        """
        ...

    @abstractmethod
    def get_all(self, user_id: Optional[str] = None) -> List[Todo]:
        """Get all todos.

        Args:
            user_id: Optional user ID for filtering (Phase II+)

        Returns:
            List of all todos
        """
        ...

    @abstractmethod
    def get_by_id(self, todo_id: str, user_id: Optional[str] = None) -> Optional[Todo]:
        """Get a todo by ID.

        Args:
            todo_id: The ID of the todo
            user_id: Optional user ID for ownership check (Phase II+)

        Returns:
            The todo if found, None otherwise
        """
        ...

    @abstractmethod
    def update(self, todo: Todo) -> Todo:
        """Update a todo.

        Args:
            todo: The todo to update

        Returns:
            The updated todo
        """
        ...

    @abstractmethod
    def delete(self, todo_id: str, user_id: Optional[str] = None) -> bool:
        """Delete a todo.

        Args:
            todo_id: The ID of the todo
            user_id: Optional user ID for ownership check (Phase II+)

        Returns:
            True if deleted, False if not found
        """
        ...
```

## Validation Rules

### Title
- Required (cannot be empty)
- Maximum length: 200 characters
- Cannot contain only whitespace

### Description
- Optional
- Maximum length: 1000 characters

### ID
- Must be unique
- UUID v4 format recommended

## Use Cases

### Phase I (CLI)

#### AddTodoUseCase
```python
class AddTodoUseCase:
    """Use case for adding a new todo."""

    def __init__(self, repository: TodoRepository):
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
        ...
```

#### ListTodosUseCase
```python
class ListTodosUseCase:
    """Use case for listing all todos."""

    def __init__(self, repository: TodoRepository):
        self._repository = repository

    def execute(self) -> List[Todo]:
        """Get all todos.

        Returns:
            List of all todos
        """
        ...
```

#### UpdateTodoUseCase
```python
class UpdateTodoUseCase:
    """Use case for updating a todo."""

    def __init__(self, repository: TodoRepository):
        self._repository = repository

    def execute(
        self,
        todo_id: str,
        title: str | None = None,
        description: str | None = None
    ) -> Todo:
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
        ...
```

#### DeleteTodoUseCase
```python
class DeleteTodoUseCase:
    """Use case for deleting a todo."""

    def __init__(self, repository: TodoRepository):
        self._repository = repository

    def execute(self, todo_id: str) -> bool:
        """Delete a todo.

        Args:
            todo_id: ID of the todo to delete

        Returns:
            True if deleted, False if not found
        """
        ...
```

#### CompleteTodoUseCase
```python
class CompleteTodoUseCase:
    """Use case for marking a todo as complete/incomplete."""

    def __init__(self, repository: TodoRepository):
        self._repository = repository

    def execute(self, todo_id: str, completed: bool = True) -> Todo:
        """Mark a todo as complete or incomplete.

        Args:
            todo_id: ID of the todo
            completed: True to mark complete, False for incomplete

        Returns:
            The updated todo

        Raises:
            ValueError: If todo not found
        """
        ...
```

### Phase II+ (Web)

Same use cases with added `user_id` parameter for ownership validation.

## Display Formats

### CLI Output (Phase I)
```
[✓] ID: 1 - Buy groceries
    Description: Milk, eggs, bread

[ ] ID: 2 - Clean room
```

### JSON API Response (Phase II+)
```json
{
  "id": "uuid",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2026-02-12T10:00:00Z",
  "updated_at": "2026-02-12T11:00:00Z",
  "user_id": "user-uuid"
}
```

## Error Messages

### Common Errors
- "Todo not found" - When attempting to access non-existent todo
- "Title cannot be empty" - When title is invalid
- "Invalid todo ID format" - When ID format is incorrect

### Phase II+ Errors
- "Unauthorized" - When user doesn't own the todo
- "Invalid token" - When JWT is invalid or expired

## Future Enhancements (Phase V)

### Additional Fields
- `due_date: datetime | None` - Due date for the task
- `priority: int` - Priority level (1-5)
- `tags: List[str]` - Tags for categorization
- `recurrence: RecurrenceRule | None` - Recurrence pattern

### Additional Operations
- Filter by status, priority, due date
- Sort by various fields
- Search by title/description
- Bulk operations