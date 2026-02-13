#!/bin/bash

# Terraform setup script for Todo Application

set -e  # Exit immediately if a command exits with a non-zero status

echo "Setting up Terraform for Todo Application..."

# Check if terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "Terraform is not installed. Please install Terraform first."
    echo "Follow instructions at: https://learn.hashicorp.com/tutorials/terraform/install-cli"
    exit 1
fi

# Check if AWS CLI is installed and configured
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Please install AWS CLI first."
    echo "Follow instructions at: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

# Verify AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo "AWS credentials not configured. Please run 'aws configure' first."
    exit 1
fi

# Initialize Terraform
echo "Initializing Terraform..."
terraform init

# Validate configuration
echo "Validating Terraform configuration..."
terraform validate

# Create/Update terraform.tfvars if it doesn't exist
if [ ! -f "terraform.tfvars" ]; then
    echo "Creating terraform.tfvars file..."
    cat > terraform.tfvars << EOF
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
EOF
    echo "Created terraform.tfvars with default values. Please update with your specific values."
fi

echo "Terraform setup completed successfully!"
echo "To deploy the infrastructure, run: terraform plan and then terraform apply"