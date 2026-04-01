---
title: Glossary
tags:
  - astra
  - reference
---

# Glossary

Alphabetical terms used across the Astra wiki. Authoritative definitions and API details live in the **PRD** (`docs/PRD.md` in the Astra repo).

| Term | Meaning |
|------|---------|
| **Access-control** | Service enforcing policy, approvals, and RBAC checks (PRD §9, §18). |
| **Actor** | Lightweight concurrent unit with mailbox; goroutine-based in the Go implementation (PRD §6). |
| **Adapter** | Integration bridge between Astra and an external agent platform (e.g., D.TEC). Implements DispatchGoal, PollStatus, HandleCallback, ListCapabilities, HealthCheck. Thread-safe registry. |
| **Agent** | Long-lived entity users spawn; backed by `agent-service` and actor supervision (PRD §16). |
| **Agent document** | Context attached to an agent: `rule`, `skill`, `context_doc`, or `reference`. Priority-sorted and assembled into agent context for planning/execution. Stored in `agent_documents` table (PRD §11). |
| **API gateway** | Edge REST/gRPC, JWT, rate limits, WebSocket chat (PRD §9). |
| **Cascade** | Chain of goals linked by `cascade_id`; completing one goal triggers dependent goals. Used in Olympus for multi-step event response workflows. |
| **Chat session** | WebSocket-backed conversation between a user and a chat-capable agent. Created via REST, upgraded at `/chat/ws`, stores message history with streaming responses (PRD §9, §16). |
| **Circuit breaker** | Gateway pattern that opens after repeated downstream failures (5 in 30s), returning 503 + Retry-After. 10s half-open cooldown. Protects goal-service, agent-service, access-control (PRD §21). |
| **Consumer group** | Redis Streams group for competing workers claiming messages (PRD §8, §12). |
| **DAG** | Directed acyclic graph of tasks and dependencies (PRD §7). |
| **Dead letter** | Terminal task status when retries exhausted (`retries >= max_retries`). Optionally published to `astra:dead_letter` stream for alerting/repair (PRD §7, §21). |
| **Dual-approval** | Two-person approval rule. `required_approvals` count on approval_requests; individual decisions tracked in `approvals` JSONB array (PRD §18). |
| **Episodic memory** | Time-ordered experiences stored durably; search via pgvector where applicable (PRD §13). |
| **Goal** | User-submitted intent that the planner turns into a task graph (PRD §7, §15). |
| **Hot path** | Request paths that must meet sub-10ms read SLAs — cache-only reads (PRD §25). |
| **Idempotency key** | Client header (`Idempotency-Key`) on `POST /goals` preventing duplicate creation. Redis-backed, 24h TTL; duplicates return same `goal_id` (PRD §21). |
| **Identity** | User CRUD, login, JWT issuance (PRD §9). |
| **Kernel** | Microkernel: actors, tasks, scheduler, messaging, state — not full business logic (PRD §5). |
| **LLM router** | Model selection, caching, rate limits for inference calls (PRD §23). |
| **mTLS** | Mutual TLS between services (PRD §18). |
| **OPA** | Open Policy Agent–style policy evaluation pattern via access-control (platform rules). |
| **Planner** | Service that expands goals into task graphs using LLM (PRD §9). |
| **Proactive posting** | Astra posting to Slack without a prior user message (e.g., "Plan pending approval"). Uses `POST /internal/slack/post` with `X-Slack-Internal-Secret` auth (PRD §16). |
| **Sandbox** | WASM / Docker / Firecracker environment for tool execution (PRD §14). |
| **Scheduler** | Owns shards, ready-task detection, `XADD` to Redis task streams (PRD §8). |
| **Semantic memory** | Embedding-backed retrieval over stored knowledge (PRD §13). |
| **Shard** | Partition of scheduling / stream traffic for horizontal scale (PRD §8). |
| **Shard ownership** | Task streams partitioned by `hash(agent_id) % TASK_SHARD_COUNT`. Configurable count; consistent hashing for rebalancing; workers consume all shards (PRD §8). |
| **Task** | Unit of work in the graph; states include pending, queued, running, completed, failed, dead_letter (PRD §7). |
| **Task service** | CRUD and dependency API for tasks and graphs (PRD §9). |
| **Trust score** | Numeric reliability score on agents (`agents.trust_score`). Used for policy gating, e.g., requiring approval below a threshold (PRD §26). |
| **Vault** | Runtime secret injection; no secrets in code or logs (PRD §18). |
| **Webhook ingest** | Service accepting external events via `POST /webhooks/{source_id}` with HMAC-SHA256 validation. Publishes normalized events to Redis streams (PRD §26). |
| **Worker** | Process that claims tasks from streams (`execution-worker`, `browser-worker`, etc.) (PRD §9). |
| **Working memory** | Short-lived actor/agent state in Redis (PRD §13). |
