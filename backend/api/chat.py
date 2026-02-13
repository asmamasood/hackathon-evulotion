"""
API router for chat-related endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from typing import Dict, Any
from uuid import UUID
from models.user import User
from core.security import get_current_user
from agents.todo_agent import todo_agent
from mcp.server import mcp_server


router = APIRouter()


@router.post("/chat")
async def process_chat_message(
    message: str,
    current_user: User = Depends(get_current_user)
):
    """
    Process a natural language message and return a response
    """
    try:
        response = await todo_agent.process_message(
            message=message,
            user_id=str(current_user.id)
        )
        return {
            "success": True,
            "response": response,
            "user_id": str(current_user.id)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )


@router.websocket("/mcp")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for MCP communication
    """
    await mcp_server.handle_websocket(websocket)