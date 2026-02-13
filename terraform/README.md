# Terraform Infrastructure for Todo Application

This directory contains the Terraform configuration for deploying the Todo Application infrastructure on AWS.

## Overview

The Terraform configuration creates the following infrastructure:

- VPC with public and private subnets
- EKS cluster for Kubernetes orchestration
- RDS PostgreSQL database instance
- Application Load Balancer for traffic routing
- S3 bucket for backups
- Security groups and networking components
- IAM roles and policies

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) >= 1.0
- [AWS CLI](https://aws.amazon.com/cli/) configured with appropriate credentials
- [kubectl](https://kubernetes.io/docs/tasks/tools/) for interacting with the cluster
- [Helm](https://helm.sh/docs/intro/install/) for package management

## Setup

### 1. Initialize Terraform

```bash
# Run the setup script
chmod +x setup.sh
./setup.sh
```

Or initialize manually:

```bash
# Initialize Terraform
terraform init

# Validate configuration
terraform validate
```

### 2. Configure Variables

Create a `terraform.tfvars` file with your specific values:

```hcl
# AWS Region
aws_region = "us-west-2"

# Project Configuration
project_name = "todo-app"
environment = "dev"

# VPC Configuration
vpc_cidr = "10.0.0.0/16"
availability_zones = ["us-west-2a", "us-west-2b", "us-west-2c"]
private_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
public_subnet_cidrs = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]

# EKS Configuration
cluster_name = "todo-cluster"
kubernetes_version = "1.28"
desired_nodes = 2
max_nodes = 5
min_nodes = 1
instance_types = ["t3.medium"]

# Database Configuration
db_engine_version = "15.4"
db_name = "todo_app"
db_username = "postgres"
db_instance_class = "db.t3.small"
db_allocated_storage = 20
db_max_allocated_storage = 100
db_multi_az = false

# SSL Certificate ARN (optional, can be empty initially)
ssl_certificate_arn = ""

# EFS Configuration
enable_efs = false
```

### 3. Plan the Deployment

```bash
terraform plan
```

### 4. Apply the Configuration

```bash
terraform apply
```

## Infrastructure Components

### VPC
- Public and private subnets across multiple AZs
- NAT Gateway for private subnet internet access
- Internet Gateway for public subnet internet access

### EKS Cluster
- Managed Kubernetes cluster
- Auto-scaling node groups
- Kubernetes Dashboard enabled
- Metrics Server enabled

### RDS PostgreSQL
- PostgreSQL database instance
- Multi-AZ deployment option
- Automated backups and snapshots
- Encryption at rest

### Application Load Balancer
- HTTP/HTTPS load balancing
- Health checks for targets
- SSL termination
- Access logging to S3

### S3 Bucket
- Encrypted storage for backups
- Versioning enabled
- Lifecycle policies for cost optimization

## Accessing the Cluster

After deployment, you can access the cluster:

```bash
# Configure kubectl
aws eks update-kubeconfig --name todo-cluster --region us-west-2

# Verify cluster access
kubectl get nodes

# Access the Kubernetes dashboard
kubectl proxy
# Then visit: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https-kubernetes-dashboard:/proxy/
```

## Deploying the Application

After the infrastructure is created, deploy the application using Helm:

```bash
# Navigate to the Helm chart directory
cd ../k8s/helm

# Install the application
helm install todo-app . \
    --namespace todo-app \
    --create-namespace \
    --set global.betterAuthSecret="your-super-secret-jwt-token-with-at-least-32-characters-long" \
    --set global.openaiApiKey="your-openai-api-key-here" \
    --set postgresql.auth.existingSecret="todo-app-db-secret" \
    --wait \
    --timeout=10m
```

## Monitoring and Observability

The infrastructure includes:

- CloudWatch for AWS resource monitoring
- Kubernetes metrics via Metrics Server
- ALB access logs to S3
- Database performance insights

## Security

### Network Security
- Private subnets for application nodes
- Security groups with minimal required ports
- Network ACLs for subnet-level security
- VPC endpoints for AWS service access

### Data Security
- Encryption at rest for RDS and S3
- Encryption in transit for all communications
- Secrets management with AWS Secrets Manager
- IAM roles with least-privilege access

### Application Security
- Kubernetes RBAC configuration
- Pod Security Standards
- Network Policies for service isolation
- TLS for all external communications

## Scaling

### EKS Node Scaling
- Auto Scaling Groups for worker nodes
- Horizontal Pod Autoscaler for applications
- Cluster Autoscaler for node management

### Database Scaling
- Read replicas for read scaling
- Storage auto-scaling
- Multi-AZ for high availability

## Backup and Recovery

### Database Backup
- Automated daily backups
- Point-in-time recovery
- Cross-region backup copying

### Application Backup
- Configuration backup to S3
- Secrets backup to AWS Secrets Manager
- Disaster recovery procedures

## Cleanup

To remove all infrastructure:

```bash
# Remove application deployments first
helm uninstall todo-app -n todo-app

# Remove the infrastructure
terraform destroy
```

## Troubleshooting

### Common Issues

#### 1. Insufficient IAM Permissions
Ensure your AWS user has the necessary permissions for EKS, RDS, and VPC resources.

#### 2. Resource Limits
Check AWS service quotas for limits on resources like VPCs, subnets, and EKS clusters.

#### 3. Security Group Issues
Verify that security groups allow the necessary traffic between components.

### Useful Commands

```bash
# Check Terraform state
terraform show

# List resources managed by Terraform
terraform state list

# Get specific resource information
terraform state show <resource-address>

# Refresh state with actual infrastructure
terraform refresh

# Import existing resources
terraform import <resource-address> <resource-id>
```

## Development

### Local Development
For local development, consider using Minikube or Kind instead of the full AWS infrastructure.

### Module Development
The configuration uses Terraform modules for organization:
- `modules/vpc/` - VPC and networking components
- `modules/eks/` - EKS cluster components
- `modules/database/` - RDS components
- `modules/load_balancer/` - ALB components

### State Management
The configuration uses S3 backend for state management with DynamoDB for locking to ensure safe concurrent access.

## Cost Optimization

### Resource Sizing
- Right-size EKS worker nodes based on application needs
- Use Spot Instances for non-critical workloads
- Configure appropriate RDS instance classes

### Lifecycle Management
- Implement S3 lifecycle policies for log archival
- Use RDS storage auto-scaling to optimize costs
- Terminate unused resources in development environments

This Terraform configuration provides a production-ready infrastructure for the Todo Application with high availability, security, and scalability.