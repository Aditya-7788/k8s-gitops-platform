# Deployment guide

## kind

Install Docker, kind, kubectl, and Helm on Ubuntu 24.04. From this repository root:

```bash
kind create cluster --name gitops --config kind/kind-config.yaml
bash scripts/build-and-load.sh
bash scripts/bootstrap.sh
echo '127.0.0.1 tasks.local' | sudo tee -a /etc/hosts
```

The build script loads `frontend:v1.0.0`, `api:v1.0.0`, and `worker:v1.0.0`. Bootstrap installs ingress-nginx and Argo CD, then applies the public GitOps root Application. If the config repo is private, configure a repository credential Secret in Argo CD before applying the root app. To rebuild after source changes, rerun `build-and-load.sh`, then update the desired tag in the GitOps config repo and push.

Local app-only development: `docker compose up --build`, then open `http://localhost:9080`. Stop with `docker compose down`.

## GitOps release

1. Commit and push a new image tag and matching Helm values in `k8s-gitops-config`.
2. Wait for the root and service Applications to report synced/healthy.
3. Watch rollout with `kubectl -n staging rollout status deployment/frontend` (repeat for `api` and `worker`).
4. Verify `http://tasks.local:9080/`, add a task, and inspect Grafana and Prometheus alerts.

## AWS

Read `terraform/README.md` and the Terraform plan before applying. Build/push images to a registry reachable by EKS and update GitOps image repositories first; kind-local image names are not available to EKS nodes. Configure Argo CD repository credentials and create the Slack Secret separately.
