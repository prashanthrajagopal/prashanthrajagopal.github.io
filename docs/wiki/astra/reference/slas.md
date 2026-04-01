---
title: SLAs & Acceptance Criteria
tags:
  - astra
  - reference
  - sla
  - performance
---

# SLAs & Acceptance Criteria

## Production SLAs

| SLA | Target | Measurement |
|-----|--------|-------------|
| Control plane API availability | 99.9% | Uptime checks + gateway health |
| API read response time (p99) | ≤ 10ms | Histogram on cached read paths |
| Task scheduling latency (median) | ≤ 50ms | Ready detection → dispatch |
| Task scheduling latency (p95) | ≤ 500ms | End-to-end scheduling path |
| Task execution correctness | ≥ 99% pass rate | Task success / (success + failure) |
| Worker failure detection | ≤ 30s | Heartbeat stream gap |
| Event durability | ≤ 1s | Async path to durable audit log |

The 10ms read SLA is the hardest constraint in the system. It is the reason the cache architecture exists. Any code path that reads from Postgres synchronously on a hot API endpoint is a bug — not a performance issue, a correctness issue.

## MVP Milestone Map

| Phase | Capability | Status |
|-------|------------|--------|
| Phase 0 | Prep — repo scaffolding, infra, migrations | **COMPLETE** |
| Phase 1 | Kernel MVP — actors, state, messaging, task graph, scheduler | **COMPLETE** |
| Phase 2 | Workers & Tool Runtime — execution, Docker sandbox, worker manager | **COMPLETE** |
| Phase 3 | Memory & LLM Routing — pgvector, LLM router, Memcached caching | **COMPLETE** |
| Phase 4 | Orchestration, Eval, Security — planner, goal-service, identity, access-control, approvals | **COMPLETE** |
| Phase 5 | Scale & Production Hardening — load tests, Grafana, alerts, runbooks, cost tracking | **COMPLETE** |
| Phase 6 | SDK & Applications — AgentContext, MemoryClient, ToolClient, examples | **COMPLETE** |
| Phase 7 | Security Compliance — gRPC/HTTP TLS, Vault integration | **COMPLETE** |
| Phase 8 | Platform Dashboard — embedded UI, snapshot API, auto-refresh | **COMPLETE** |
| Phase 9 | Agent Profile & Context — system_prompt, agent_documents, context propagation | **COMPLETE** |
| Phase 10 | Chat Agents — WebSocket streaming, sessions, tool invocation | **COMPLETE** |
| P0-P2 | Platform Stability — agent restore, dead-letter, circuit breakers, idempotency, sharding | **COMPLETE** |
| Phase 11 | Multi-tenancy — orgs, teams, RBAC, visibility, data isolation | In progress |
| Phase 12 | Slack integration — adapter, proactive posting, platform secrets | Partial |

## MVP functional acceptance

| Criterion | Phase delivered |
|---|---|
| Spawn and run a persistent agent | Phase 1 |
| Planner produces task DAGs from a goal | Phase 4 |
| Scheduler detects ready tasks and dispatches to workers | Phase 1 |
| Worker executes tasks and returns results persisted in Postgres | Phase 1/2 |
| Task state transitions emit events to `events` table | Phase 1 |
| Observability traces visible for each task execution | Phase 5 |
| Tool runtime can run sandboxed command and return artifact | Phase 2 |

## Scale targets

| Target | Value |
|---|---|
| Concurrent agents | Millions |
| Tasks per day | 100M+ |
| No single API call > | 10ms |
| Worker failure detection | ≤ 30s |

These are **design targets**. Load-testing procedures live **in the Astra repo**.
