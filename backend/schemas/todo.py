"""
API request/response schemas for the Todo application
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class TodoCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None


class TodoUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class TodoToggleCompleteRequest(BaseModel):
    completed: Optional[bool] = None


class TodoResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    completed: bool
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TodoListResponse(BaseModel):
    todos: list[TodoResponse]
    count: int


class ApiResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    success: bool
    message: str
    error_code: Optional[str] = None