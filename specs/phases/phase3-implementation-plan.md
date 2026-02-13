# Phase III - Implementation Plan

> Last Updated: 2026-02-13
> Version: 1.0.0
> Status: Planned

## References

- @specs/phases/phase3.md
- @specs/api/endpoints.md
- @specs/database/schema.md
- @specs/ui/components.md

## Overview

This document outlines the implementation plan for Phase III - AI Todo Chatbot with MCP and Agents.

## Implementation Strategy

Following clean architecture principles, we'll implement in parallel tracks:
1. Backend (MCP server and AI agent integration)
2. Frontend (ChatKit UI for AI interaction)
3. Database (Conversation and message persistence)

We'll follow a test-driven approach where possible, implementing MCP tools first, then connecting them to the AI agent, and finally building the frontend interface.

## Step-by-Step Implementation

### Step 1: Database Schema & Models

**Files to create:**
- `backend/models/conversation.py`
- `backend/models/message.py`
- Update existing models as needed

**Implementation details:**
- Define SQLModel models for Conversation and Message
- Set up relationships between models
- Configure database session with Neon PostgreSQL

### Step 2: MCP Server Implementation

**Files to create:**
- `backend/mcp/__init__.py`
- `backend/mcp/server.py`
- `backend/mcp/protocol.py`

**Implementation details:**
- Implement MCP protocol for tool discovery
- Create standardized tool endpoints
- Handle bidirectional communication
- Implement tool registration and execution

### Step 3: MCP Tools Implementation

**Files to create:**
- `backend/agents/tools/__init__.py`
- `backend/agents/tools/add_task.py`
- `backend/agents/tools/list_tasks.py`
- `backend/agents/tools/update_task.py`
- `backend/agents/tools/complete_task.py`
- `backend/agents/tools/delete_task.py`

**Implementation details:**
- Implement all required MCP tools
- Connect to existing todo functionality
- Handle input validation and error cases
- Return appropriate responses

### Step 4: AI Agent Integration

**Files to create:**
- `backend/agents/__init__.py`
- `backend/agents/todo_agent.py`
- `backend/agents/intent_detector.py`

**Implementation details:**
- Create OpenAI agent with todo-specific tools
- Implement intent detection and mapping
- Handle conversation memory and context
- Manage conversation state

### Step 5: Backend API Extensions

**Files to create/modify:**
- `backend/api/chat.py`
- Update `backend/main.py` to include new routes

**Implementation details:**
- Implement chat endpoint for natural language processing
- Add conversation management endpoints
- Connect to AI agent and MCP tools
- Handle authentication and authorization

### Step 6: Frontend Setup

**Files to create:**
- `frontend/components/chat/chat-interface.tsx`
- `frontend/components/chat/message-list.tsx`
- `frontend/components/chat/message-input.tsx`
- `frontend/hooks/use-chat.ts`

**Implementation details:**
- Create real-time messaging interface
- Implement message history and scroll management
- Add typing indicators and loading states
- Connect to backend chat API

### Step 7: Documentation

**Files to create/modify:**
- `README.md` - Installation and usage instructions
- `CLAUDE.md` - AI assistant context

**README.md content:**
- Project description
- Prerequisites
- Installation instructions
- Environment variables
- Running locally
- API documentation reference
- Project structure

## Implementation Tasks

### Task 1: Create Database Models
- [ ] Create Conversation model
- [ ] Create Message model with relationships
- [ ] Update database session
- [ ] Test database connections

### Task 2: Implement MCP Server
- [ ] Create MCP protocol implementation
- [ ] Implement tool discovery mechanism
- [ ] Create tool registration system
- [ ] Test MCP communication

### Task 3: Implement MCP Tools
- [ ] Create add_task tool
- [ ] Create list_tasks tool
- [ ] Create update_task tool
- [ ] Create complete_task tool
- [ ] Create delete_task tool
- [ ] Test all tools individually

### Task 4: Integrate AI Agent
- [ ] Create OpenAI agent instance
- [ ] Implement intent detection
- [ ] Connect to MCP tools
- [ ] Test AI responses

### Task 5: Extend Backend API
- [ ] Create chat API endpoints
- [ ] Implement conversation management
- [ ] Connect to AI agent
- [ ] Test API endpoints

### Task 6: Build Frontend Components
- [ ] Create chat interface component
- [ ] Create message list component
- [ ] Create message input component
- [ ] Implement useChat hook
- [ ] Connect to backend API

### Task 7: Testing & Validation
- [ ] Test natural language processing
- [ ] Test conversation persistence
- [ ] Test error handling
- [ ] Validate against acceptance criteria

### Task 8: Documentation
- [ ] Write README.md
- [ ] Write CLAUDE.md
- [ ] Document API endpoints
- [ ] Add setup instructions

## MCP Tool Implementation

### add_task Tool
```python
def add_task(description: str, due_date: Optional[str] = None) -> dict:
    """
    Add a new task based on natural language description
    """
    # Parse description to extract task details
    # Create new todo via existing service
    # Return confirmation
```

### list_tasks Tool
```python
def list_tasks(filter_criteria: Optional[dict] = None) -> dict:
    """
    Retrieve and display user's tasks
    """
    # Apply filters if provided
    # Return list of tasks
```

### update_task Tool
```python
def update_task(task_id: str, updates: dict) -> dict:
    """
    Modify an existing task
    """
    # Validate task exists and belongs to user
    # Apply updates
    # Return confirmation
```

### complete_task Tool
```python
def complete_task(task_id: str) -> dict:
    """
    Mark a task as completed
    """
    # Validate task exists and belongs to user
    # Update completion status
    # Return confirmation
```

### delete_task Tool
```python
def delete_task(task_id: str) -> dict:
    """
    Remove a task
    """
    # Validate task exists and belongs to user
    # Delete task
    # Return confirmation
```

## AI Agent Implementation

### Intent Detection
- Use OpenAI's function calling to detect user intent
- Map natural language to specific actions
- Handle ambiguous requests with clarifications
- Maintain conversation context

### Response Generation
- Generate natural language responses
- Provide helpful feedback and suggestions
- Handle errors gracefully
- Maintain conversation flow

## Testing Plan

### Backend Testing Commands

1. **Start backend:**
```bash
cd backend
uv run uvicorn main:app --reload
```

2. **Test chat endpoint:**
```bash
curl -X POST \
     -H "Authorization: Bearer <JWT_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"message": "Add a task to buy groceries tomorrow"}' \
     http://localhost:8000/api/v1/chat
```

### Frontend Testing Commands

1. **Start frontend:**
```bash
cd frontend
npm run dev
```

2. **Access at:**
- Frontend: http://localhost:3000/chat
- Backend API docs: http://localhost:8000/docs

### Expected Behaviors

| Action | Expected Result |
|--------|----------------|
| "Add a task to buy groceries" | Task added with title "buy groceries" |
| "Show me my tasks" | List of user's tasks displayed |
| "Mark task #1 as complete" | Task #1 marked as complete |
| "Delete task #2" | Task #2 removed from list |
| Unclear request | AI asks for clarification |

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| AI misinterpreting commands | Implement robust intent detection with fallbacks |
| MCP protocol compatibility | Follow MCP specification closely |
| Performance degradation | Optimize AI calls and implement caching |
| Security vulnerabilities | Sanitize all AI inputs and outputs |
| Conversation context loss | Implement proper state management |

## Success Criteria

- Natural language commands work reliably
- MCP tools follow standard protocol
- AI clarifies ambiguous requests appropriately
- Conversation context is maintained properly
- Response times meet performance requirements
- Clean architecture principles followed
- Documentation is complete and accurate
- Application runs locally with all features working