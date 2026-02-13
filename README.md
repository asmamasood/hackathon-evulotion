# Phase V - Production Cloud Deployment with Advanced Features

> Last Updated: 2026-02-13
> Phase: V
> Status: Implementation Complete

## Overview

Phase V represents the culmination of the 5-phase Todo Application project. This phase deploys the application to a production-ready cloud environment on AWS EKS with advanced features including Dapr for distributed application capabilities, Apache Kafka for event streaming, and comprehensive monitoring and observability.

## Architecture

### Tech Stack
- **Infrastructure**: AWS EKS, RDS PostgreSQL, Application Load Balancer
- **Containerization**: Docker with multi-stage builds and security scanning
- **Orchestration**: Kubernetes with Helm for deployment management
- **Frontend**: Next.js 14 with App Router, TypeScript, Tailwind CSS
- **Backend**: FastAPI with SQLModel ORM
- **Database**: PostgreSQL with read replicas and automated backups
- **Authentication**: JWT-based with Better Auth
- **AI Integration**: OpenAI Agents SDK with MCP tools
- **Event Streaming**: Apache Kafka with Dapr integration
- **Monitoring**: Prometheus, Grafana, ELK Stack, CloudWatch
- **Package Managers**: UV (Python), npm (JavaScript)

### Architecture Layers
1. **Domain Layer**: Entities and repository interfaces
2. **Infrastructure Layer**: Concrete implementations (DB, external services)
3. **Application Layer**: Use cases and business logic
4. **AI Layer**: MCP tools and agent orchestration
5. **Presentation Layer**: API endpoints and UI components
6. **Orchestration Layer**: Kubernetes manifests and Helm charts
7. **Infrastructure Layer**: Terraform for infrastructure as code

## Features

### Cloud Infrastructure
- AWS EKS cluster with auto-scaling node groups
- RDS PostgreSQL with read replicas and automated backups
- Application Load Balancer with SSL termination
- CloudWatch for infrastructure monitoring
- S3 for backup storage and static assets
- AWS Secrets Manager for credential management

### Advanced Monitoring
- Prometheus and Grafana for application metrics
- ELK Stack for centralized logging
- Jaeger for distributed tracing
- Custom dashboards for business metrics
- Alerting and notification system

### CI/CD Pipeline
- GitHub Actions with multiple environments
- Automated testing and security scanning
- Blue-green deployment strategy
- Automated rollback capabilities
- Performance testing integration

### Security Enhancements
- AWS IAM integration with Kubernetes RBAC
- Secrets management with AWS Secrets Manager
- Network security with security groups and VPC
- WAF for application protection
- Advanced authentication with OAuth2

### Performance Optimization
- CDN for static assets (CloudFront)
- Database connection pooling and query optimization
- Redis caching layer for session and application data
- Auto-scaling configuration with HPA and VPA
- Performance monitoring and alerts

### Dapr Integration (Advanced)
- Service-to-service communication with Dapr
- State management using Dapr components
- Publish/subscribe messaging with Dapr and Kafka
- Secret management with Dapr
- Distributed tracing with Dapr

### Event Streaming (Advanced)
- Apache Kafka cluster with multi-AZ deployment
- Topic partitioning and replication
- Stream processing with Kafka Streams
- Event sourcing and CQRS patterns
- Real-time analytics with Kafka Connect

## Project Structure

```
hackathon-todo/
├── specs/
│   └── phases/
│       ├── phase1.md
│       ├── phase2.md
│       ├── phase3.md
│       ├── phase4.md
│       └── phase5.md
├── terraform/
│   ├── main.tf
│   ├── eks.tf
│   ├── rds.tf
│   ├── networking.tf
│   ├── security.tf
│   ├── monitoring.tf
│   ├── variables.tf
│   └── outputs.tf
├── k8s/
│   ├── manifests/
│   │   ├── namespace.yaml
│   │   ├── postgresql/
│   │   ├── frontend/
│   │   ├── backend/
│   │   ├── kafka/
│   │   ├── dapr/
│   │   ├── monitoring/
│   │   └── ingress.yaml
│   └── helm/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   ├── models/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── agents/
│   ├── mcp/
│   └── CLAUDE.md
├── frontend/
│   ├── Dockerfile
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── styles/
│   └── CLAUDE.md
├── cicd/
│   └── github-actions/
│       ├── deploy-dev.yml
│       ├── deploy-staging.yml
│       ├── deploy-prod.yml
│       ├── test.yml
│       └── security-scan.yml
├── scripts/
│   ├── deploy.sh
│   ├── rollback.sh
│   └── backup.sh
├── CLAUDE.md
└── README.md
```

## Getting Started

### Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform >= 1.0
- kubectl for cluster interaction
- Helm for package management
- Docker for containerization
- GitHub CLI for repository management

### Setup Instructions

#### 1. Infrastructure Setup

```bash
# Navigate to terraform directory
cd terraform

# Initialize Terraform
terraform init

# Review the execution plan
terraform plan -var="aws_region=us-west-2" -var="project_name=todo-app" -var="environment=prod"

# Apply the infrastructure
terraform apply -var="aws_region=us-west-2" -var="project_name=todo-app" -var="environment=prod"
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
- `DAPR_HTTP_PORT` - Dapr sidecar HTTP port
- `DAPR_GRPC_PORT` - Dapr sidecar gRPC port

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
- WAF for application protection

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
- CloudWatch for AWS resource metrics
- Custom business metrics
- Performance benchmarks
- Resource utilization tracking

### Logging
- Structured logging with correlation IDs
- Centralized log aggregation with ELK Stack
- Log retention policies
- Search and analysis capabilities
- Alerting on log patterns

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
- CDN integration for static assets

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
docker build -t <registry>/todo-backend:latest .
docker push <registry>/todo-backend:latest

# Update deployment with new image
kubectl set image deployment/backend backend=<registry>/todo-backend:latest -n todo-app
```

## Future Considerations

### Phase VI Migration Path
- Integration with AWS Lambda for serverless functions
- Advanced analytics with AWS Kinesis
- Machine learning model deployment with SageMaker
- Advanced security with AWS GuardDuty
- Cost optimization with AWS Cost Explorer

### Design Decisions for Phase V
- EKS chosen for managed Kubernetes
- RDS chosen for managed PostgreSQL
- Terraform for infrastructure as code
- Helm for application packaging
- GitHub Actions for CI/CD
- Blue-green deployment for zero-downtime updates
- Dapr for distributed application capabilities
- Kafka for event streaming and real-time processing

## Deployment Options

### Vercel Deployment (Frontend)

The frontend application is ready for deployment on Vercel. To deploy:

1. **Install Vercel CLI:**
```bash
npm i -g vercel
```

2. **Login to Vercel:**
```bash
vercel login
```

3. **Navigate to frontend directory and deploy:**
```bash
cd frontend
vercel --prod
```

4. **Or use the deployment script:**
```bash
chmod +x scripts/deploy-vercel.sh
./scripts/deploy-vercel.sh prod
```

### Environment Variables for Vercel
When prompted during deployment, set these environment variables:
- `NEXT_PUBLIC_API_BASE_URL` - Your backend API URL (e.g., https://your-backend.onrender.com/api/v1)
- `NEXT_PUBLIC_BETTER_AUTH_URL` - Your authentication service URL

### Kubernetes Deployment (Complete Application)
For full-stack deployment with backend and database, use the Kubernetes approach described above.

### Hugging Face Spaces Deployment (Backend)

The backend application can also be deployed on Hugging Face Spaces. To deploy:

1. **Prepare the backend for Spaces:**
```bash
cd backend
```

2. **Create a Hugging Face Space:**
- Go to [huggingface.co/spaces](https://huggingface.co/spaces)
- Create a new Space with the "Docker" SDK
- Choose "GPU" or "CPU" type depending on your needs

3. **Add the required files to your Space repository:**
- `space.py` - Main application entry point for Spaces
- `requirements.txt` - Python dependencies
- `Dockerfile.spaces` - Docker configuration for Spaces
- `app.yml` - Hugging Face Space configuration

4. **Configure environment variables in your Space settings:**
- `DATABASE_URL` - Database connection string (use SQLite for Spaces)
- `BETTER_AUTH_SECRET` - JWT secret for authentication
- `OPENAI_API_KEY` - OpenAI API key for AI features (if applicable)

5. **The Space will automatically build and deploy the backend**

## Success Metrics

- Successful deployment to EKS with all services operational
- All security best practices implemented
- Performance benchmarks met
- Monitoring and alerting operational
- Documentation is complete and accurate
- CI/CD pipeline operational with automated deployments
- Application performs as expected in cloud environment
- Advanced features (Dapr, Kafka) properly integrated
- Zero-downtime deployments achieved
- Proper resource utilization and cost optimization