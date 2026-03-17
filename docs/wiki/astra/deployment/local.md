---
title: Local Development
tags:
  - astra
  - deployment
  - local
  - docker-compose
---

# Local Development

Infrastructure runs in Docker Compose. Services run as native Go binaries. This is intentional — native processes start in milliseconds, run in your debugger, and don't require image rebuilds.

## Quick start

1. Start infrastructure (Postgres, Redis, Memcached, MinIO) with `docker compose up -d`.
2. Run all migrations with `go run ./scripts/migrate` (or apply them directly with `psql -f migrations/*.sql`).
3. Build all services with `go build ./...`.
4. Start all services with `./scripts/deploy.sh`.

`deploy.sh` starts all 16 services as background processes. Service ports match the gRPC/HTTP ports defined in each service's `main.go`.

## Validate setup

Run `./scripts/validate.sh` to check binary builds, migration state, service health endpoints, and structural correctness. Run after any major change.

## Service ports

| Service | Protocol | Port |
|---|---|---|
| `api-gateway` | HTTP/REST | 8080 |
| `identity` | HTTP | 8085 |
| `access-control` | HTTP | 8086 |
| `planner-service` | HTTP | 8087 |
| `goal-service` | HTTP | 8088 |
| `evaluation-service` | HTTP | 8089 |
| `worker-manager` | HTTP | 8082 |
| `tool-runtime` | HTTP | 8083 |
| `task-service` | gRPC | 9090 |
| `agent-service` | gRPC | 9091 |
| `memory-service` | gRPC | 9092 |
| `llm-router` | gRPC | 9093 |

## Environment config

Copy `.env.example` to `.env`. The required environment variables are:

- `POSTGRES_DSN` — connection string for Postgres (e.g. `postgres://astra:astra@localhost:5432/astra?sslmode=disable`)
- `REDIS_ADDR` — Redis address (e.g. `localhost:6379`)
- `MEMCACHED_ADDR` — Memcached address (e.g. `localhost:11211`)
- LLM provider key — one of `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `OLLAMA_BASE_URL` for local inference
- `ASTRA_USE_METAL` — set to `true` on macOS to enable Metal acceleration
- `ASTRA_USE_CUDA` — set to `false` unless on Linux with NVIDIA GPU
- `AUTO_APPROVE_PLANS` — set to `true` to disable plan approval flow during development
- `ASTRA_LLM_MAX_INFLIGHT` — maximum concurrent LLM calls (e.g. `20`)

See `.env.example` in the Astra repo.

## Dashboard

After starting services, the super-admin dashboard is at `http://localhost:8080/superadmin/dashboard/`.

Default credentials (set via `ASTRA_SUPER_ADMIN_EMAIL` and `ASTRA_SUPER_ADMIN_PASSWORD` in `.env`).
