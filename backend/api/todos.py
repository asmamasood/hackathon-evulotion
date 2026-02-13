"""
API router for todo-related endpoints with Dapr and Kafka integration
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from database.session import get_async_session
from models.todo import Todo, TodoCreate, TodoUpdate
from models.user import User
from schemas.todo import (
    TodoCreateRequest,
    TodoUpdateRequest,
    TodoResponse,
    TodoListResponse,
    ApiResponse,
    TodoToggleCompleteRequest
)
from core.security import get_current_user, verify_user_owns_resource
from dapr.clients import DaprClient
import json
from datetime import datetime
import logging

router = APIRouter()

# Initialize logger
logger = logging.getLogger(__name__)


@router.get("/{user_id}/todos", response_model=TodoListResponse)
async def get_user_todos(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all todos for a specific user
    """
    # Verify that the requesting user is the same as the user in the URL
    if not verify_user_owns_resource(str(current_user.id), str(user_id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's todos"
        )

    # Query todos for the user
    statement = select(Todo).where(Todo.user_id == user_id)
    result = await session.execute(statement)
    todos = result.scalars().all()

    todo_responses = [
        TodoResponse(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            user_id=todo.user_id,
            created_at=todo.created_at,
            updated_at=todo.updated_at
        ) for todo in todos
    ]

    # Publish event to Kafka via Dapr
    try:
        with DaprClient() as dapr_client:
            event_data = {
                "event_type": "user.todos.fetched",
                "user_id": str(user_id),
                "count": len(todo_responses),
                "timestamp": datetime.utcnow().isoformat()
            }
            
            dapr_client.publish_event(
                pubsub_name="pubsub",
                topic_name="todo-events",
                data=json.dumps(event_data),
                data_content_type="application/json"
            )
    except Exception as e:
        logger.error(f"Failed to publish event: {e}")

    return TodoListResponse(todos=todo_responses, count=len(todo_responses))


@router.post("/{user_id}/todos", response_model=TodoResponse)
async def create_todo(
    user_id: UUID,
    todo_data: TodoCreateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new todo for a specific user
    """
    # Verify that the requesting user is the same as the user in the URL
    if not verify_user_owns_resource(str(current_user.id), str(user_id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create todos for this user"
        )

    # Create the new todo
    todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        user_id=user_id
    )

    session.add(todo)
    await session.commit()
    await session.refresh(todo)

    # Publish event to Kafka via Dapr
    try:
        with DaprClient() as dapr_client:
            event_data = {
                "event_type": "todo.created",
                "todo_id": str(todo.id),
                "user_id": str(user_id),
                "title": todo.title,
                "description": todo.description,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            dapr_client.publish_event(
                pubsub_name="pubsub",
                topic_name="todo-events",
                data=json.dumps(event_data),
                data_content_type="application/json"
            )
            
            # Also save to Dapr state store
            dapr_client.save_state(
                store_name="statestore",
                key=f"todo-{todo.id}",
                value=json.dumps({
                    "id": str(todo.id),
                    "title": todo.title,
                    "description": todo.description,
                    "completed": todo.completed,
                    "user_id": str(todo.user_id),
                    "created_at": todo.created_at.isoformat(),
                    "updated_at": todo.updated_at.isoformat()
                })
            )
    except Exception as e:
        logger.error(f"Failed to publish event or save state: {e}")

    return TodoResponse(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        user_id=todo.user_id,
        created_at=todo.created_at,
        updated_at=todo.updated_at
    )


@router.get("/{user_id}/todos/{todo_id}", response_model=TodoResponse)
async def get_todo(
    user_id: UUID,
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific todo for a user
    """
    # Verify that the requesting user is the same as the user in the URL
    if not verify_user_owns_resource(str(current_user.id), str(user_id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's todos"
        )
    
    # Query the specific todo
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    result = await session.execute(statement)
    todo = result.scalar_one_or_none()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return TodoResponse(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        user_id=todo.user_id,
        created_at=todo.created_at,
        updated_at=todo.updated_at
    )


@router.put("/{user_id}/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(
    user_id: UUID,
    todo_id: UUID,
    todo_data: TodoUpdateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific todo for a user
    """
    # Verify that the requesting user is the same as the user in the URL
    if not verify_user_owns_resource(str(current_user.id), str(user_id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's todos"
        )

    # Query the specific todo
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    result = await session.execute(statement)
    todo = result.scalar_one_or_none()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Store original data for event
    original_title = todo.title
    original_description = todo.description

    # Update the todo with provided data
    if todo_data.title is not None:
        todo.title = todo_data.title
    if todo_data.description is not None:
        todo.description = todo_data.description

    session.add(todo)
    await session.commit()
    await session.refresh(todo)

    # Publish event to Kafka via Dapr
    try:
        with DaprClient() as dapr_client:
            event_data = {
                "event_type": "todo.updated",
                "todo_id": str(todo.id),
                "user_id": str(user_id),
                "original_title": original_title,
                "original_description": original_description,
                "updated_title": todo.title,
                "updated_description": todo.description,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            dapr_client.publish_event(
                pubsub_name="pubsub",
                topic_name="todo-events",
                data=json.dumps(event_data),
                data_content_type="application/json"
            )
            
            # Update in Dapr state store
            dapr_client.save_state(
                store_name="statestore",
                key=f"todo-{todo.id}",
                value=json.dumps({
                    "id": str(todo.id),
                    "title": todo.title,
                    "description": todo.description,
                    "completed": todo.completed,
                    "user_id": str(todo.user_id),
                    "created_at": todo.created_at.isoformat(),
                    "updated_at": todo.updated_at.isoformat()
                })
            )
    except Exception as e:
        logger.error(f"Failed to publish event or update state: {e}")

    return TodoResponse(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        user_id=todo.user_id,
        created_at=todo.created_at,
        updated_at=todo.updated_at
    )


@router.delete("/{user_id}/todos/{todo_id}")
async def delete_todo(
    user_id: UUID,
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific todo for a user
    """
    # Verify that the requesting user is the same as the user in the URL
    if not verify_user_owns_resource(str(current_user.id), str(user_id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user's todos"
        )

    # Query the specific todo
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    result = await session.execute(statement)
    todo = result.scalar_one_or_none()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Store todo data for event before deletion
    todo_data = {
        "id": str(todo.id),
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "user_id": str(todo.user_id),
        "created_at": todo.created_at.isoformat(),
        "updated_at": todo.updated_at.isoformat()
    }

    await session.delete(todo)
    await session.commit()

    # Publish event to Kafka via Dapr
    try:
        with DaprClient() as dapr_client:
            event_data = {
                "event_type": "todo.deleted",
                "todo_id": str(todo_id),
                "user_id": str(user_id),
                "todo_data": todo_data,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            dapr_client.publish_event(
                pubsub_name="pubsub",
                topic_name="todo-events",
                data=json.dumps(event_data),
                data_content_type="application/json"
            )
            
            # Remove from Dapr state store
            dapr_client.delete_state(
                store_name="statestore",
                key=f"todo-{todo_id}"
            )
    except Exception as e:
        logger.error(f"Failed to publish event or delete state: {e}")

    return {"success": True, "message": "Todo deleted successfully"}


@router.patch("/{user_id}/todos/{todo_id}/complete", response_model=TodoResponse)
async def toggle_todo_complete(
    user_id: UUID,
    todo_id: UUID,
    toggle_data: TodoToggleCompleteRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Toggle the completion status of a specific todo for a user
    """
    # Verify that the requesting user is the same as the user in the URL
    if not verify_user_owns_resource(str(current_user.id), str(user_id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user's todos"
        )

    # Query the specific todo
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    result = await session.execute(statement)
    todo = result.scalar_one_or_none()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Store original completion status for event
    original_completed = todo.completed

    # Toggle the completion status
    if toggle_data.completed is not None:
        todo.completed = toggle_data.completed
    else:
        todo.completed = not todo.completed  # Toggle if not specified

    session.add(todo)
    await session.commit()
    await session.refresh(todo)

    # Publish event to Kafka via Dapr
    try:
        with DaprClient() as dapr_client:
            event_data = {
                "event_type": "todo.completed" if todo.completed else "todo.uncompleted",
                "todo_id": str(todo_id),
                "user_id": str(user_id),
                "original_completed": original_completed,
                "new_completed": todo.completed,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            dapr_client.publish_event(
                pubsub_name="pubsub",
                topic_name="todo-events",
                data=json.dumps(event_data),
                data_content_type="application/json"
            )
            
            # Update in Dapr state store
            dapr_client.save_state(
                store_name="statestore",
                key=f"todo-{todo.id}",
                value=json.dumps({
                    "id": str(todo.id),
                    "title": todo.title,
                    "description": todo.description,
                    "completed": todo.completed,
                    "user_id": str(todo.user_id),
                    "created_at": todo.created_at.isoformat(),
                    "updated_at": todo.updated_at.isoformat()
                })
            )
    except Exception as e:
        logger.error(f"Failed to publish event or update state: {e}")

    return TodoResponse(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        user_id=todo.user_id,
        created_at=todo.created_at,
        updated_at=todo.updated_at
    )