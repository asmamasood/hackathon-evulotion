# Main Terraform configuration for Todo Application Infrastructure

# VPC Configuration
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "${var.project_name}-vpc"
  cidr = var.vpc_cidr

  azs             = var.availability_zones
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway = true
  single_nat_gateway = true
  enable_vpn_gateway = false

  public_subnet_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                    = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"           = "1"
  }
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = var.cluster_name
  cluster_version = var.kubernetes_version

  vpc_id     = module.vpc.vpc_id
  subnet_ids = concat(module.vpc.private_subnets, module.vpc.public_subnets)

  # EKS Node Group
  node_groups = {
    main = {
      desired_capacity = var.desired_nodes
      max_capacity     = var.max_nodes
      min_capacity     = var.min_nodes

      instance_types = var.instance_types

      additional_tags = {
        Name = "${var.project_name}-node-group"
      }
    }
  }

  # Enable EKS add-ons
  enable_cluster_creator_admin_permissions = true

  tags = {
    Name = "${var.project_name}-cluster"
  }
}

# RDS PostgreSQL Instance
module "db" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 6.0"

  identifier = "${var.project_name}-db"

  engine            = "postgres"
  engine_version    = var.db_engine_version
  family            = "postgres15" # for parameter group
  major_engine_version = "15"      # for option group

  db_name  = var.db_name
  username = var.db_username
  port     = "5432"

  instance_class = var.db_instance_class

  allocated_storage     = var.db_allocated_storage
  max_allocated_storage = var.db_max_allocated_storage
  storage_encrypted     = true
  storage_type          = "gp3"

  db_parameter_group_name      = "default.postgres15"
  parameter_group_name         = "default.postgres15"
  apply_immediately            = true
  allow_major_version_upgrade  = false
  auto_minor_version_upgrade   = true
  backup_retention_period      = 7
  backup_window                = "03:00-04:00"
  create_db_option_group       = false
  create_db_parameter_group    = false
  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]
  maintenance_window           = "sun:04:00-sun:05:00"
  skip_final_snapshot          = false
  snapshot_identifier          = null
  vpc_security_group_ids       = [aws_security_group.rds.id]
  subnet_ids                   = module.vpc.private_subnets
  multi_az                     = var.db_multi_az
  publicly_accessible          = false

  tags = {
    Name = "${var.project_name}-db"
  }
}

# Security Group for RDS
resource "aws_security_group" "rds" {
  name_prefix = "${var.project_name}-rds-"
  description = "Security group for RDS PostgreSQL"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port = 5432
    to_port   = 5432
    protocol  = "tcp"
    # Allow access from EKS nodes
    security_groups = [module.eks.node_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-rds-sg"
  }
}

# EFS for shared storage (optional)
resource "aws_efs_file_system" "app" {
  count = var.enable_efs ? 1 : 0

  creation_token = "${var.project_name}-efs"

  performance_mode       = "generalPurpose"
  throughput_mode        = "provisioned"
  provisioned_throughput_in_mibps = 10

  encrypted = true

  tags = {
    Name = "${var.project_name}-efs"
  }
}

# ALB for ingress
module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 9.0"

  name = var.project_name

  vpc_id          = module.vpc.vpc_id
  subnets         = module.vpc.public_subnets
  security_groups = [aws_security_group.alb.id]

  # HTTP listeners
  http_tcp_listeners = [
    {
      port     = 80
      protocol = "HTTP"

      forward = {
        target_group_key = "frontend"
      }
    }
  ]

  # HTTPS listeners
  https_listeners = [
    {
      port     = 443
      protocol = "HTTPS"
      certificate_arn = var.ssl_certificate_arn

      forward = {
        target_group_key = "frontend"
      }
    }
  ]

  # Target groups
  target_groups = [
    {
      key             = "frontend"
      backend_protocol = "HTTP"
      backend_port    = 3000

      health_check = {
        enabled             = true
        healthy_threshold   = 2
        unhealthy_threshold = 2
        timeout             = 5
        interval            = 30
        path                = "/"
        matcher             = "200"
      }

      target_type = "ip"
    },
    {
      key             = "backend"
      backend_protocol = "HTTP"
      backend_port    = 8000

      health_check = {
        enabled             = true
        healthy_threshold   = 2
        unhealthy_threshold = 2
        timeout             = 5
        interval            = 30
        path                = "/health"
        matcher             = "200"
      }

      target_type = "ip"
    }
  ]

  tags = {
    Name = "${var.project_name}-alb"
  }
}

# Security Group for ALB
resource "aws_security_group" "alb" {
  name_prefix = "${var.project_name}-alb-"
  description = "Security group for ALB"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-alb-sg"
  }
}

# S3 Bucket for backups
resource "aws_s3_bucket" "backups" {
  bucket = "${var.project_name}-${var.environment}-backups"

  tags = {
    Name = "${var.project_name}-backups"
  }
}

resource "aws_s3_bucket_versioning" "backups" {
  bucket = aws_s3_bucket.backups.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "backups" {
  bucket = aws_s3_bucket.backups.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}