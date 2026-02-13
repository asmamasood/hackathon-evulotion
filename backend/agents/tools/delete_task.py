"""
MCP tool for deleting tasks
"""

from typing import Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from models.todo import Todo
from database.session import get_async_session


async def delete_task(
    task_id: str,
    user_id: str = None,
    session: AsyncSession = None
) -> Dict[str, Any]:
    """
    Remove a task
    """
    if not session or not user_id:
        raise ValueError("Session and user_id are required")
    
    # Find the task
    stmt = select(Todo).where(Todo.id == UUID(task_id), Todo.user_id == UUID(user_id))
    result = await session.execute(stmt)
    todo = result.scalar_one_or_none()
    
    if not todo:
        raise ValueError(f"Task with ID {task_id} not found or does not belong to user")
    
    # Delete the task
    await session.delete(todo)
    await session.commit()
    
    return {
        "success": True,
        "message": f"Task '{todo.title}' deleted successfully",
        "task_id": str(todo.id)
    }