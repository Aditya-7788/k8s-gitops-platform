# Three-minute demo

| Time | Walkthrough |
| --- | --- |
| 0:00–0:30 | Show the three repositories and the app-of-apps tree in Argo CD. Explain that Git is the desired-state source. |
| 0:30–1:00 | Push a change to the staging image tag or chart values in `k8s-gitops-config`; show Argo CD detecting and syncing the commit. |
| 1:00–1:45 | Watch the frontend, API, and worker Deployments roll out with `kubectl -n staging get pods -w`. Open the site and create a task. |
| 1:45–2:30 | Open Grafana's **Per-Service Health** dashboard. Show request rate, errors, resource use, and restarts; optionally run `scripts/load-test.sh` to exercise HPA metrics. |
| 2:30–3:00 | Show staging and production Application health, summarize the manual Slack Secret boundary, and note that task storage is in-memory for demo purposes. |

Recording link: `https://example.com/replace-with-demo-video`
