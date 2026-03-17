---
title: Getting Started
tags:
  - astra
  - setup
  - getting-started
---

# Getting Started

What you need to run Astra locally, orient yourself in the codebase, and understand the system before touching anything.

## Prerequisites

- Go 1.22+
- Docker + Docker Compose
- `buf` (protobuf toolchain)
- `golangci-lint`

## Quickstart

To get Astra running locally: clone the repo, start infrastructure with `docker compose up -d`, run migrations with `go run ./scripts/migrate`, build all services with `go build ./...`, then start everything with `./scripts/deploy.sh`.

The deploy script starts all 16 services as native processes. Infrastructure (Postgres, Redis, Memcached, MinIO) runs in Docker; services run natively on your machine. This is intentional — fast iteration, real debuggers, no container rebuild cycle.

## Orientation

### The kernel boundary

The most important thing to understand before reading any code: the kernel is small by constraint, not by accident.

The system is layered from top to bottom as follows. At the top, Applications (Agent Apps) use the Astra SDK (the agent dev framework), which in turn calls into the Astra Kernel (microkernel). The kernel contains five components: the Actor Runtime, Task Graph Engine, Scheduler, Message Bus, and State Manager. Below the kernel sits Infrastructure: Postgres (primary + replicas), Redis (streams, state, locks), Memcached (LLM/embedding cache), and MinIO / GCS (object storage).

Application code and agent logic never touch kernel internals directly. They go through the SDK, which calls kernel APIs. This boundary is enforced: `internal/*` packages cannot be imported by anything outside the monorepo.

### Monorepo layout

The repo is organized as follows: `cmd/` holds service entrypoints (one directory per service); `internal/` holds private implementation packages for the kernel and services; `pkg/` holds stable shared packages (db, config, logger, grpc, metrics); `proto/` holds protobuf/gRPC definitions; `migrations/` holds SQL migrations (ordered, idempotent); `deployments/` holds Helm charts and Kubernetes manifests; `tests/` holds integration and end-to-end fixtures; and `docs/` holds PRDs and design docs (source of truth).

### Layer order

Build/import order is enforced by design. Nothing in a lower layer may import from a higher layer.

| Layer | Packages |
|---|---|
| 0 — Foundation | `pkg/config`, `pkg/logger`, `pkg/metrics`, `pkg/models`, `pkg/db`, `pkg/grpc`, `pkg/otel` |
| 1 — Kernel primitives | `internal/actors`, `internal/messaging`, `internal/events` |
| 2 — Kernel engine | `internal/kernel`, `internal/tasks`, `internal/scheduler` |
| 3 — Services | `internal/llm`, `internal/agent`, `internal/planner`, `internal/memory`, `internal/workers`, `internal/tools`, `internal/evaluation`, `internal/agentdocs`, `internal/identity`, `internal/rbac` |
| 4 — Entrypoints | All `cmd/*` services |

## First tasks

If you're new to the codebase, read in this order:

1. [`internal/actors`](../architecture/actor-framework.md) — understand the actor model before anything else
2. [`internal/tasks`](../architecture/task-graph.md) — understand task state machine and DAG
3. [`internal/scheduler`](../architecture/scheduler.md) — understand how tasks get dispatched
4. [`cmd/api-gateway`](../reference/api-endpoints.md) — understand the external API surface
5. [Phase roadmap](../roadmap/index.md) — understand what's built and what isn't

## Verify your setup

To verify your setup, check that all services report healthy by calling `GET http://localhost:8080/health`. Then spawn a test agent with `POST http://localhost:8080/agents` (JSON body: `{"name": "test-agent"}`), and submit a goal with `POST http://localhost:8080/agents/{agent_id}/goals` (JSON body: `{"goal_text": "Hello Astra", "priority": 100}`).

The [validate script](../../deployment/local.md) runs a full structural check: `./scripts/validate.sh`.
