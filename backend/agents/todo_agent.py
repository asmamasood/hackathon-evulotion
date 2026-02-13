"""
AI Todo Agent for the Todo application
"""

from typing import Dict, Any, List
from openai import AsyncOpenAI
from .tools.add_task import add_task
from .tools.list_tasks import list_tasks
from .tools.update_task import update_task
from .tools.complete_task import complete_task
from .tools.delete_task import delete_task
from mcp.server import mcp_server
from database.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import os


class TodoAgent:
    """
    AI agent for handling todo-related natural language commands
    """
    
    def __init__(self, api_key: str = None):
        if api_key:
            self.client = AsyncOpenAI(api_key=api_key)
        else:
            # Try to get API key from environment
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.client = AsyncOpenAI(api_key=api_key)
            else:
                # For development, we'll use a mock implementation
                self.client = None
            
        # Register MCP tools
        mcp_server.register_tool("add_task", self.execute_add_task)
        mcp_server.register_tool("list_tasks", self.execute_list_tasks)
        mcp_server.register_tool("update_task", self.execute_update_task)
        mcp_server.register_tool("complete_task", self.execute_complete_task)
        mcp_server.register_tool("delete_task", self.execute_delete_task)
    
    async def execute_add_task(self, **params) -> Dict[str, Any]:
        """
        Execute the add_task tool
        """
        async with get_async_session() as session:
            return await add_task(
                title=params.get('title'),
                description=params.get('description'),
                user_id=params.get('user_id'),
                session=session
            )
    
    async def execute_list_tasks(self, **params) -> Dict[str, Any]:
        """
        Execute the list_tasks tool
        """
        async with get_async_session() as session:
            return await list_tasks(
                user_id=params.get('user_id'),
                filter_criteria=params.get('filter'),
                session=session
            )
    
    async def execute_update_task(self, **params) -> Dict[str, Any]:
        """
        Execute the update_task tool
        """
        async with get_async_session() as session:
            return await update_task(
                task_id=params.get('task_id'),
                user_id=params.get('user_id'),
                title=params.get('title'),
                description=params.get('description'),
                completed=params.get('completed'),
                session=session
            )
    
    async def execute_complete_task(self, **params) -> Dict[str, Any]:
        """
        Execute the complete_task tool
        """
        async with get_async_session() as session:
            return await complete_task(
                task_id=params.get('task_id'),
                user_id=params.get('user_id'),
                session=session
            )
    
    async def execute_delete_task(self, **params) -> Dict[str, Any]:
        """
        Execute the delete_task tool
        """
        async with get_async_session() as session:
            return await delete_task(
                task_id=params.get('task_id'),
                user_id=params.get('user_id'),
                session=session
            )
    
    async def process_message(self, message: str, user_id: str) -> str:
        """
        Process a natural language message and return a response
        """
        # If we have an OpenAI client, use it for intent detection
        if self.client:
            return await self.process_with_openai(message, user_id)
        else:
            # Fallback to keyword-based approach
            return await self.process_with_keywords(message, user_id)
    
    async def process_with_openai(self, message: str, user_id: str) -> str:
        """
        Process message using OpenAI API for intent detection
        """
        try:
            # Define the tools that the AI can use
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "add_task",
                        "description": "Add a new task to the user's todo list",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string", "description": "The title of the task"},
                                "description": {"type": "string", "description": "Detailed description of the task"},
                                "user_id": {"type": "string", "description": "The ID of the user"}
                            },
                            "required": ["title", "user_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "list_tasks",
                        "description": "List all tasks for the user",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "user_id": {"type": "string", "description": "The ID of the user"},
                                "filter": {"type": "string", "description": "Filter criteria (e.g., 'completed', 'pending', 'today', 'all')"}
                            },
                            "required": ["user_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "update_task",
                        "description": "Update an existing task",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "string", "description": "The ID of the task to update"},
                                "user_id": {"type": "string", "description": "The ID of the user"},
                                "title": {"type": "string", "description": "New title for the task"},
                                "description": {"type": "string", "description": "New description for the task"},
                                "completed": {"type": "boolean", "description": "Whether the task is completed"}
                            },
                            "required": ["task_id", "user_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "complete_task",
                        "description": "Mark a task as completed",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "string", "description": "The ID of the task to mark as complete"},
                                "user_id": {"type": "string", "description": "The ID of the user"}
                            },
                            "required": ["task_id", "user_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "delete_task",
                        "description": "Delete a task",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "string", "description": "The ID of the task to delete"},
                                "user_id": {"type": "string", "description": "The ID of the user"}
                            },
                            "required": ["task_id", "user_id"]
                        }
                    }
                }
            ]
            
            # Call the OpenAI API with the message and tools
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that manages todo lists. Use the available functions to help the user manage their tasks. Always respond with the appropriate function call based on the user's request."},
                    {"role": "user", "content": message}
                ],
                tools=tools,
                tool_choice="auto"
            )
            
            # Process the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            
            if tool_calls:
                # Execute the tool calls
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = eval(tool_call.function.arguments)  # In production, use json.loads
                    
                    # Add user_id to function args if not present
                    if 'user_id' not in function_args:
                        function_args['user_id'] = user_id
                    
                    # Execute the appropriate function
                    if function_name == "add_task":
                        result = await self.execute_add_task(**function_args)
                        return result.get('message', 'Task added successfully!')
                    elif function_name == "list_tasks":
                        result = await self.execute_list_tasks(**function_args)
                        tasks = result.get('tasks', [])
                        if tasks:
                            task_list = "\n".join([f"- {task['title']} ({'completed' if task['completed'] else 'pending'})" 
                                                  for task in tasks])
                            return f"Your tasks:\n{task_list}"
                        else:
                            return "You have no tasks."
                    elif function_name == "update_task":
                        result = await self.execute_update_task(**function_args)
                        return result.get('message', 'Task updated successfully!')
                    elif function_name == "complete_task":
                        result = await self.execute_complete_task(**function_args)
                        return result.get('message', 'Task completed!')
                    elif function_name == "delete_task":
                        result = await self.execute_delete_task(**function_args)
                        return result.get('message', 'Task deleted!')
                    else:
                        return f"Unknown function: {function_name}"
            else:
                # If no tool calls were made, return the assistant's message
                return response_message.content or "I processed your request."
        except Exception as e:
            # Fallback to keyword-based approach if OpenAI fails
            print(f"OpenAI processing failed: {str(e)}")
            return await self.process_with_keywords(message, user_id)
    
    async def process_with_keywords(self, message: str, user_id: str) -> str:
        """
        Process a natural language message using keyword detection
        """
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['add', 'create', 'new', 'make']):
            # Extract task details from message
            task_title = self.extract_task_title(message)
            if task_title:
                try:
                    result = await self.execute_add_task(
                        title=task_title,
                        user_id=user_id
                    )
                    return result.get('message', 'Task added successfully!')
                except Exception as e:
                    return f"Error adding task: {str(e)}"
        
        elif any(word in message_lower for word in ['show', 'list', 'view', 'see']):
            try:
                result = await self.execute_list_tasks(user_id=user_id)
                tasks = result.get('tasks', [])
                if tasks:
                    task_list = "\n".join([f"- {task['title']} ({'completed' if task['completed'] else 'pending'})" 
                                          for task in tasks])
                    return f"Your tasks:\n{task_list}"
                else:
                    return "You have no tasks."
            except Exception as e:
                return f"Error listing tasks: {str(e)}"
        
        elif any(word in message_lower for word in ['complete', 'done', 'finish', 'completed']):
            # Simple implementation - would need more sophisticated parsing
            try:
                # For now, assume user wants to complete the first task
                result = await self.execute_list_tasks(user_id=user_id)
                tasks = result.get('tasks', [])
                if tasks:
                    first_task = tasks[0]
                    complete_result = await self.execute_complete_task(
                        task_id=first_task['id'],
                        user_id=user_id
                    )
                    return complete_result.get('message', 'Task completed!')
                else:
                    return "You have no tasks to complete."
            except Exception as e:
                return f"Error completing task: {str(e)}"
        
        elif any(word in message_lower for word in ['delete', 'remove', 'cancel']):
            # Simple implementation - would need more sophisticated parsing
            try:
                # For now, assume user wants to delete the first task
                result = await self.execute_list_tasks(user_id=user_id)
                tasks = result.get('tasks', [])
                if tasks:
                    first_task = tasks[0]
                    delete_result = await self.execute_delete_task(
                        task_id=first_task['id'],
                        user_id=user_id
                    )
                    return delete_result.get('message', 'Task deleted!')
                else:
                    return "You have no tasks to delete."
            except Exception as e:
                return f"Error deleting task: {str(e)}"
        
        else:
            return "I'm not sure how to handle that request. You can ask me to add, list, complete, or delete tasks."
    
    def extract_task_title(self, message: str) -> str:
        """
        Extract task title from natural language message
        This is a simple implementation - in reality, this would use NLP
        """
        # Remove common phrases
        message = message.replace("add a task to", "").replace("add task to", "").strip()
        message = message.replace("create a task to", "").replace("create task to", "").strip()
        message = message.replace("new task:", "").replace("task:", "").strip()
        
        # Take the first part of the message as the title
        # In a real implementation, this would be much more sophisticated
        return message.split('.')[0].split(',')[0].strip()


# Global todo agent instance
todo_agent = TodoAgent()