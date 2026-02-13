output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = aws_eks_cluster.todo_cluster.endpoint
}

output "cluster_ca_certificate" {
  description = "Base64 encoded CA certificate for EKS cluster"
  value       = aws_eks_cluster.todo_cluster.certificate_authority[0].data
}

output "cluster_name" {
  description = "Kubernetes Cluster Name"
  value       = aws_eks_cluster.todo_cluster.name
}

output "cluster_arn" {
  description = "The Amazon Resource Name (ARN) of the EKS cluster"
  value       = aws_eks_cluster.todo_cluster.arn
}

output "node_instance_role_arn" {
  description = "The ARN of the IAM role assigned to the node instances"
  value       = aws_iam_role.node.arn
}

output "node_security_group_id" {
  description = "Security group ID for the node instances"
  value       = aws_eks_node_group.todo_nodes.resources[0].remote_access_sg_id
}

output "vpc_id" {
  description = "ID of the VPC where the cluster is deployed"
  value       = aws_vpc.todo_vpc.id
}

output "subnet_ids" {
  description = "IDs of the subnets where the cluster is deployed"
  value       = concat(aws_subnet.public_subnets[*].id, aws_subnet.private_subnets[*].id)
}