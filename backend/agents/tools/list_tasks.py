"""
MCP tool for listing tasks
"""

from typing import Dict, Any
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from models.todo import Todo
from database.session import get_async_session


async def list_tasks(
    user_id: str = None,
    filter_criteria: str = None,
    session: AsyncSession = None
) -> Dict[str, Any]:
    """
    Retrieve and display user's tasks
    """
    if not session or not user_id:
        raise ValueError("Session and user_id are required")
    
    # Build query based on filter criteria
    query = select(Todo).where(Todo.user_id == UUID(user_id))
    
    if filter_criteria == "completed":
        query = query.where(Todo.completed == True)
    elif filter_criteria == "pending":
        query = query.where(Todo.completed == False)
    elif filter_criteria == "today":
        # This would require more complex date filtering
        # For now, we'll return all tasks
        pass
    
    result = await session.execute(query)
    todos = result.scalars().all()
    
    task_list = []
    for todo in todos:
        task_list.append({
            "id": str(todo.id),
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed,
            "created_at": todo.created_at.isoformat() if todo.created_at else None
        })
    
    return {
        "success": True,
        "count": len(task_list),
        "tasks": task_list,
        "filter_applied": filter_criteria
    }