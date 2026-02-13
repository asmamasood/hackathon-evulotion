# Phase IV - Cloud-Native Kubernetes Deployment

> Last Updated: 2026-02-13
> Phase: IV
> Status: Implementation in Progress

## Overview

Phase IV transforms the Phase III application into a cloud-native, containerized solution deployed on Kubernetes. This phase implements infrastructure as code with Terraform, containerization with Docker, and deployment automation with Helm and CI/CD pipelines.

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        AWS EKS Cluster                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │                        todo-app Namespace                               │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │  │
│  │  │   Frontend  │  │   Backend   │  │ PostgreSQL  │  │   Kafka     │  │  │
│  │  │   (Next.js) │  │  (FastAPI)  │  │ (Stateful) │  │  (Cluster)  │  │  │
│  │  │             │  │             │  │            │  │             │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │  │
│  │         │               │                 │               │          │  │
│  │         ▼               ▼                 ▼               ▼          │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │  │
│  │  │ Frontend    │  │ Backend     │  │ PVC for     │  │ Kafka       │  │  │
│  │  │ Service     │  │ Service     │  │ Persistent  │  │ Topics      │  │  │
│  │  │             │  │             │  │ Storage     │  │             │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │  │
│  │         │               │                 │               │          │  │
│  │         ▼               ▼                 ▼               ▼          │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │                    Application Load Balancer                  │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                        Monitoring & Security                          │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │ │ │
│  │  │ Prometheus  │  │   Grafana   │  │  Jaeger     │  │  ELK Stack  │ │ │ │
│  │  │             │  │             │  │             │  │             │ │ │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │ │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Tech Stack
- **Infrastructure**: AWS EKS, Terraform
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Kubernetes with Helm
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLModel, PostgreSQL
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus, Grafana, ELK Stack

## Features

### Infrastructure as Code
- Complete Terraform configuration for AWS infrastructure
- EKS cluster with auto-scaling node groups
- RDS PostgreSQL with read replicas
- Application Load Balancer configuration
- Security groups and network policies
- S3 for backup storage

### Containerization
- Multi-stage Docker builds for optimized images
- Security scanning with Trivy
- Non-root user execution
- Environment-based configuration

### Kubernetes Deployment
- Helm charts for parameterized deployments
- Namespaced deployments for isolation
- Service discovery and load balancing
- Persistent volume claims for data
- ConfigMaps and Secrets management
- Health checks and readiness probes

### Monitoring & Observability
- Prometheus for metrics collection
- Grafana for dashboard visualization
- ELK Stack for logging
- Jaeger for distributed tracing
- Health checks and alerts

### CI/CD Pipeline
- Automated Docker image building
- Security scanning integration
- Automated testing
- Blue-green deployment strategy
- Automated rollback capabilities

## Project Structure

```
hackathon-todo/
├── specs/
│   └── phases/
│       ├── phase1.md
│       ├── phase2.md
│       ├── phase3.md
│       └── phase4.md
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── models/
│   ├── api/
│   ├── core/
│   ├── database/
│   └── CLAUDE.md
├── frontend/
│   ├── Dockerfile
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── CLAUDE.md
├── k8s/
│   ├── manifests/
│   │   ├── namespace.yaml
│   │   ├── postgresql/
│   │   ├── frontend/
│   │   ├── backend/
│   │   ├── kafka/
│   │   └── ingress.yaml
│   ├── helm/
│   │   ├── Chart.yaml
│   │   ├── values.yaml
│   │   ├── templates/
│   │   │   ├── frontend/
│   │   │   ├── backend/
│   │   │   ├── database/
│   │   │   ├── kafka/
│   │   │   └── ingress/
│   │   └── files/
│   └── scripts/
│       ├── deploy.sh
│       └── setup.sh
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── providers.tf
│   ├── backend.tf
│   └── modules/
│       ├── vpc/
│       ├── eks/
│       ├── rds/
│       └── alb/
├── cicd/
│   └── github-actions/
│       ├── deploy.yml
│       ├── test.yml
│       └── security-scan.yml
├── CLAUDE.md
└── README.md
```

## Getting Started

### Prerequisites

- [AWS CLI](https://aws.amazon.com/cli/) configured with appropriate permissions
- [Terraform](https://www.terraform.io/downloads.html) >= 1.0
- [kubectl](https://kubernetes.io/docs/tasks/tools/) for cluster interaction
- [Helm](https://helm.sh/docs/intro/install/) for package management
- [Docker](https://www.docker.com/products/docker-desktop/) for containerization
- [GitHub CLI](https://cli.github.com/) for repository management

### Setup Instructions

#### 1. Infrastructure Setup

```bash
# Navigate to terraform directory
cd terraform

# Initialize Terraform
terraform init

# Review the execution plan
terraform plan -var="aws_region=us-west-2" -var="project_name=todo-app" -var="environment=dev"

# Apply the infrastructure
terraform apply -var="aws_region=us-west-2" -var="project_name=todo-app" -var="environment=dev"
```

#### 2. Configure kubectl

```bash
# Configure kubectl to connect to the EKS cluster
aws eks update-kubeconfig --name todo-cluster --region us-west-2

# Verify cluster connectivity
kubectl cluster-info
kubectl get nodes
```

#### 3. Build and Push Docker Images

```bash
# Build frontend image
cd frontend
docker build -t <your-registry>/todo-frontend:latest .
docker push <your-registry>/todo-frontend:latest

# Build backend image
cd ../backend
docker build -t <your-registry>/todo-backend:latest .
docker push <your-registry>/todo-backend:latest
```

#### 4. Deploy Application with Helm

```bash
# Navigate to Helm chart directory
cd ../k8s/helm

# Install the application
helm install todo-app . \
    --namespace todo-app \
    --create-namespace \
    --set frontend.image.repository=<your-registry>/todo-frontend \
    --set frontend.image.tag=latest \
    --set backend.image.repository=<your-registry>/todo-backend \
    --set backend.image.tag=latest \
    --set global.betterAuthSecret="your-super-secret-jwt-token-with-at-least-32-characters-long" \
    --set global.openaiApiKey="your-openai-api-key-here" \
    --set postgresql.auth.postgresPassword="your-postgres-password" \
    --wait \
    --timeout=10m
```

#### 5. Access the Application

```bash
# Get the load balancer URL
kubectl get ingress -n todo-app

# Or access via service
kubectl get service todo-app-frontend -n todo-app
```

## Configuration

### Environment Variables

#### Backend
- `DATABASE_URL` - PostgreSQL connection string
- `BETTER_AUTH_SECRET` - JWT secret for authentication
- `OPENAI_API_KEY` - API key for OpenAI integration
- `DEBUG` - Debug mode flag

#### Frontend
- `NEXT_PUBLIC_API_BASE_URL` - Backend API base URL
- `NEXT_PUBLIC_APP_ENV` - Application environment

### Helm Values

Customize the deployment using the `values.yaml` file or override values during installation:

```bash
helm upgrade todo-app . \
    --namespace todo-app \
    --reuse-values \
    --set frontend.replicaCount=3 \
    --set backend.replicaCount=2 \
    --set postgresql.primary.resources.requests.memory="512Mi" \
    --set postgresql.primary.resources.requests.cpu="500m"
```

## Security

### Infrastructure Security
- VPC with private subnets for nodes
- Security groups with minimal required ports
- IAM roles with least privilege access
- Secrets management with AWS Secrets Manager
- Network ACLs for subnet-level security

### Application Security
- TLS/SSL for all communications
- JWT validation on every request
- User data isolation enforcement
- Input validation and sanitization
- Secure credential management

### Container Security
- Non-root user execution
- Minimal attack surface with Alpine base images
- Regular security scanning with Trivy
- Image signing and verification

## Monitoring & Observability

### Metrics Collection
- Prometheus for application and infrastructure metrics
- Custom business metrics
- Resource utilization tracking
- Performance benchmarks

### Logging
- Structured logging with correlation IDs
- Centralized log aggregation with ELK Stack
- Log retention policies
- Search and analysis capabilities

### Tracing
- Distributed tracing with Jaeger
- Request flow visualization
- Performance bottleneck identification
- Cross-service correlation

## Scaling

### Horizontal Scaling
- Horizontal Pod Autoscaler for application pods
- Cluster Autoscaler for node management
- Database connection pooling
- CDN for static assets

### Vertical Scaling
- Resource requests and limits configuration
- Quality of Service (QoS) classes
- Priority classes for critical workloads

## Backup & Recovery

### Database Backup
- Automated RDS snapshots
- Point-in-time recovery
- Cross-region backup copying
- Backup encryption

### Application Backup
- Configuration backup to S3
- Secrets backup to AWS Secrets Manager
- Disaster recovery procedures
- Backup validation

## CI/CD Pipeline

### Workflow Stages

1. **Source**: Code changes trigger pipeline
2. **Build**: Docker images built and scanned
3. **Test**: Automated testing and security scanning
4. **Deploy**: Blue-green deployment to EKS
5. **Validate**: Health checks and metrics validation
6. **Monitor**: Post-deployment monitoring

### Automation Features
- Automated testing on every commit
- Security scanning integrated
- Performance testing before production
- Automated rollback on failure
- Notification and alerting

## Troubleshooting

### Common Issues

#### 1. Insufficient IAM Permissions
```bash
# Verify AWS credentials
aws sts get-caller-identity

# Check required permissions
aws iam get-user
```

#### 2. Resource Limits
```bash
# Check resource quotas
aws service-quotas list-service-quotas --service-code eks

# Check current usage
kubectl describe nodes
```

#### 3. Networking Issues
```bash
# Check security groups
kubectl get svc -o wide

# Check ingress status
kubectl get ingress
```

### Debugging Commands

```bash
# Check pod status
kubectl get pods -n todo-app

# View pod logs
kubectl logs -l app=frontend -n todo-app
kubectl logs -l app=backend -n todo-app
kubectl logs -l app=postgresql -n todo-app

# Describe pod for detailed information
kubectl describe pod <pod-name> -n todo-app

# Port forward to access services locally
kubectl port-forward svc/frontend 3000:80 -n todo-app
kubectl port-forward svc/backend 8000:8000 -n todo-app
```

## Performance Tuning

### Resource Optimization
```bash
# Adjust resource requests and limits
helm upgrade todo-app . \
    --namespace todo-app \
    --set frontend.resources.requests.memory="256Mi" \
    --set frontend.resources.requests.cpu="200m" \
    --set frontend.resources.limits.memory="512Mi" \
    --set frontend.resources.limits.cpu="500m" \
    --set backend.resources.requests.memory="512Mi" \
    --set backend.resources.requests.cpu="500m" \
    --set backend.resources.limits.memory="1Gi" \
    --set backend.resources.limits.cpu="1000m"
```

### Database Connection Pooling
```bash
# Configure connection pooling in backend
helm upgrade todo-app . \
    --namespace todo-app \
    --set backend.env.DATABASE_CONNECTION_POOL_SIZE=20 \
    --set backend.env.DATABASE_MAX_OVERFLOW=30
```

## Development Workflow

### Local Development with Kubernetes
```bash
# Use Telepresence for intercepting traffic to local machine
telepresence intercept todo-app-backend --port 8000

# Develop locally while using Kubernetes services
uvicorn main:app --reload --port 8000
```

### Updating Images
```bash
# Rebuild and push new image
docker build -t <registry>/todo-backend:v1.0.1 .
docker push <registry>/todo-backend:v1.0.1

# Update deployment with new image
kubectl set image deployment/backend backend=<registry>/todo-backend:v1.0.1 -n todo-app
```

## Future Considerations

### Phase V Migration Path
- Integration with AWS Lambda for serverless functions
- Advanced analytics with AWS Kinesis
- Machine learning model deployment with SageMaker
- Advanced security with AWS GuardDuty
- Cost optimization with AWS Cost Explorer

### Design Decisions for Phase IV
- EKS chosen for managed Kubernetes
- RDS chosen for managed PostgreSQL
- Terraform for infrastructure as code
- Helm for application packaging
- GitHub Actions for CI/CD
- Blue-green deployment for zero-downtime updates

## Success Metrics

- Successful deployment to EKS with all services operational
- All security best practices implemented
- Performance benchmarks met
- Monitoring and alerting operational
- Documentation is complete and accurate
- CI/CD pipeline operational with automated deployments
- Application scales appropriately under load
- Backup and recovery procedures validated