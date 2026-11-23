variable "aws_region" {
  description = "AWS region containing the EKS cluster."
  type        = string
  default     = "us-east-1"
}

variable "cluster_name" {
  description = "Name shared by the EKS cluster and VPC."
  type        = string
  default     = "task-manager-gitops"
}

variable "kubernetes_version" {
  description = "Supported EKS Kubernetes control-plane version."
  type        = string
  default     = "1.33"
}

variable "vpc_cidr" {
  description = "IPv4 CIDR for the EKS VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "node_instance_types" {
  description = "EC2 instance types for the managed worker group."
  type        = list(string)
  default     = ["t3.small"]
}

variable "environment" {
  description = "Environment label applied to AWS resources."
  type        = string
  default     = "capstone"
}
