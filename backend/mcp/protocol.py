"""
MCP (Model Context Protocol) definitions for the Todo application
"""

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel


class MCPMethod(str(Enum):
    """MCP method types"""
    LIST_TOOLS = "tools/list"
    CALL_TOOL = "call/"
    INIT_HELLO = "initialize"
    INIT_COMPLETE = "initialized"


class MCPRequest(BaseModel):
    """MCP request model"""
    method: str
    params: Optional[Dict[str, Any]] = None
    id: Optional[str] = None


class MCPResponse(BaseModel):
    """MCP response model"""
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[str] = None


class ToolDefinition(BaseModel):
    """Definition of an MCP tool"""
    name: str
    description: str
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None


# Common tool schemas
ADD_TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "The title of the task"},
        "description": {"type": "string", "description": "Detailed description of the task"},
        "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD format"}
    },
    "required": ["title"]
}

LIST_TASKS_SCHEMA = {
    "type": "object",
    "properties": {
        "filter": {"type": "string", "description": "Filter criteria (e.g., 'completed', 'pending', 'today')"}
    }
}

UPDATE_TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "task_id": {"type": "string", "description": "ID of the task to update"},
        "title": {"type": "string", "description": "New title for the task"},
        "description": {"type": "string", "description": "New description for the task"},
        "due_date": {"type": "string", "description": "New due date in YYYY-MM-DD format"}
    },
    "required": ["task_id"]
}

COMPLETE_TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "task_id": {"type": "string", "description": "ID of the task to mark as complete"}
    },
    "required": ["task_id"]
}

DELETE_TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "task_id": {"type": "string", "description": "ID of the task to delete"}
    },
    "required": ["task_id"]
}