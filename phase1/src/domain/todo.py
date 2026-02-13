"""Todo entity definition.

This module defines the core Todo entity representing a task.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


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
    """

    id: str
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        """Validate todo after initialization.

        Raises:
            ValueError: If title is empty or only whitespace.
        """
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")

    def mark_complete(self) -> "Todo":
        """Mark the todo as complete.

        Returns:
            The updated todo with completed=True
        """
        return Todo(
            id=self.id,
            title=self.title,
            description=self.description,
            completed=True,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def mark_incomplete(self) -> "Todo":
        """Mark the todo as incomplete.

        Returns:
            The updated todo with completed=False
        """
        return Todo(
            id=self.id,
            title=self.title,
            description=self.description,
            completed=False,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def update(
        self,
        title: str | None = None,
        description: str | None = None,
    ) -> "Todo":
        """Update the todo with new values.

        Args:
            title: New title (optional)
            description: New description (optional)

        Returns:
            The updated todo

        Raises:
            ValueError: If title is empty or only whitespace
        """
        new_title = title if title is not None else self.title
        new_description = description if description is not None else self.description

        return Todo(
            id=self.id,
            title=new_title,
            description=new_description,
            completed=self.completed,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )