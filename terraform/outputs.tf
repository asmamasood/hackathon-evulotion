# Output values for the Todo Application infrastructure

output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "cluster_name" {
  description = "Name of the EKS cluster"
  value       = module.eks.cluster_name
}

output "cluster_security_group_id" {
  description = "Security group IDs attached to the cluster control plane"
  value       = module.eks.cluster_security_group_id
}

output "node_security_group_id" {
  description = "Security group ID for the node instances"
  value       = module.eks.node_security_group_id
}

output "cluster_certificates" {
  description = "Cluster CA certificate"
  value       = module.eks.cluster_certificate_authority_data
  sensitive   = true
}

output "db_endpoint" {
  description = "RDS instance endpoint"
  value       = module.db.db_instance_address
}

output "db_name" {
  description = "RDS instance name"
  value       = module.db.db_instance_identifier
}

output "db_username" {
  description = "RDS master username"
  value       = module.db.db_instance_username
  sensitive   = true
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "vpc_private_subnets" {
  description = "Private subnets in the VPC"
  value       = module.vpc.private_subnets
}

output "vpc_public_subnets" {
  description = "Public subnets in the VPC"
  value       = module.vpc.public_subnets
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = module.alb.lb_dns_name
}

output "alb_arn" {
  description = "ARN of the Application Load Balancer"
  value       = module.alb.lb_arn
}

output "alb_target_group_arns" {
  description = "ARNs of the ALB target groups"
  value       = module.alb.target_group_arns
}

output "s3_backup_bucket" {
  description = "Name of the S3 bucket for backups"
  value       = aws_s3_bucket.backups.bucket
}

output "kubernetes_config_map" {
  description = "Config map for Kubernetes cluster"
  value       = module.eks.kubeconfig
  sensitive   = true
}