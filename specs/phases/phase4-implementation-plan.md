# Phase IV - Implementation Plan

> Last Updated: 2026-02-13
> Version: 1.0.0
> Status: Planned

## References

- @specs/phases/phase4.md
- @specs/api/endpoints.md
- @specs/database/schema.md
- @specs/ui/components.md

## Overview

This document outlines the implementation plan for Phase IV - Local Kubernetes Deployment.

## Implementation Strategy

Following cloud-native principles, we'll implement in parallel tracks:
1. Containerization (Docker images for frontend and backend)
2. Kubernetes manifests (Deployments, Services, ConfigMaps, etc.)
3. Helm chart creation (templated deployment configurations)
4. Local cluster setup (Minikube configuration)
5. AI-assisted operations (kubectl-ai integration)

We'll follow a test-driven approach where possible, implementing containerization first, then creating Kubernetes resources, and finally building the Helm chart.

## Step-by-Step Implementation

### Step 1: Containerization

**Files to create:**
- `frontend/Dockerfile`
- `backend/Dockerfile`
- `frontend/.dockerignore`
- `backend/.dockerignore`

**Implementation details:**
- Multi-stage builds for optimized images
- Security scanning with Trivy
- Minimal base images (Alpine Linux)
- Non-root user execution
- Environment-based configuration

### Step 2: Kubernetes Manifests

**Files to create:**
- `k8s/manifests/namespace.yaml`
- `k8s/manifests/postgresql/`
- `k8s/manifests/frontend/deployment.yaml`
- `k8s/manifests/frontend/service.yaml`
- `k8s/manifests/backend/deployment.yaml`
- `k8s/manifests/backend/service.yaml`
- `k8s/manifests/ingress.yaml`
- `k8s/manifests/configmaps.yaml`
- `k8s/manifests/secrets.yaml`

**Implementation details:**
- Deployments with rolling updates
- Services with load balancing
- Ingress with TLS termination
- ConfigMaps for configuration
- Secrets for sensitive data
- PersistentVolumeClaims for storage
- NetworkPolicies for security

### Step 3: Helm Chart Creation

**Files to create:**
- `k8s/helm/Chart.yaml`
- `k8s/helm/values.yaml`
- `k8s/helm/templates/_helpers.tpl`
- `k8s/helm/templates/frontend/`
- `k8s/helm/templates/backend/`
- `k8s/helm/templates/database/`
- `k8s/helm/templates/ingress/`
- `k8s/helm/templates/monitoring/`

**Implementation details:**
- Parameterized values for different environments
- Template validation and testing
- Dependency management for common charts
- CI/CD integration for automated deployments

### Step 4: Minikube Setup

**Files to create:**
- `k8s/scripts/minikube-setup.sh`
- `k8s/scripts/deploy.sh`
- `k8s/scripts/scale.sh`
- `k8s/scripts/backup.sh`

**Implementation details:**
- Minikube cluster configuration
- Addon setup (ingress, metrics-server)
- Resource allocation configuration
- Deployment automation scripts

### Step 5: Monitoring & Observability

**Files to create:**
- `k8s/manifests/monitoring/prometheus.yaml`
- `k8s/manifests/monitoring/grafana.yaml`
- `k8s/manifests/monitoring/elasticsearch.yaml`
- `k8s/manifests/monitoring/kibana.yaml`
- `k8s/manifests/monitoring/fluentd.yaml`

**Implementation details:**
- Prometheus for metrics collection
- Grafana for dashboard visualization
- ELK Stack for logging
- Health checks and alerts
- Resource monitoring

### Step 6: Documentation

**Files to create/modify:**
- `README.md` - Installation and deployment instructions
- `CLAUDE.md` - AI assistant context

**README.md content:**
- Project description
- Prerequisites
- Minikube setup instructions
- Deployment instructions
- Environment variables
- Monitoring and logging setup
- Troubleshooting guide

## Implementation Tasks

### Task 1: Create Dockerfiles for Frontend and Backend
- [ ] Create frontend Dockerfile with multi-stage build
- [ ] Create backend Dockerfile with multi-stage build
- [ ] Add .dockerignore files
- [ ] Test Docker builds locally
- [ ] Scan images for vulnerabilities

### Task 2: Create Kubernetes Manifests
- [ ] Create namespace manifest
- [ ] Create PostgreSQL StatefulSet
- [ ] Create frontend deployment and service
- [ ] Create backend deployment and service
- [ ] Create ingress configuration
- [ ] Create ConfigMaps and Secrets
- [ ] Create PersistentVolumeClaims
- [ ] Test manifests on Minikube

### Task 3: Create Helm Chart
- [ ] Initialize Helm chart structure
- [ ] Create parameterized templates for frontend
- [ ] Create parameterized templates for backend
- [ ] Create parameterized templates for database
- [ ] Create ingress template
- [ ] Create values.yaml with defaults
- [ ] Test Helm chart installation
- [ ] Validate chart with Helm lint

### Task 4: Set up Minikube Environment
- [ ] Install Minikube and kubectl
- [ ] Configure Minikube with appropriate resources
- [ ] Enable required addons (ingress, metrics-server)
- [ ] Test basic cluster functionality
- [ ] Verify cluster connectivity

### Task 5: Deploy Application to Minikube
- [ ] Deploy PostgreSQL database
- [ ] Deploy backend service
- [ ] Deploy frontend service
- [ ] Configure ingress routing
- [ ] Test application functionality
- [ ] Verify service connectivity

### Task 6: Set up Monitoring & Observability
- [ ] Deploy Prometheus
- [ ] Deploy Grafana
- [ ] Deploy ELK Stack
- [ ] Configure health checks
- [ ] Set up alerts and notifications
- [ ] Test monitoring functionality

### Task 7: Integrate kubectl-ai
- [ ] Install kubectl-ai plugin
- [ ] Configure AI-assisted operations
- [ ] Test AI-assisted troubleshooting
- [ ] Document AI-assisted workflows

### Task 8: Testing & Validation
- [ ] Test application deployment
- [ ] Test scaling operations
- [ ] Test health checks
- [ ] Validate security configurations
- [ ] Test backup and recovery
- [ ] Validate against acceptance criteria

### Task 9: Documentation
- [ ] Write README.md
- [ ] Write CLAUDE.md
- [ ] Document Helm chart usage
- [ ] Add troubleshooting guide
- [ ] Include monitoring setup instructions

## Dockerfile Implementation

### Frontend Dockerfile
```dockerfile
# Multi-stage build for frontend
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the Next.js application
RUN npm run build

# Production stage
FROM node:18-alpine AS runner

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Set working directory
WORKDIR /app

# Copy built application from builder stage
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./ 
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# Start the application
CMD ["node", "server.js"]
```

### Backend Dockerfile
```dockerfile
# Multi-stage build for backend
FROM python:3.13-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml uv.lock ./

# Sync dependencies to a virtual environment
RUN uv sync --locked --no-dev --no-install-workspace

# Production stage
FROM python:3.13-slim AS runtime

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup appuser

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv

# Copy source code
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Activate virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8000/health || exit 1

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Kubernetes Manifest Examples

### Frontend Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: todo-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: todo-frontend:latest
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_BASE_URL
          value: "http://backend.todo-app.svc.cluster.local:8000/api/v1"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Testing Plan

### Local Testing Commands

1. **Build Docker images:**
```bash
cd frontend && docker build -t todo-frontend .
cd backend && docker build -t todo-backend .
```

2. **Start Minikube:**
```bash
minikube start --cpus=4 --memory=8192 --disk-size=40g
minikube addons enable ingress
minikube addons enable metrics-server
```

3. **Deploy with Helm:**
```bash
helm install todo-app k8s/helm/ --values k8s/helm/values.yaml
```

4. **Test application:**
```bash
minikube service frontend --url
```

### Expected Behaviors

| Action | Expected Result |
|--------|----------------|
| Helm install | All resources created successfully |
| Application access | Frontend and backend accessible |
| Health checks | All pods passing health checks |
| Scaling | Pods scaling up/down correctly |
| Ingress routing | Proper routing to frontend/backend |

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Resource constraints | Configure appropriate resource limits |
| Security vulnerabilities | Scan images and implement security best practices |
| Networking issues | Test ingress and service connectivity |
| Data persistence | Verify PostgreSQL storage configuration |
| Monitoring gaps | Implement comprehensive observability stack |

## Success Criteria

- Successful deployment to Minikube
- All services accessible and functional
- Proper resource allocation and scaling
- Security best practices implemented
- Monitoring and logging operational
- Documentation is complete and accurate
- Application performs as expected in Kubernetes environment