# FastAPI Backend Agent for Hackathon-2-Todo

## Overview
The FastAPI Backend Agent is a specialized component focused on FastAPI backend development for the Hackathon-2-Todo project. It handles request/response validation, authentication integration, and database interactions following FastAPI best practices.

## Features
- FastAPI routing and request/response validation
- Authentication integration (JWT, OAuth)
- Database integration with SQLAlchemy
- Error handling and dependency management
- API optimization and performance tuning
- Security-first implementation

## Components

### Backend Agent
Located at: `.specify/backend/backend-agent.ps1`

The main entry point for backend-related tasks. Use this script to:
- Display backend agent information
- List available backend skills
- Show recommended FastAPI project structure

### Backend Skills
Located at: `.specify/backend/skills/`

Modular skill sets for different backend aspects:
- `routing.md` - FastAPI routing and request/response validation
- `authentication-integration.md` - Authentication integration
- `database-integration.md` - Database integration with SQLAlchemy
- `error-handling.md` - Comprehensive error handling

## Usage

### PowerShell
```powershell
# Show backend agent info and skills
.\.specify\backend\backend-agent.ps1

# List available skills
.\.specify\backend\backend-agent.ps1 -Command skills

# Show recommended FastAPI structure
.\.specify\backend\backend-agent.ps1 -Command structure
```

### From the Backend Agent
The backend agent can be invoked directly to handle backend-related tasks following FastAPI best practices.

## Integration
This backend agent integrates with:
- The auth agent for authentication functionality
- Database systems using SQLAlchemy
- Frontend applications via well-defined API endpoints

## Best Practices
- Follow FastAPI conventions and standards
- Implement security-first approach
- Use asynchronous operations for performance
- Follow RESTful API design principles
- Include comprehensive error handling and logging

## Maintenance
- Regular updates to follow FastAPI best practices
- Security audits for API endpoints
- Performance optimization as needed
- Documentation updates for API changes