# Monitoring runbook

## Access

The `kube-prometheus-stack` Application installs Prometheus, Grafana, Alertmanager, and node-exporter with constrained requests and limits. Grafana dashboards are provisioned from ConfigMaps labeled `grafana_dashboard: "1"`. API and worker ServiceMonitors use the `prometheus` release label. Frontend has health probes but no metrics endpoint.

Find pod status and recent events:

```bash
kubectl get pods -A
kubectl get events -A --sort-by=.lastTimestamp
kubectl -n staging get servicemonitor,prometheusrule
```

Port-forward Grafana locally:

```bash
kubectl -n monitoring port-forward svc/kube-prometheus-stack-grafana 3000:80
```

Retrieve the generated Grafana admin password from the `kube-prometheus-stack-grafana` Secret in the `monitoring` namespace. The chart dashboard names are **Cluster Overview** and **Per-Service Health**.

## Triage

1. Check Argo CD application health and sync status, then `kubectl describe` the unhealthy workload.
2. Check pod logs and events; confirm readiness `/health`, image tag, and available node memory.
3. Use Prometheus alerts for restarts, CPU, request error ratio, and not-ready pods. The API's error counter is exported as `errors_total`; HTTP request counters are labeled `method`, `path`, and `status`.
4. Run `bash scripts/load-test.sh` to exercise `/api/load`. Kind bootstrap installs metrics-server with the kubelet TLS verification bypass required by a local kind cluster; use this only for the local demo. HPA needs sustained CPU usage and metrics collection, so allow time for metrics and scaling to settle.

The Task Manager stores tasks in each API process's memory, so a reschedule or request to another replica may show a different list. This is expected for this demo.

## Slack receiver secret

Create the `alertmanager-slack` Secret in `monitoring` with key `slack_webhook_url` before expecting Slack notifications. Use the exact manual command in the GitOps config README. Never commit the real webhook URL.
