---
title: GCP Deployment
tags:
  - astra
  - deployment
  - gcp
  - kubernetes
---

# GCP Deployment

Astra on GCP uses managed services for all infrastructure. No self-managed Postgres, Redis, or Memcached in production GCP.

## Script

Run `./scripts/gcp-deploy.sh` with the appropriate flags. **Not** `scripts/deploy.sh` — that's local only.

## Configuration

Copy `scripts/.env.gcp.example` to `.env.gcp`. The required variables are:

- `GCP_PROJECT` — your GCP project ID
- `GCP_REGION` — deployment region (e.g. `us-central1`)
- `GCP_CLUSTER` — GKE cluster name
- `POSTGRES_PASSWORD` — strong password for Cloud SQL
- `GCS_WORKSPACE_BUCKET` — GCS bucket name (optional; defaults to `${GCP_PROJECT}-astra-workspace`)

See `.env.gcp.example` in the Astra repo.

## Flags

| Flag | Effect |
|---|---|
| `--setup` | First-time provision: creates GKE, Cloud SQL, Memorystore, Artifact Registry, GCS bucket |
| `--dev` | Deploy with `values-gke-dev.yaml` (lower resource limits) |
| `--prod` | Deploy with `values-gke-prod.yaml` (production sizing) |
| `--build-only` | Build and push Docker images only, no deploy |
| `--deploy-only` | Run migrations + Helm without rebuilding images |

## Provisioned resources

| Resource | Service |
|---|---|
| Kubernetes | GKE Autopilot |
| Postgres | Cloud SQL (PostgreSQL 15), HA instance |
| Redis | Memorystore for Redis |
| Memcached | Memorystore for Memcached |
| Container registry | Artifact Registry |
| Object storage | GCS bucket (`gs://${GCP_PROJECT}-astra-workspace`) |

**Object storage policy:** On GCP, workspace and artifact storage is GCS. MinIO is for local/docker-compose only. Do not reference MinIO in production GCP configs.

## Helm deployment

Each service is deployed individually via `helm upgrade --install`, specifying the service name, Artifact Registry image path, and git SHA image tag. The full chart configuration is in `deployments/helm/astra/values.yaml`. See `deployments/helm/astra/` in the Astra repo.

## Documentation

- `README.md` — GCP section
- `deployments/helm/astra/README.md` — Helm chart reference
- `docs/deployment-design.md` — deployment design decisions (Astra repo)
