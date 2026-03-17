---
title: Architecture Overview
tags:
  - astra
  - architecture
  - overview
---

# Architecture Overview

Astra is a production-grade, microkernel-style autonomous agent platform. The entire system is designed around one hard constraint: **no API call may take more than 10ms to respond**. All hot-path reads serve from cache (Redis or Memcached). Synchronous Postgres reads on the request path are a bug.

## Component diagram

The system is layered top-to-bottom. Applications use the Astra SDK (`pkg/sdk`), which calls into the Astra Kernel (microkernel). The kernel comprises five components: the Actor Runtime (`internal/actors`), Task Graph Engine (`internal/tasks`), Scheduler (`internal/scheduler`), Message Bus (`internal/messaging`), and State Manager (`internal/events`). Below the kernel sits Infrastructure: Postgres (primary + replicas, pgvector), Redis (streams, ephemeral state, locks), Memcached (LLM/embedding/tool cache), and MinIO / GCS (object storage).

## Kubernetes namespaces

| Namespace | Services |
|---|---|
| `control-plane` | `api-gateway`, `identity`, `access-control` |
| `kernel` | `scheduler-service`, `task-service`, `agent-service`, `goal-service`, `memory-service` |
| `workers` | `execution-worker`, `browser-worker`, `tool-runtime`, `worker-manager`, `llm-router`, `prompt-manager`, `evaluation-service` |
| `infrastructure` | Postgres, Redis, Memcached, MinIO (local) / Cloud SQL, Memorystore, GCS (GCP) |
| `observability` | Prometheus, Grafana, OpenTelemetry collector, Loki |

## Data flow: goal → task → result

The request flows through the following stages in order:

1. A user submits `POST /agents/{id}/goals`.
2. The `goal-service` validates the request, assembles agent context, and routes to the planner.
3. The `planner-service` uses an LLM-backed call to generate a DAG.
4. The `task-service` receives a `CreateGraph` call and persists the DAG to Postgres.
5. The `scheduler-service` detects ready tasks on its 100ms poll cycle.
6. The scheduler publishes to `XADD astra:tasks:shard:N` (a Redis stream).
7. An `execution-worker` claims the task from the stream and sets its status to `running`.
8. The `tool-runtime` executes the task in a sandbox.
9. `CompleteTask` is called: the result is persisted, a `TaskCompleted` event is emitted, and the scheduler unlocks dependent child tasks.

Every arrow is either a gRPC call or a Redis Streams publish/consume. No direct database calls across service boundaries.

## The 10ms SLA

The hard constraint shapes the entire cache strategy:

| Read type | Cache layer | TTL |
|---|---|---|
| Actor working state | Redis Hash `actor:state:{id}` | 5m |
| Agent profile | Redis Hash `agent:profile:{id}` | 5m |
| Agent documents | Redis JSON `agent:docs:{id}` | 5m |
| Task reads | Redis via `CachedStore` | short-lived |
| LLM responses | Memcached `llm:resp:{model}:{hash}` | 24h |
| Embeddings | Memcached `embed:{hash}` | 7-30d |

Write path: Postgres transaction → Redis Stream event → async cache update. Reads that miss fall through to Postgres and populate the cache for next time.

!!! warning "Tradeoff"
    This architecture accepts eventual consistency between Postgres and cache. Cache misses add latency. Write-through caching adds complexity. The alternative — synchronous Postgres reads on the hot path — doesn't meet the 10ms SLA at scale.

## Hardware targets

Astra runs on both macOS and Linux in production.

| Platform | Acceleration |
|---|---|
| macOS (Apple Silicon) | Metal (GPU), Neural Engine (ANE), native `darwin/arm64` binaries |
| macOS (Intel) | Metal where available, native `darwin/amd64` binaries |
| Linux | CUDA (NVIDIA GPUs), CPU fallback |

Backend selection is explicit via config (`ASTRA_USE_METAL=true`, `ASTRA_USE_CUDA=false`) with graceful fallback to CPU. The codebase uses a single abstraction layer for backend selection — no platform-specific code in the kernel.
