# Todo Application Backend - Phase IV - Claude Code Context

> Last Updated: 2026-02-13
> Phase: IV
> Status: Implementation in Progress

## Backend Overview

This is the FastAPI backend for Phase IV of the Todo Application, deployed in a Kubernetes environment. It provides API endpoints for todo management with authentication and database integration.

## Architecture

### Tech Stack
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: PostgreSQL (via Kubernetes StatefulSet)
- **Authentication**: JWT with Better Auth
- **Containerization**: Docker with multi-stage build
- **Orchestration**: Kubernetes Deployment/Service

### Kubernetes Architecture Layers
1. **Domain Layer** (`models/`): Entities and repository interfaces
2. **Infrastructure Layer** (`database/`): Database session management
3. **Application Layer** (`api/`, `core/`): Business logic and security
4. **Presentation Layer** (`main.py`): API endpoints and application setup
5. **Container Layer**: Docker image with optimized runtime
6. **Orchestration Layer**: Kubernetes Deployment with resource management

## Key Files and Directories

### `main.py`
- Main FastAPI application entry point
- CORS middleware configuration
- API router inclusion
- Database initialization

### `models/`
- `todo.py` - Todo entity and related schemas
- `user.py` - User entity and related schemas
- `conversation.py` - Conversation entity for AI chat
- `message.py` - Message entity for AI chat

### `api/`
- `todos.py` - Todo-related endpoints with user isolation
- `auth.py` - Authentication endpoints
- `users.py` - User management endpoints
- `chat.py` - AI chat endpoints
- `mcp.py` - Model Context Protocol endpoints

### `database/`
- `session.py` - Database session management with async support

### `core/`
- `config.py` - Application settings and configuration
- `security.py` - JWT utilities and authentication helpers

### `agents/`
- `todo_agent.py` - AI agent for natural language processing
- `tools/` - MCP tools for AI integration

### `mcp/`
- `server.py` - MCP server implementation
- `protocol.py` - MCP protocol definitions

### `schemas/`
- `todo.py` - API request/response schemas for todo operations

### `Dockerfile`
- Multi-stage Dockerfile for optimized image
- Non-root user execution
- Security scanning preparation
- Runtime optimization

## Kubernetes Configuration

### Deployment Configuration
- Resource requests and limits
- Liveness and readiness probes
- Environment variable configuration
- Security context settings

### Service Configuration
- ClusterIP service for internal communication
- Port exposure for API access
- Service discovery within cluster

### Environment Variables
- `DATABASE_URL` - PostgreSQL connection string
- `BETTER_AUTH_SECRET` - JWT secret key
- `OPENAI_API_KEY` - OpenAI API key for AI features
- `DEBUG` - Debug mode flag

## Security Implementation

### Authentication
- JWT token validation on every request
- User ID verification in URL matches token
- Secure credential management via Kubernetes secrets

### Database Security
- Connection pooling with resource limits
- Encrypted connections to PostgreSQL
- Parameterized queries to prevent injection

### Container Security
- Non-root user execution
- Minimal attack surface
- ReadOnlyRootFilesystem security context
- Resource limits to prevent DoS

## API Endpoints

### Todo Endpoints (`/api/v1/{user_id}/todos`)
- `GET /` - Get all todos for a user
- `POST /` - Create a new todo for a user
- `GET /{todo_id}` - Get a specific todo
- `PUT /{todo_id}` - Update a specific todo
- `DELETE /{todo_id}` - Delete a specific todo
- `PATCH /{todo_id}/complete` - Toggle completion status

### Auth Endpoints (`/api/v1/`)
- `GET /me` - Get current user info
- `GET /validate-token` - Validate JWT token

### User Endpoints (`/api/v1/`)
- `POST /users/register` - User registration
- `POST /users/login` - User login

### Chat Endpoints (`/api/v1/`)
- `POST /chat` - Process natural language commands
- `WS /mcp` - WebSocket for MCP communication

## Containerization

### Multi-Stage Build
- Builder stage: Dependencies installation and compilation
- Runtime stage: Minimal runtime environment
- Security scanning integration
- Layer optimization for caching

### Runtime Configuration
- Non-root user execution
- Resource limits and requests
- Health checks and probes
- Environment-based configuration

## Kubernetes Integration

### Deployment Strategy
- Rolling updates for zero-downtime deployments
- Replica management for scalability
- Resource quotas for predictable performance
- Affinity/anti-affinity for distribution

### Service Discovery
- Internal service communication
- Environment-based service URLs
- DNS resolution within cluster
- Load balancing across replicas

## Monitoring & Observability

### Health Checks
- Liveness probe for container health
- Readiness probe for service availability
- Custom health endpoints for application status

### Logging
- Structured logging with correlation IDs
- JSON format for log aggregation
- Request/response logging for debugging
- Error logging with context

## Development Workflow

### Local Development
```bash
# Build Docker image
docker build -t todo-backend:latest .

# Run locally
docker run -p 8000:8000 todo-backend:latest
```

### Kubernetes Deployment
```bash
# Load image to Minikube
minikube image load todo-backend:latest

# Deploy with Helm
helm upgrade --install todo-app k8s/helm/ --namespace todo-app
```

### Testing
```bash
# Run tests in container
docker run todo-backend:latest pytest
```

## Current Implementation Status

### Completed
- Multi-stage Dockerfile with security optimizations
- Kubernetes Deployment and Service manifests
- Helm chart with parameterized configuration
- Health checks and readiness probes
- Security context configuration
- Resource limits and requests

### Phase IV Specific
- Containerized FastAPI application
- Kubernetes-native deployment
- Helm chart for simplified deployment
- Security-hardened container image
- Resource-optimized runtime

### Next Steps
- Performance testing in Kubernetes
- Horizontal Pod Autoscaler configuration
- Advanced monitoring integration
- Security scanning implementation
- Production readiness validation

## Important Notes

- All API endpoints enforce user data isolation
- JWT validation happens at the dependency level
- Database models are designed to work with Neon PostgreSQL
- The application follows FastAPI best practices and Kubernetes conventions
- Container images are optimized for security and size
- Helm charts are parameterized for different environments
- Health checks ensure service availability