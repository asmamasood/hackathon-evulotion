# Phase II - Full-Stack Web App Specification

> Last Updated: 2026-02-13
> Version: 1.0.0
> Status: Planned

## Overview

Phase II transforms the Phase I console application into a **multi-user web application** with persistent storage using Neon PostgreSQL and JWT-based authentication via Better Auth.

## References

- @specs/overview.md
- @specs/architecture.md
- @specs/phases/phase1.md

## Objectives

1. Transform in-memory CLI app to persistent web app
2. Implement multi-user support with authentication
3. Add persistent storage with Neon PostgreSQL
4. Implement JWT-based authentication via Better Auth
5. Create responsive frontend with Next.js
6. Enforce user data isolation on backend

## Features

### Enhanced Todo Features (from Phase I)
- Add task (title + description)
- View tasks (status indicator)
- Update task
- Delete task
- Mark task complete/incomplete

### New Features (Phase II)
- User registration and login
- Multi-user support with data isolation
- Persistent storage
- Responsive web interface
- API endpoints for all operations

## Requirements

### Technology Stack
- Frontend: Next.js 16+ (App Router, TypeScript, Tailwind)
- Backend: FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Auth: Better Auth (JWT)
- Package Manager: UV

### API Endpoints
```
GET    /api/{user_id}/tasks          # Get user's tasks
POST   /api/{user_id}/tasks          # Create new task for user
GET    /api/{user_id}/tasks/{id}     # Get specific task
PUT    /api/{user_id}/tasks/{id}     # Update specific task
DELETE /api/{user_id}/tasks/{id}     # Delete specific task
PATCH  /api/{user_id}/tasks/{id}/complete  # Toggle completion status
```

### Auth Rules
- JWT required on all endpoints
- Token from Better Auth
- Shared secret via BETTER_AUTH_SECRET
- Backend verifies JWT
- user_id in URL must match token

### Database Schema
```sql
-- Users table (handled by Better Auth)
-- Todos table
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    user_id UUID NOT NULL,  -- Foreign key to Better Auth user
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Project Structure
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
│       ├── phase2.md          # ← This file
│       ├── phase3.md
│       ├── phase4.md
│       └── phase5.md
├── frontend/
│   ├── CLAUDE.md
│   ├── package.json
│   ├── next.config.js
│   ├── tsconfig.json
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── register/
│   │   │   └── page.tsx
│   │   └── dashboard/
│   │       └── page.tsx
│   ├── components/
│   │   ├── ui/
│   │   │   ├── todo-list.tsx
│   │   │   ├── todo-form.tsx
│   │   │   └── todo-item.tsx
│   │   └── auth/
│   │       └── auth-provider.tsx
│   ├── lib/
│   │   ├── auth.ts
│   │   └── api.ts
│   └── styles/
│       └── globals.css
├── backend/
│   ├── CLAUDE.md
│   ├── pyproject.toml
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── todo.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── todos.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── session.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   └── schemas/
│       ├── __init__.py
│       ├── user.py
│       └── todo.py
├── CLAUDE.md
├── docker-compose.yml
└── README.md
```

### Domain Model Evolution

#### Todo Entity (Enhanced from Phase I)
```python
class Todo(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to user
    user: Optional[User] = Relationship(back_populates="todos")
```

#### User Entity (New for Phase II)
```python
class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to todos
    todos: List[Todo] = Relationship(back_populates="user")
```

### API Design Principles

#### Authentication
- All endpoints require JWT token in Authorization header
- Token validated against Better Auth
- User ID extracted from token and compared with URL parameter
- 401 Unauthorized for invalid tokens
- 403 Forbidden for user mismatch

#### Error Handling
- Consistent error response format
- Proper HTTP status codes
- User-friendly error messages
- No sensitive information in error responses

#### Response Format
```json
{
  "success": true,
  "data": {},
  "message": "Operation successful"
}
```

### Frontend Requirements

#### Pages
- Landing page with app overview
- Login page with JWT authentication
- Registration page (if needed)
- Dashboard with todo list and management

#### Components
- Todo list component
- Todo form component
- Todo item component with completion toggle
- Authentication provider component

#### Styling
- Responsive design using Tailwind CSS
- Mobile-first approach
- Consistent color scheme and typography
- Accessible UI components

### Security Requirements

#### Authentication & Authorization
- JWT tokens validated on every request
- User data isolation enforced server-side
- No client-side user ID manipulation allowed
- Secure token storage and transmission

#### Input Validation
- Server-side validation for all inputs
- SQL injection prevention via SQLModel
- XSS prevention via React framework
- Rate limiting for authentication endpoints

#### Data Protection
- HTTPS in production
- Secure headers
- Proper CORS configuration
- Environment-based secret management

## Acceptance Criteria

### Functional Requirements
- [ ] User can register/login via Better Auth
- [ ] User can create new todo items
- [ ] User can view their own todo items only
- [ ] User can update their own todo items
- [ ] User can delete their own todo items
- [ ] User can mark their own todo items as complete/incomplete
- [ ] User cannot access other users' todo items
- [ ] All API endpoints work as specified
- [ ] Frontend is responsive and user-friendly

### Non-Functional Requirements
- [ ] Clean architecture separation of concerns
- [ ] Type hints throughout
- [ ] Proper error handling and logging
- [ ] Secure authentication and authorization
- [ ] Performance benchmarks met
- [ ] Database queries optimized

### Documentation Requirements
- [ ] README.md with installation and usage instructions
- [ ] CLAUDE.md with AI assistant context for each component
- [ ] API documentation via FastAPI automatic docs
- [ ] Database schema documentation

## Deliverables

1. Constitution file (CLAUDE.md at root and component levels)
2. `/specs` with full history (this spec and related specs)
3. `/frontend` Next.js application with responsive UI
4. `/backend` FastAPI application with authentication
5. `/database` Neon PostgreSQL schema and migrations
6. Working full-stack demo
7. README.md with setup and usage instructions

## Success Metrics

- All required features implemented
- Multi-user data isolation enforced
- Authentication working via Better Auth
- Responsive frontend with good UX
- Clean architecture principles followed
- Documentation is complete and accurate

## Constraints

- User data must be isolated (no cross-user access)
- JWT authentication required on all endpoints
- Better Auth integration mandatory
- Neon PostgreSQL required for persistence
- Next.js App Router required for frontend

## Future Considerations

### Phase III Migration Path
- Domain layer remains largely unchanged
- API endpoints remain compatible
- New MCP tools layer added
- AI agent integration points prepared
- Conversation storage added

### Design Decisions for Phase II
- Better Auth chosen for JWT management
- SQLModel selected for type-safe ORM
- Next.js App Router for modern React development
- Tailwind CSS for responsive styling