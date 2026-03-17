---
title: Services
tags:
  - astra
  - architecture
  - services
  - microservices
---

# Services — 16 Canonical Microservices

Each service is an **independently scalable process**. Services communicate over **gRPC** (internal, with **mTLS**) and expose **REST/WebSocket** only at the **API gateway** edge.

**External API surface:** Humans and integrations call **REST/WebSocket** on `api-gateway` only, with **JWT** auth. **Internal API:** services call each other over **gRPC with mTLS** — no direct Postgres access across arbitrary service boundaries; each service owns its integration pattern with the DB or cache.

```mermaid
flowchart TB
  subgraph cp [control-plane]
    GW[api-gateway]
    ID[identity]
    AC[access-control]
  end
  subgraph kern [kernel]
    AG[agent-service]
    GL[goal-service]
    PL[planner-service]
    SCH[scheduler-service]
    TK[task-service]
    MEM[memory-service]
  end
  subgraph wrk [workers]
    LLM[llm-router]
    PM[prompt-manager]
    EV[evaluation-service]
    WM[worker-manager]
    EX[execution-worker]
    BR[browser-worker]
    TR[tool-runtime]
  end
  GW --> AG
  GW --> GL
  GL --> PL
  PL --> TK
  SCH --> EX
  EX --> TR
```

## Service catalogue

| # | Service | Namespace | Responsibility |
|---|---------|-----------|----------------|
| 1 | `api-gateway` | control-plane | REST/WebSocket gateway, auth, rate limits, versioning |
| 2 | `identity` | control-plane | Users, JWT, service identity |
| 3 | `access-control` | control-plane | RBAC, approvals |
| 4 | `agent-service` | kernel | Agent lifecycle, profile & documents |
| 5 | `goal-service` | kernel | Goals, context to planner |
| 6 | `planner-service` | kernel | Goals → task graphs (LLM) |
| 7 | `scheduler-service` | kernel | Ready tasks, dispatch |
| 8 | `task-service` | kernel | Task/graph API |
| 9 | `llm-router` | workers | Model routing, cache, cost |
| 10 | `prompt-manager` | workers | Prompt templates & experiments |
| 11 | `evaluation-service` | workers | Validation & eval |
| 12 | `worker-manager` | workers | Worker registry & health |
| 13 | `execution-worker` | workers | General task execution |
| 14 | `browser-worker` | workers | Browser automation tasks |
| 15 | `tool-runtime` | workers | Sandboxed tool execution |
| 16 | `memory-service` | kernel | Episodic / semantic memory |

**Chat (v1):** Chat capability is built into `api-gateway`. No separate chat service for Phase 10.

## Inter-service communication

```
External → api-gateway (REST/WebSocket)
           ↓ gRPC
           agent-service, task-service, goal-service (kernel services)
           ↓ gRPC
           llm-router, memory-service, planner-service
           ↓ stream queues
           execution-worker, browser-worker
           ↓
           tool-runtime (sandbox)
```

## Agent lifecycle flow (summary)

**Goal submitted** → **context assembled** → **planner** builds **DAG** → **task service** persists graph → **scheduler** dispatches → **workers** run steps (including **sandbox** where needed) → **evaluation** where configured. Details: **PRD §9, §15**.

## Chat API (Phase 10)

| Method | Path | Description |
|---|---|---|
| `POST` | `/chat/sessions` | Create a chat session (`agent_id`, `title`) |
| `GET` | `/chat/sessions` | List chat sessions for authenticated user |
| `GET` | `/chat/sessions/{id}` | Get chat session details |
| `GET` | `/chat/ws` | WebSocket upgrade for streaming chat |

WebSocket framing: **JSON message types** per **PRD** (streaming, tools, errors).

## Agent profile and documents (summary)

| Method | Path | Description |
|---|---|---|
| `PATCH` | `/agents/{id}` | Update agent profile |
| `GET` | `/agents/{id}/profile` | Cached profile |
| `POST` | `/agents/{id}/documents` | Attach document (rule/skill/context_doc/reference) |
| `GET` | `/agents/{id}/documents` | List agent documents, optional `?doc_type=` filter |
| `DELETE` | `/agents/{id}/documents/{doc_id}` | Remove document |
