#!/usr/bin/env bash
set -euo pipefail

cluster_name="${KIND_CLUSTER_NAME:-gitops}"
image_tag="${IMAGE_TAG:-v1.0.0}"
services=(frontend api worker)

for service in "${services[@]}"; do
  image="${service}:${image_tag}"
  docker build --pull -t "${image}" "services/${service}"
  kind load docker-image "${image}" --name "${cluster_name}"
done
