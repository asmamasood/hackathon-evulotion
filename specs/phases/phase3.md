# Phase III - AI Todo Chatbot (MCP + Agents) Specification

> Last Updated: 2026-02-13
> Version: 1.0.0
> Status: Planned

## Overview

Phase III introduces AI-powered natural language control of todos using OpenAI Agents SDK and Model Context Protocol (MCP) tools. This transforms the traditional todo app into an intelligent assistant that understands natural language commands.

## References

- @specs/overview.md
- @specs/architecture.md
- @specs/phases/phase2.md

## Objectives

1. Implement natural language processing for todo commands
2. Create MCP tools for AI agent integration
3. Build conversation persistence system
4. Integrate with OpenAI Agents SDK
5. Develop ChatKit frontend for AI interaction

## Features

### Enhanced Todo Features (from Phase II)
- Add task (via natural language)
- View tasks (via natural language)
- Update task (via natural language)
- Delete task (via natural language)
- Mark task complete/incomplete (via natural language)

### New AI Features (Phase III)
- Natural language processing for all commands
- Conversational AI interface
- Intent detection and action mapping
- Conversation history and context management
- Error handling and clarification requests

## MCP Tools (MANDATORY)

### 1. add_task
- **Purpose**: Add a new task based on natural language input
- **Input**: Natural language description of task
- **Output**: Confirmation of task creation
- **Example**: "Add a task to buy groceries tomorrow"

### 2. list_tasks
- **Purpose**: Retrieve and display user's tasks
- **Input**: Filter criteria (optional)
- **Output**: List of tasks with status
- **Example**: "Show me my tasks for today"

### 3. update_task
- **Purpose**: Modify an existing task
- **Input**: Task identifier and new details
- **Output**: Confirmation of update
- **Example**: "Change the deadline of my project task to Friday"

### 4. complete_task
- **Purpose**: Mark a task as completed
- **Input**: Task identifier
- **Output**: Confirmation of completion
- **Example**: "Mark my workout task as done"

### 5. delete_task
- **Purpose**: Remove a task
- **Input**: Task identifier
- **Output**: Confirmation of deletion
- **Example**: "Delete my appointment with John"

## Agent Behavior

### Intent Detection
- Parse user input to identify task operations
- Recognize task attributes (title, description, due date, priority)
- Handle ambiguous requests with clarifications
- Maintain conversation context

### Action Mapping
- Map detected intents to appropriate MCP tools
- Validate required parameters before tool invocation
- Handle partial information with follow-up questions
- Provide natural language feedback

### Error Handling
- Gracefully handle unrecognized commands
- Clarify ambiguous requests
- Recover from tool execution failures
- Maintain conversation flow

## Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Layer                       │
│                 (ChatKit UI)                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Chat Interface (messages, input, history)       │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼ WebSocket/HTTP
┌─────────────────────────────────────────────────────────┐
│                   Backend Layer                         │
│                   (FastAPI)                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ ChatAPI      │ │ MCP Server   │ │ Agent Orch.  │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   AI Agent Layer                        │
│              (OpenAI Agents SDK)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Intent Detect│ │ Tool Executor│ │ Response Gen │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼ MCP Tools
┌─────────────────────────────────────────────────────────┐
│                  MCP Tools Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ add_task     │ │ list_tasks   │ │ update_task  │ │
│  │ complete_task│ │ delete_task  │ │              │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Domain + Infrastructure                 │
│  (Use Cases, Entities, PostgreSQL, Conversation Store)  │
└─────────────────────────────────────────────────────────┘
```

### Database Schema Extensions

#### Conversations Table
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Messages Table
```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Technical Implementation

### OpenAI Agents SDK Integration
- Create agent with todo-specific tools
- Implement conversation memory
- Handle streaming responses
- Manage conversation state

### MCP Server Implementation
- Expose MCP tools as standardized endpoints
- Handle tool discovery and registration
- Implement tool execution protocols
- Support bidirectional communication

### ChatKit Frontend Integration
- Real-time messaging interface
- Typing indicators and loading states
- Message history and scroll management
- Natural language input with smart suggestions

## API Extensions

### New Endpoints
- `POST /api/v1/chat` - Process natural language input
- `GET /api/v1/conversations` - List user conversations
- `GET /api/v1/conversations/{id}` - Get specific conversation
- `POST /api/v1/conversations` - Create new conversation
- `DELETE /api/v1/conversations/{id}` - Delete conversation

### Enhanced Todo Endpoints
- Maintain existing endpoints for backward compatibility
- Add AI-enhanced versions with natural language processing

## Project Structure

```
hackathon-todo/
├── specs/
│   └── phases/
│       └── phase3.md          # ← This file
├── frontend/
│   ├── components/
│   │   └── chat/
│   │       ├── chat-interface.tsx
│   │       ├── message-list.tsx
│   │       └── message-input.tsx
│   └── hooks/
│       └── use-chat.ts
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── todo_agent.py
│   │   └── tools/
│   │       ├── __init__.py
│   │       ├── add_task.py
│   │       ├── list_tasks.py
│   │       ├── update_task.py
│   │       ├── complete_task.py
│   │       └── delete_task.py
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   └── protocol.py
│   ├── api/
│   │   └── chat.py
│   └── models/
│       ├── conversation.py
│       └── message.py
├── CLAUDE.md
└── README.md
```

## Security Considerations

### AI Safety
- Input sanitization for AI prompts
- Rate limiting for AI interactions
- Content filtering for inappropriate requests
- Privacy protection for conversation data

### Data Protection
- Encrypt sensitive conversation data
- Implement proper access controls
- Secure AI model interactions
- Audit AI decision-making processes

## Performance Requirements

### Response Times
- AI response: < 2 seconds for simple operations
- Tool execution: < 500ms
- Database operations: < 200ms
- Frontend updates: < 100ms

### Scalability
- Support concurrent AI conversations
- Efficient message storage and retrieval
- Caching for frequently accessed data
- Resource management for AI operations

## Acceptance Criteria

### Functional Requirements
- [ ] User can add tasks using natural language
- [ ] User can view tasks using natural language
- [ ] User can update tasks using natural language
- [ ] User can delete tasks using natural language
- [ ] User can mark tasks complete/incomplete using natural language
- [ ] AI clarifies ambiguous requests
- [ ] Conversation history persists between sessions
- [ ] MCP tools work as specified

### Non-Functional Requirements
- [ ] Clean architecture separation of concerns
- [ ] Type hints throughout
- [ ] Proper error handling and logging
- [ ] Secure authentication and authorization
- [ ] Performance benchmarks met

### Documentation Requirements
- [ ] README.md with installation and usage instructions
- [ ] CLAUDE.md with AI assistant context
- [ ] API documentation for new endpoints
- [ ] MCP tool specifications

## Deliverables

1. MCP server with standardized tools
2. OpenAI agent with todo-specific capabilities
3. ChatKit frontend with natural language interface
4. Conversation and message persistence
5. Working AI todo chatbot demo
6. Updated documentation

## Success Metrics

- Natural language commands work reliably
- AI clarifies ambiguous requests appropriately
- Conversation context is maintained properly
- MCP tools follow standard protocol
- Response times meet performance requirements
- Documentation is complete and accurate

## Constraints

- MCP tools must follow standard protocol
- AI responses must be safe and appropriate
- Conversation data must be properly secured
- Existing API endpoints remain backward compatible
- Natural language processing must be reliable

## Future Considerations

### Phase IV Migration Path
- Containerization for AI services
- Kubernetes orchestration
- Advanced AI model management
- Scaling strategies for high concurrency

### Design Decisions for Phase III
- MCP chosen for standardized AI tool integration
- OpenAI Agents SDK for robust AI orchestration
- Conversation persistence for context management
- Natural language processing for intuitive interaction