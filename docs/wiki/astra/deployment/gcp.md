---
title: GCP Deployment
tags:
  - astra
  - deployment
  - gcp
---

# GCP deployment

Production on **GCP** typically uses **GKE** plus **managed** Postgres, Redis, and related services. **Helm values**, **scripts**, and **environment templates** live **only in the Astra repo**.

## Entry point

| Item | Detail |
|------|--------|
| **Script** | `scripts/gcp-deploy.sh` (not `scripts/deploy.sh`, which is local-only) |
| **Config** | Optional `.env.gcp`; template at `scripts/.env.gcp.example` |
| **Env vars** | `GCP_PROJECT`, `GCP_REGION`, `GCP_CLUSTER`, `POSTGRES_PASSWORD`, optional `GCS_WORKSPACE_BUCKET` |

## Flags

| Flag | Purpose |
|------|---------|
| `--setup` | First-time provision (creates all GCP resources) |
| `--dev` / `--prod` | Tier selection (`values-gke-dev.yaml` vs `values-gke-prod.yaml`) |
| `--build-only` | Build container images only |
| `--deploy-only` | Migrate + Helm deploy without rebuilding images |

## Provisioned resources

| Resource | Service |
|----------|---------|
| **GKE Autopilot** | Kubernetes cluster |
| **Cloud SQL** | PostgreSQL 15 (primary) |
| **Memorystore** | Redis |
| **Memorystore** | Memcached |
| **Artifact Registry** | Container image storage |
| **Cloud Storage** | `gs://${GCP_PROJECT}-astra-workspace` (override via `GCS_WORKSPACE_BUCKET`) |

## Object storage policy

On the GCP deploy path, workspace/artifact storage is **GCS**. MinIO is for local/docker-compose only — do not rely on MinIO in production GCP.

## Application deploy

Per-service `helm upgrade --install astra-<service>` using chart `deployments/helm/astra` with `--set service.name=<service>` and images from Artifact Registry.

## Themes

- **Private networking** between workloads and data stores.
- **Secrets** via **Vault** or cloud secret managers — not in git.
- **Scaling** per **PRD §20**.

See also [Kubernetes / Helm](kubernetes.md) for namespace layout at a high level.
