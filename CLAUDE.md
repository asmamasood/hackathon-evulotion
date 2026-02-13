# Todo Application - Phase IV - Claude Code Context

> Last Updated: 2026-02-13
> Phase: IV
> Status: Implementation in Progress

## Project Overview

This is Phase IV of the 5-phase Todo Application project. The goal is to containerize the Phase III application and deploy it to a local Kubernetes cluster using Minikube. This phase focuses on cloud-native deployment patterns, containerization, and Kubernetes orchestration.

## Architecture

### Current Architecture
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Kubernetes with Minikube
- **Packaging**: Helm charts for deployment
- **Frontend**: Next.js 14 with App Router
- **Backend**: FastAPI with SQLModel ORM
- **Database**: PostgreSQL with persistent storage
- **Authentication**: JWT-based with Better Auth
- **AI Integration**: OpenAI Agents SDK with MCP tools
- **Package Managers**: UV (Python), npm (JavaScript)

### Kubernetes Architecture Layers
1. **Infrastructure Layer**: Minikube cluster with addons
2. **Platform Layer**: Kubernetes core services (Deployments, Services, Ingress)
3. **Application Layer**: Helm charts with parameterized deployments
4. **Data Layer**: PostgreSQL StatefulSet with persistent volumes
5. **Presentation Layer**: Frontend and backend services

## Key Files and Directories

### Containerization (`/`)
- `frontend/Dockerfile` - Multi-stage Dockerfile for frontend
- `backend/Dockerfile` - Multi-stage Dockerfile for backend

### Kubernetes Manifests (`/k8s/manifests/`)
- `namespace.yaml` - Application namespace definition
- `postgresql/` - PostgreSQL StatefulSet and PVC
- `frontend/` - Frontend deployment and service
- `backend/` - Backend deployment and service
- `ingress.yaml` - Ingress routing configuration
- `secrets.yaml` - Kubernetes secrets
- `configmaps.yaml` - Configuration maps

### Helm Chart (`/k8s/helm/`)
- `Chart.yaml` - Helm chart metadata
- `values.yaml` - Default configuration values
- `templates/` - Parameterized Kubernetes manifests
- `templates/_helpers.tpl` - Helm template helpers
- `templates/frontend/` - Frontend deployment templates
- `templates/backend/` - Backend deployment templates
- `templates/database/` - Database deployment templates
- `templates/ingress/` - Ingress templates

### Scripts (`/k8s/scripts/`)
- `minikube-setup.sh` - Minikube cluster setup
- `deploy.sh` - Application deployment script

## Important Implementation Details

### Containerization Strategy
1. **Multi-stage Builds**: Separate build and runtime stages for optimized images
2. **Security**: Non-root user execution and minimal base images
3. **Optimization**: Alpine Linux base images and layer caching
4. **Scanning**: Vulnerability scanning with Trivy

### Kubernetes Deployment
1. **Namespaces**: Isolated environment with dedicated namespace
2. **StatefulSets**: PostgreSQL with persistent storage
3. **Deployments**: Replica management for frontend and backend
4. **Services**: Internal service discovery and load balancing
5. **Ingress**: External access with path-based routing
6. **PVCs**: Persistent storage for database
7. **Secrets**: Secure management of sensitive data
8. **ConfigMaps**: Configuration management

### Helm Chart Features
1. **Parameterization**: Environment-specific configuration through values
2. **Templating**: Reusable templates with conditional logic
3. **Dependencies**: Subchart management for common components
4. **Hooks**: Pre/post-install hooks for initialization
5. **Rollbacks**: Versioned releases with rollback capabilities

### Security Considerations
1. **Image Security**: Scanning and minimal attack surface
2. **Runtime Security**: Non-root containers and security contexts
3. **Network Security**: Network policies and TLS encryption
4. **Secrets Management**: Encrypted secrets and RBAC
5. **Resource Limits**: CPU and memory constraints

### Monitoring & Observability
1. **Health Checks**: Liveness and readiness probes
2. **Metrics**: Resource utilization and custom metrics
3. **Logging**: Structured logging and aggregation
4. **Tracing**: Distributed tracing for request flows

## Development Workflow

### Local Development
1. **Minikube Setup**: `./k8s/scripts/minikube-setup.sh`
2. **Build Images**: `docker build -t <image> .`
3. **Load Images**: `minikube image load <image>`
4. **Deploy**: `./k8s/scripts/deploy.sh`
5. **Access**: `minikube service <service-name> --url`

### Testing
- **Helm Lint**: `helm lint k8s/helm/`
- **Template Validation**: `helm template k8s/helm/`
- **Deployment Verification**: `kubectl get pods -n todo-app`

## Current Status

Phase IV is currently in implementation phase. The structure is in place with:
- Dockerfiles for frontend and backend with multi-stage builds
- Kubernetes manifests for all components
- Helm chart with parameterized templates
- Minikube setup and deployment scripts
- Security configurations and resource limits

## Next Steps

1. Complete Helm chart validation and testing
2. Implement monitoring and observability stack
3. Add horizontal pod autoscaling
4. Implement CI/CD integration
5. Prepare for Phase V (Cloud deployment)

## Constraints and Requirements

- Must run on local Minikube cluster
- Images must pass security scanning
- Resource limits must be set appropriately
- All secrets must be managed securely
- Helm charts must be parameterized
- Deployment must be reproducible
- Network policies must be implemented
- Health checks must be configured

## Security Considerations

- Image vulnerability scanning
- Non-root container execution
- RBAC configuration
- Network policies
- Secrets encryption
- TLS for all communications
- Resource quotas and limits
- Pod security policies

## Hugging Face Spaces Deployment

The backend application is configured for deployment on Hugging Face Spaces:

### Configuration Files
- `space.py` - Main application entry point for Spaces
- `app.yml` - Hugging Face Space configuration
- `Dockerfile.spaces` - Docker configuration optimized for Spaces
- `requirements.txt` - Python dependencies for Spaces deployment

### Deployment Process
1. Create a new Space on Hugging Face with Docker SDK
2. Add the configuration files to your Space repository
3. Set environment variables in Space settings
4. The Space will automatically build and deploy the backend

### Features Available on Spaces
- Full API functionality via FastAPI
- Authentication and authorization
- Todo management capabilities
- AI integration (if OpenAI API key is provided)
- Health checks and monitoring endpoints