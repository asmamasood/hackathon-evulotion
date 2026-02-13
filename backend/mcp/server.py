"""
MCP (Model Context Protocol) server for the Todo application
"""

from typing import Dict, Any, List
import json
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel


class MCPTask(BaseModel):
    """Base class for MCP tasks"""
    method: str
    params: Dict[str, Any]
    id: str


class MCPResult(BaseModel):
    """Base class for MCP results"""
    result: Dict[str, Any]
    id: str


class MCPError(BaseModel):
    """Base class for MCP errors"""
    error: Dict[str, Any]
    id: str


class MCPServer:
    """
    Model Context Protocol server implementation
    """
    
    def __init__(self):
        self.tools = {}
        self.sessions = {}
    
    def register_tool(self, name: str, handler):
        """
        Register a tool with the MCP server
        """
        self.tools[name] = handler
    
    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a registered tool with given parameters
        """
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        handler = self.tools[tool_name]
        return await handler(**params) if callable(handler) else handler(params)
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get list of available tools
        """
        return [{"name": name, "description": getattr(handler, '__doc__', '')} 
                for name, handler in self.tools.items()]
    
    async def handle_websocket(self, websocket: WebSocket):
        """
        Handle incoming WebSocket connection for MCP
        """
        await websocket.accept()
        client_id = str(id(websocket))
        self.sessions[client_id] = websocket
        
        try:
            while True:
                data = await websocket.receive_text()
                request = json.loads(data)
                
                method = request.get('method')
                params = request.get('params', {})
                req_id = request.get('id', '')
                
                if method == 'tools/list':
                    # Return available tools
                    tools = self.get_available_tools()
                    response = MCPResult(result={"tools": tools}, id=req_id)
                    await websocket.send_text(response.model_dump_json())
                elif method.startswith('call/'):
                    # Execute a tool
                    tool_name = method.split('/', 1)[1]
                    try:
                        result = await self.execute_tool(tool_name, params)
                        response = MCPResult(result=result, id=req_id)
                        await websocket.send_text(response.model_dump_json())
                    except Exception as e:
                        error_response = MCPError(
                            error={"code": -32603, "message": str(e)}, 
                            id=req_id
                        )
                        await websocket.send_text(error_response.model_dump_json())
                else:
                    error_response = MCPError(
                        error={"code": -32601, "message": f"Method {method} not found"}, 
                        id=req_id
                    )
                    await websocket.send_text(error_response.model_dump_json())
                    
        except WebSocketDisconnect:
            if client_id in self.sessions:
                del self.sessions[client_id]


# Global MCP server instance
mcp_server = MCPServer()