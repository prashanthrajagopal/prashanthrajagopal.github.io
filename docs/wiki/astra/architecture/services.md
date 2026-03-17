---
title: Services
tags:
  - astra
  - architecture
  - services
  - microservices
---

# Services — 16 Canonical Microservices

Each service is an independent process in the monorepo (`cmd/<service>/main.go`). Each scales horizontally. Services communicate via gRPC (internal) or REST (external via api-gateway).

## Service catalogue

| # | Service | Namespace | Port | Responsibility |
|---|---|---|---|---|
| 1 | `api-gateway` | control-plane | 8080 | REST/gRPC gateway, auth middleware, rate limiting, versioning; chat sessions, WebSocket streaming |
| 2 | `identity` | control-plane | 8085 | User management (CRUD, login, password reset), JWT tokens, service-to-service tokens |
| 3 | `access-control` | control-plane | 8086 | Policy engine (RBAC, super_admin), approval workflows, approval assignment |
| 4 | `agent-service` | kernel | 9091 | Agent lifecycle (spawn/stop/inspect), actor supervisor integration, agent profile & document management |
| 5 | `goal-service` | kernel | 8088 | Goal ingestion, validation, routing to planner, context assembly (system_prompt + documents) |
| 6 | `planner-service` | kernel | 8087 | Core planner: goals → TaskGraphs using LLM |
| 7 | `scheduler-service` | kernel | — | Distributed scheduler, shard manager, ready-task dispatch |
| 8 | `task-service` | kernel | 9090 | Task CRUD, dependency engine API, state queries |
| 9 | `llm-router` | workers | 9093 | Model routing (local/premium/code), response caching, rate limiting, usage metrics |
| 10 | `prompt-manager` | workers | — | Prompt templates, versions, A/B prompt experiments |
| 11 | `evaluation-service` | workers | 8089 | Result validators, test harnesses, auto-evaluators |
| 12 | `worker-manager` | workers | 8082 | Worker registration, health monitoring, scaling hints, orphan task recovery |
| 13 | `execution-worker` | workers | — | General worker runtime (consumes tasks from Redis streams) |
| 14 | `browser-worker` | workers | — | Headless browser automation (Playwright/Puppeteer); consumes `astra:tasks:browser` stream |
| 15 | `tool-runtime` | workers | 8083 | Tool sandbox controller (WASM/Docker/Firecracker lifecycle), `POST /execute` |
| 16 | `memory-service` | kernel | 9092 | Episodic/semantic memory, embedding pipeline, pgvector search |

**Chat (v1):** Chat capability is built into `api-gateway`. No separate chat service for Phase 10.

## Inter-service communication

```
External → api-gateway (REST/WebSocket)
           ↓ gRPC
           agent-service, task-service, goal-service (kernel services)
           ↓ gRPC
           llm-router, memory-service, planner-service
           ↓ Redis Streams
           execution-worker, browser-worker
           ↓ HTTP
           tool-runtime (sandbox execution)
```

## Agent lifecycle flow

```
POST /agents/{id}/goals
→ goal-service: validate + assemble agent context (system_prompt + rules + skills + context_docs)
→ planner-service: LLM-backed goal → DAG (each task payload embeds agent_context)
→ task-service: CreateGraph (persist tasks + dependencies to Postgres)
→ scheduler-service: detect ready tasks → XADD astra:tasks:shard:N
→ execution-worker: claim task → tool-runtime for execution → CompleteTask/FailTask
→ evaluation-service: validate result
```

## Chat API (Phase 10)

| Method | Path | Description |
|---|---|---|
| `POST` | `/chat/sessions` | Create a chat session (`agent_id`, `title`) |
| `GET` | `/chat/sessions` | List chat sessions for authenticated user |
| `GET` | `/chat/sessions/{id}` | Get chat session details |
| `GET` | `/chat/ws` | WebSocket upgrade for streaming chat |

WebSocket protocol: JSON frames with types `chunk`, `message_start`, `message_end`, `tool_call`, `tool_result`, `done`, `error`, `pong`, `session`.

## Agent profile and documents API (Phase 9)

| Method | Path | Description |
|---|---|---|
| `PATCH` | `/agents/{id}` | Update agent profile (system_prompt, config) |
| `GET` | `/agents/{id}/profile` | Get agent profile (Redis cache, 5min TTL) |
| `POST` | `/agents/{id}/documents` | Attach document (rule/skill/context_doc/reference) |
| `GET` | `/agents/{id}/documents` | List agent documents, optional `?doc_type=` filter |
| `DELETE` | `/agents/{id}/documents/{doc_id}` | Remove document |
