# EKS Terraform

This code provisions a three-AZ VPC with public/private subnets, a single NAT gateway, a configurable EKS control plane (default 1.33), and an EC2 managed node group. It has not been applied.

```bash
terraform init
terraform fmt -check
terraform validate
terraform plan -out=tfplan
```

Review the plan, AWS account, region, and cost (including NAT gateway and EKS charges) before applying. State is local by default; configure a secured remote backend and state locking before team use. Restrict the public API endpoint to trusted CIDRs before production use. Configure kubectl with the `configure_kubectl` output. This module does not install Argo CD, ingress, or application images.
