"""
MCP tool for updating tasks
"""

from typing import Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from models.todo import Todo
from database.session import get_async_session


async def update_task(
    task_id: str,
    user_id: str = None,
    title: str = None,
    description: str = None,
    completed: bool = None,
    session: AsyncSession = None
) -> Dict[str, Any]:
    """
    Modify an existing task
    """
    if not session or not user_id:
        raise ValueError("Session and user_id are required")
    
    # Find the task
    stmt = select(Todo).where(Todo.id == UUID(task_id), Todo.user_id == UUID(user_id))
    result = await session.execute(stmt)
    todo = result.scalar_one_or_none()
    
    if not todo:
        raise ValueError(f"Task with ID {task_id} not found or does not belong to user")
    
    # Update the task with provided values
    if title is not None:
        todo.title = title
    if description is not None:
        todo.description = description
    if completed is not None:
        todo.completed = completed
    
    await session.commit()
    await session.refresh(todo)
    
    return {
        "success": True,
        "message": f"Task '{todo.title}' updated successfully",
        "task_id": str(todo.id),
        "updated_fields": {
            "title": title,
            "description": description,
            "completed": completed
        }
    }