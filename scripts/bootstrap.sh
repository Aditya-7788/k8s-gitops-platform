#!/usr/bin/env bash
set -euo pipefail

cluster_name="${KIND_CLUSTER_NAME:-gitops}"
if ! kind get clusters | grep -Fxq "${cluster_name}"; then
  kind create cluster --name "${cluster_name}" --config kind/kind-config.yaml
fi

kubectl cluster-info --context "kind-${cluster_name}"
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.3/deploy/static/provider/kind/deploy.yaml
kubectl wait --namespace ingress-nginx \
  --for=condition=Ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=180s

kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.7.2/components.yaml
if ! kubectl get deployment metrics-server --namespace kube-system \
  -o jsonpath='{.spec.template.spec.containers[0].args}' | grep -Fq -- '--kubelet-insecure-tls'; then
  kubectl patch deployment metrics-server --namespace kube-system --type=json \
    --patch='[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
fi
kubectl wait --namespace kube-system \
  --for=condition=Available deployment/metrics-server \
  --timeout=180s

helm repo add argo https://argoproj.github.io/argo-helm --force-update
helm repo update argo
helm upgrade --install argocd argo/argo-cd --version 10.18.3 \
  --namespace argocd --create-namespace \
  --set server.service.type=ClusterIP \
  --wait --timeout 5m

kubectl apply -f https://raw.githubusercontent.com/Aditya-7788/k8s-gitops-config/main/apps/root.yaml
