---
title: Deployment
tags:
  - astra
  - deployment
  - infrastructure
---

# Deployment

Astra supports four deployment targets. All use the same codebase; backend selection (Metal, CUDA, CPU) is explicit via environment config.

## Environments

| Environment | Typical target | Secrets |
|-------------|----------------|---------|
| **Local dev** | Docker Compose + native services | `.env` / local only — not for prod secrets |
| **Staging** | Smaller k8s or single node | Vault or sealed secrets |
| **Production** | GKE / EKS / bare metal + managed data | **Vault** at runtime (PRD §18) |

## Targets

| Page | Target |
|---|---|
| [Local (docker-compose)](local.md) | Development — infra in Docker, services native |
| [Kubernetes / Helm](kubernetes.md) | Cloud production — Helm, namespaces, mTLS |
| [GCP Managed Services](gcp.md) | GCP production — Cloud SQL, Memorystore, GCS |
| [macOS Production](macos.md) | Mac Mini / Mac Studio production deployments |

## Kubernetes namespaces

| Namespace | Services |
|---|---|
| `control-plane` | `api-gateway`, `identity`, `access-control` |
| `kernel` | `scheduler-service`, `task-service`, `agent-service`, `goal-service`, `planner-service`, `memory-service` |
| `workers` | `execution-worker`, `browser-worker`, `tool-runtime`, `worker-manager`, `llm-router`, `prompt-manager`, `evaluation-service` |
| `infrastructure` | Postgres, Redis, Memcached, MinIO (local) |
| `observability` | Prometheus, Grafana, OpenTelemetry collector, Loki |

## Scaling model

| Component | Strategy |
|---|---|
| Stateless services | HPA based on CPU / request rate |
| Workers | HPA based on Redis queue depth + scheduler hints |
| Redis | Cluster mode, shard count based on throughput |
| Postgres | Primary for writes, read replicas for heavy reads |
| Memcached | Memory-optimised nodes, horizontal scaling |
