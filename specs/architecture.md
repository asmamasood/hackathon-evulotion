# Todo Application - Architecture

> Last Updated: 2026-02-12
> Version: 1.0.0

## Overview

This document describes the architectural decisions and patterns used throughout the 5-phase development of the Todo application.

## Clean Architecture Principles

The application follows Clean Architecture principles at all phases:

1. **Independence of Frameworks**: Core business logic doesn't depend on external frameworks
2. **Testability**: Business rules can be tested without UI, database, web server
3. **Independence of UI**: UI can change without affecting business rules
4. **Independence of Database**: Business rules don't depend on database technology
5. **Independence of External Agents**: Business rules don't know anything about the outside world

## Phase I - Console Todo App Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Add Command │  │ List Command │  │  ... Command │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Use Case Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ AddTodoUseCase│ │ListTodoUseCase│ │ ...UseCase   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Domain Layer                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Todo (id, title, description, completed)      │  │
│  │  TodoRepository (interface)                    │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Infrastructure Layer                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │  InMemoryTodoRepository                         │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Directory Structure (Phase I)

```
hackathon-todo/
├── .spec-kit/
│   └── config.yaml
├── specs/
│   ├── overview.md
│   ├── architecture.md
│   ├── features/
│   ├── api/
│   ├── database/
│   ├── ui/
│   └── phases/
│       ├── phase1.md
│       ├── phase2.md
│       ├── phase3.md
│       ├── phase4.md
│       └── phase5.md
├── phase1/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py              # CLI entry point
│   │   ├── cli/
│   │   │   ├── __init__.py
│   │   │   └── commands.py      # CLI command handlers
│   │   ├── domain/
│   │   │   ├── __init__.py
│   │   │   ├── todo.py          # Todo entity
│   │   │   └── repository.py    # Repository interface
│   │   ├── use_cases/
│   │   │   ├── __init__.py
│   │   │   ├── add_todo.py      # Add todo use case
│   │   │   ├── list_todos.py    # List todos use case
│   │   │   ├── update_todo.py   # Update todo use case
│   │   │   ├── delete_todo.py   # Delete todo use case
│   │   │   └── complete_todo.py # Complete todo use case
│   │   └── infrastructure/
│   │       ├── __init__.py
│   │       └── in_memory_repository.py
│   ├── pyproject.toml
│   ├── README.md
│   └── CLAUDE.md
├── CLAUDE.md
├── docker-compose.yml
└── README.md
```

## Phase II - Full-Stack Web App Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend Layer                       │
│                    (Next.js 16+)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ TodoListPage │ │ TodoForm     │ │ AuthPage      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼ HTTP/REST
┌─────────────────────────────────────────────────────────┐
│                   API Gateway / Auth                    │
│                   (Better Auth - JWT)                   │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Backend Layer                         │
│                   (FastAPI)                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ TodoAPI      │ │ AuthAPI      │ │ UserAPI       │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Use Case Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ AddTodoUseCase│ │ListTodoUseCase│ │ ...UseCase   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Domain Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Todo         │ │ User         │ │ TodoRepository│ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Infrastructure Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ PostgreSQL   │ │ JWT Validator│ │ Session Store │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Phase III - AI Todo Chatbot Architecture

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

## Phase IV - Local Kubernetes Deployment Architecture

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Minikube Cluster                      │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Namespace: todo-app                 │  │
│  │                                                  │  │
│  │  ┌──────────────┐  ┌──────────────┐            │  │
│  │  │  Frontend    │  │   Backend    │            │  │
│  │  │  (Pod)       │  │   (Pod)      │            │  │
│  │  └──────────────┘  └──────────────┘            │  │
│  │         │                 │                     │  │
│  │         ▼                 ▼                     │  │
│  │  ┌──────────────┐  ┌──────────────┐            │  │
│  │  │   Service    │  │   Service    │            │  │
│  │  └──────────────┘  └──────────────┘            │  │
│  │         │                 │                     │  │
│  │         ▼                 ▼                     │  │
│  │  ┌──────────────┐  ┌──────────────┐            │  │
│  │  │   Ingress    │  │             │            │  │
│  │  └──────────────┘  └──────────────┘            │  │
│  │                                                  │  │
│  │  ┌──────────────────────────────────────────┐  │  │
│  │  │     PostgreSQL (StatefulSet)            │  │  │
│  │  └──────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Phase V - Advanced Cloud Deployment Architecture

### Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AKS / GKE Cluster                           │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                  Dapr Sidecar Pattern                      │    │
│  │                                                              │    │
│  │  ┌──────────────┐      ┌──────────────┐                     │    │
│  │  │  Frontend    │◄────►│  Dapr S.S.   │                     │    │
│  │  └──────────────┘      └──────────────┘                     │    │
│  │                              │                               │    │
│  │  ┌──────────────┐      ┌──────────────┐                     │    │
│  │  │  Backend     │◄────►│  Dapr S.S.   │                     │    │
│  │  └──────────────┘      └──────────────┘                     │    │
│  │                              │                               │    │
│  │  ┌──────────────┐      ┌──────────────┐                     │    │
│  │  │  Worker      │◄────►│  Dapr S.S.   │                     │    │
│  │  └──────────────┘      └──────────────┘                     │    │
│  └────────────────────────────────────────────────────────────┘    │
│                              │                                     │
│                              ▼                                     │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                     Dapr Building Blocks                    │    │
│  │                                                              │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │    │
│  │  │ State Store  │  │   Pub/Sub    │  │    Cron      │      │    │
│  │  │ (Redis/Cosmos)│  │   (Kafka)    │  │              │      │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘      │    │
│  │                                                              │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │    │
│  │  │   Secrets    │  │ Bindings     │  │ Observability│      │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘      │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                     Kafka Topics                            │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │    │
│  │  │todo-created  │ │todo-updated  │ │todo-deleted  │      │    │
│  │  │todo-completed│ │reminder-due  │ │...           │      │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘      │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

## Design Patterns Used

### Domain-Driven Design (DDD)
- **Entities**: Core domain objects (Todo, User)
- **Value Objects**: Immutable values (TaskId, UserId)
- **Repositories**: Collections of domain objects
- **Use Cases**: Application business logic

### Repository Pattern
- Abstracts data access logic
- Enables swapping implementations (in-memory → PostgreSQL)
- Supports testing with mock implementations

### Dependency Inversion Principle
- High-level modules don't depend on low-level modules
- Both depend on abstractions (interfaces)
- Enables flexible architecture

### MVC (Model-View-Controller)
- Frontend: React components (View) → API calls (Controller) → Domain (Model)
- Backend: FastAPI routes (Controller) → Use cases → Domain

### Event-Driven Architecture (Phase V)
- Decoupled services via Kafka
- Async processing for background tasks
- Event sourcing capabilities

## Security Architecture

### Authentication & Authorization
- **Phase I**: None (local CLI)
- **Phase II+**: JWT-based authentication via Better Auth
- **User Isolation**: Backend enforces user_id matching
- **Role-Based Access**: Future extensibility for roles/permissions

### Data Protection
- Input validation on all endpoints
- SQL injection prevention via ORM (SQLModel)
- XSS prevention via React framework
- CSRF protection via SameSite cookies

### Secrets Management
- Environment variables for sensitive data
- Dapr Secrets management (Phase V)
- No hardcoded credentials in source code