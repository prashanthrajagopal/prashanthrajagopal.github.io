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
| **Agent** | Long-lived entity users spawn; backed by `agent-service` and actor supervision (PRD §16). |
| **API gateway** | Edge REST/gRPC, JWT, rate limits, WebSocket chat (PRD §9). |
| **Consumer group** | Redis Streams group for competing workers claiming messages (PRD §8, §12). |
| **DAG** | Directed acyclic graph of tasks and dependencies (PRD §7). |
| **Episodic memory** | Time-ordered experiences stored durably; search via pgvector where applicable (PRD §13). |
| **Goal** | User-submitted intent that the planner turns into a task graph (PRD §7, §15). |
| **Hot path** | Request paths that must meet sub-10ms read SLAs — cache-only reads (PRD §25). |
| **Identity** | User CRUD, login, JWT issuance (PRD §9). |
| **Kernel** | Microkernel: actors, tasks, scheduler, messaging, state — not full business logic (PRD §5). |
| **LLM router** | Model selection, caching, rate limits for inference calls (PRD §23). |
| **mTLS** | Mutual TLS between services (PRD §18). |
| **OPA** | Open Policy Agent–style policy evaluation pattern via access-control (platform rules). |
| **Planner** | Service that expands goals into task graphs using LLM (PRD §9). |
| **Sandbox** | WASM / Docker / Firecracker environment for tool execution (PRD §14). |
| **Scheduler** | Owns shards, ready-task detection, `XADD` to Redis task streams (PRD §8). |
| **Semantic memory** | Embedding-backed retrieval over stored knowledge (PRD §13). |
| **Shard** | Partition of scheduling / stream traffic for horizontal scale (PRD §8). |
| **Task** | Unit of work in the graph; states include pending, queued, running, completed, failed (PRD §7). |
| **Task service** | CRUD and dependency API for tasks and graphs (PRD §9). |
| **Vault** | Runtime secret injection; no secrets in code or logs (PRD §18). |
| **Worker** | Process that claims tasks from streams (`execution-worker`, `browser-worker`, etc.) (PRD §9). |
| **Working memory** | Short-lived actor/agent state in Redis (PRD §13). |
