# Phase II - Implementation Plan

> Last Updated: 2026-02-13
> Version: 1.0.0
> Status: Planned

## References

- @specs/phases/phase2.md
- @specs/api/endpoints.md
- @specs/database/schema.md
- @specs/ui/components.md

## Overview

This document outlines the implementation plan for Phase II - Full-Stack Web App.

## Implementation Strategy

Following clean architecture principles, we'll implement in parallel tracks:
1. Backend (FastAPI + SQLModel + Neon PostgreSQL)
2. Frontend (Next.js + TypeScript + Tailwind)
3. Authentication (Better Auth integration)

We'll follow a test-driven approach where possible, implementing API endpoints first, then connecting them to the frontend.

## Step-by-Step Implementation

### Step 1: Project Setup

**Tasks:**
1. Create directory structure
2. Initialize UV project for backend
3. Initialize Next.js project for frontend
4. Create docker-compose.yml for local development
5. Set up shared configuration

**Commands:**
```bash
# Backend setup
mkdir -p backend/{models,api,database,core,schemas}
cd backend
uv init --no-readme
touch main.py

# Frontend setup
mkdir -p frontend/{app,components,lib,styles}
cd frontend
npm create next-app@latest . --typescript --tailwind --eslint --app --no-src-dir --no-import-alias
```

**pyproject.toml (Backend):**
```toml
[project]
name = "todo-backend"
version = "0.1.0"
description = "Todo Application Backend - Phase II"
requires-python = ">=3.13"
dependencies = [
    "fastapi>=0.104.1",
    "uvicorn>=0.24.0",
    "sqlmodel>=0.0.16",
    "better-auth>=0.0.0-beta.1",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "alembic>=1.13.1",
    "asyncpg>=0.29.0",
    "pydantic-settings>=2.1.0"
]

[project.scripts]
dev = "backend.main:dev"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=7.4.0",
    "httpx>=0.25.0"
]
```

**package.json (Frontend):**
```json
{
  "name": "todo-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "next": "14.0.2",
    "@types/node": "^20.11.5",
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.3.6",
    "better-auth": "^0.0.0-beta.1",
    "typescript": "^5.3.3"
  }
}
```

### Step 2: Database Schema & Models

**Files to create:**
- `backend/models/__init__.py`
- `backend/models/user.py`
- `backend/models/todo.py`
- `backend/database/session.py`
- `backend/core/config.py`

**Implementation details:**
- Define SQLModel models for User and Todo
- Set up database session with Neon PostgreSQL
- Configure connection settings
- Define relationships between models

### Step 3: Backend Core Setup

**Files to create:**
- `backend/core/security.py`
- `backend/schemas/__init__.py`
- `backend/schemas/user.py`
- `backend/schemas/todo.py`

**Implementation details:**
- JWT token validation utilities
- Pydantic schemas for API requests/responses
- Authentication helpers
- Error handling utilities

### Step 4: API Endpoints

**Files to create:**
- `backend/api/__init__.py`
- `backend/api/auth.py`
- `backend/api/todos.py`
- `backend/main.py`

**Implementation details:**
- Implement all required API endpoints
- Add JWT authentication middleware
- Validate user_id matches token
- Return proper HTTP status codes
- Add error handling

### Step 5: Frontend Setup

**Files to create:**
- `frontend/app/layout.tsx`
- `frontend/app/page.tsx`
- `frontend/app/login/page.tsx`
- `frontend/app/dashboard/page.tsx`
- `frontend/components/ui/todo-list.tsx`
- `frontend/components/ui/todo-form.tsx`
- `frontend/components/ui/todo-item.tsx`
- `frontend/lib/api.ts`
- `frontend/lib/auth.ts`

**Implementation details:**
- Create responsive layout with Tailwind
- Implement login page with Better Auth
- Create dashboard with todo management
- Build reusable UI components
- Set up API client for backend communication

### Step 6: Better Auth Integration

**Files to modify:**
- `backend/main.py` (add Better Auth)
- `frontend/components/auth/auth-provider.tsx`
- `frontend/lib/auth.ts`

**Implementation details:**
- Configure Better Auth with JWT
- Set up shared secret
- Implement token validation
- Create auth context provider

### Step 7: Documentation

**Files to create:**
- `README.md` - Installation and usage instructions
- `CLAUDE.md` - AI assistant context
- `docker-compose.yml` - Local development setup

**README.md content:**
- Project description
- Prerequisites
- Installation instructions
- Environment variables
- Running locally
- API documentation reference
- Project structure

## Implementation Tasks

### Task 1: Create Project Structure
- [ ] Create backend directory structure
- [ ] Create frontend directory structure
- [ ] Initialize backend with UV
- [ ] Initialize frontend with Next.js
- [ ] Create docker-compose.yml

### Task 2: Implement Database Models
- [ ] Create User model
- [ ] Create Todo model with relationships
- [ ] Set up database session
- [ ] Configure database settings

### Task 3: Implement Backend Core
- [ ] Create security utilities
- [ ] Create API schemas
- [ ] Set up configuration
- [ ] Test database connection

### Task 4: Implement API Endpoints
- [ ] Create todos API endpoints
- [ ] Add authentication middleware
- [ ] Implement user data isolation
- [ ] Add error handling
- [ ] Test endpoints manually

### Task 5: Integrate Better Auth
- [ ] Configure Better Auth in backend
- [ ] Set up JWT validation
- [ ] Create auth provider for frontend
- [ ] Test authentication flow

### Task 6: Implement Frontend
- [ ] Create layout and routing
- [ ] Build login/register pages
- [ ] Create dashboard page
- [ ] Build todo management components
- [ ] Connect to backend API
- [ ] Add responsive design

### Task 7: Testing & Validation
- [ ] Test authentication flow
- [ ] Test all API endpoints
- [ ] Test frontend functionality
- [ ] Validate user data isolation
- [ ] Test error conditions

### Task 8: Documentation
- [ ] Write README.md
- [ ] Write CLAUDE.md
- [ ] Document API endpoints
- [ ] Add setup instructions

## API Endpoint Implementation

### GET /api/{user_id}/tasks
- Validate JWT token
- Extract user_id from token
- Verify user_id matches URL parameter
- Return user's todos from database

### POST /api/{user_id}/tasks
- Validate JWT token
- Extract user_id from token
- Verify user_id matches URL parameter
- Create new todo with user_id
- Return created todo

### GET /api/{user_id}/tasks/{id}
- Validate JWT token
- Extract user_id from token
- Verify user_id matches URL parameter
- Verify todo belongs to user
- Return specific todo

### PUT /api/{user_id}/tasks/{id}
- Validate JWT token
- Extract user_id from token
- Verify user_id matches URL parameter
- Verify todo belongs to user
- Update todo with provided data
- Return updated todo

### DELETE /api/{user_id}/tasks/{id}
- Validate JWT token
- Extract user_id from token
- Verify user_id matches URL parameter
- Verify todo belongs to user
- Delete todo
- Return success response

### PATCH /api/{user_id}/tasks/{id}/complete
- Validate JWT token
- Extract user_id from token
- Verify user_id matches URL parameter
- Verify todo belongs to user
- Toggle completion status
- Return updated todo

## Authentication Implementation

### Backend Authentication
- Middleware to validate JWT tokens
- Extract user_id from token
- Compare with URL parameter
- Return 403 if mismatch

### Frontend Authentication
- Better Auth client setup
- Protected routes implementation
- Token management
- Redirect to login when unauthorized

## Testing Plan

### Backend Testing Commands

1. **Start backend:**
```bash
cd backend
uv run uvicorn main:app --reload
```

2. **Test endpoints with curl:**
```bash
# Get user's tasks (with valid JWT)
curl -H "Authorization: Bearer <JWT_TOKEN>" \
     http://localhost:8000/api/<USER_ID>/tasks

# Create new task (with valid JWT)
curl -X POST \
     -H "Authorization: Bearer <JWT_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"title":"Test task","description":"Test description"}' \
     http://localhost:8000/api/<USER_ID>/tasks
```

### Frontend Testing Commands

1. **Start frontend:**
```bash
cd frontend
npm run dev
```

2. **Access at:**
- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs

### Expected Behaviors

| Action | Expected Result |
|--------|----------------|
| Access /dashboard without login | Redirect to login |
| Access /dashboard with valid login | Show user's todos |
| Create todo | Added to user's list only |
| Access other user's todos | 403 Forbidden |
| Invalid JWT | 401 Unauthorized |

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Authentication bypass | Double-check user_id validation on every endpoint |
| Cross-user data access | Implement strict user isolation in all queries |
| Database connection issues | Test Neon PostgreSQL connectivity early |
| CORS problems | Configure proper CORS settings |
| JWT validation errors | Thoroughly test token validation logic |

## Success Criteria

- All API endpoints work as specified
- User data isolation enforced on backend
- Authentication working via Better Auth
- Responsive frontend with good UX
- Clean architecture separation maintained
- Documentation is complete and accurate
- Application runs locally with docker-compose