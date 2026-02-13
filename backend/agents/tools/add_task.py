"""
MCP tool for adding tasks
"""

from typing import Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import uuid
from models.todo import Todo
from database.session import get_async_session
from core.security import get_current_user


async def add_task(
    title: str, 
    description: str = None, 
    user_id: str = None,
    session: AsyncSession = None
) -> Dict[str, Any]:
    """
    Add a new task based on natural language description
    """
    if not session or not user_id:
        raise ValueError("Session and user_id are required")
    
    # Create new todo
    todo = Todo(
        title=title,
        description=description,
        user_id=UUID(user_id)  # Convert string to UUID
    )
    
    session.add(todo)
    await session.commit()
    await session.refresh(todo)
    
    return {
        "success": True,
        "message": f"Task '{title}' added successfully",
        "task_id": str(todo.id),
        "task_details": {
            "id": str(todo.id),
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed
        }
    }