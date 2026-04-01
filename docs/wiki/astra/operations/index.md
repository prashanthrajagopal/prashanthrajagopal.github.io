---
title: Operations
tags:
  - astra
  - operations
  - runbooks
---

# Operations

Runbooks, oncall procedures, and incident response for Astra. The authoritative runbooks also live in **`docs/runbooks/`** in the Astra repo — these pages are the wiki summary. For step-by-step shell commands during an incident, use the repo runbooks.

## Severity levels

| Level | Meaning | Example |
|-------|---------|---------|
| **SEV1** | Platform down or data loss risk | Postgres primary unreachable for all traffic |
| **SEV2** | Major degradation | Single region Redis loss, elevated task failures |
| **SEV3** | Minor / isolated | One worker pool stuck, non-prod only |

## Communication

- Post in the designated **incident channel**; nominate **incident commander** for SEV1/2.  
- Update **status page** (if configured) when user-visible.  
- **Stakeholders:** product owner for sustained SEV1; security for auth or data exposure.

## Runbooks

| Runbook | Trigger |
|---|---|
| [Worker Lost](runbook-worker-lost.md) | Heartbeat lost >30s |
| [High Error Rate](runbook-high-error-rate.md) | >5% task failures over 5min |
| [Postgres Outage](runbook-postgres-outage.md) | DB connection errors platform-wide |
| [Redis Failure](runbook-redis-failure.md) | Redis connection errors or data loss |
| [LLM Cost Spike](runbook-cost-spike.md) | Cost >2x daily average |
| Shard Scaling | Shard imbalance or scaling event — update `TASK_SHARD_COUNT`, restart scheduler + workers |
| TLS Rotation | Certificate expiration — generate new certs, update K8s secrets, roll services |
| Vault Setup | Initial or reconfigured — set `ASTRA_VAULT_ADDR`/`TOKEN`/`PATH`, load secrets to KV-v2 |

## Failure modes (P0–P2)

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Task final failure (max retries) | `FailTask` with `retries >= maxRetries` | Status → `dead_letter`; optional publish to `astra:dead_letter` for alerting/repair |
| Agent-service restart | Process restart | Agent restore loads active agents from DB, spawns into kernel automatically |
| Downstream overload | Circuit breaker opens | Gateway returns 503 + `Retry-After`; clients back off |
| Duplicate `POST /goals` | Same `Idempotency-Key` within TTL | Goal-service returns cached 201 with same `goal_id` |
| Scheduler shard imbalance | Monitoring | Rebalance via `TASK_SHARD_COUNT`; see shard-scaling runbook |
| Actor mailbox full | Kernel returns `ResourceExhausted` | Client backs off; `retry-after` in gRPC trailer |

## Oncall rotations

| Rotation | Scope |
|---|---|
| **Kernel SRE** | Scheduler, actors, tasks, messaging, state manager |
| **Agent Platform** | Workers, tools, memory, LLM routing |

Full escalation matrix: `docs/runbooks/` in the Astra repo.

## Incident lifecycle

```
Detect → Triage → Contain → Remediate → Postmortem → Remediation Review
```

## Upgrade plan

- Kernel upgrades must be backward-compatible on message contracts and schemas
- Rolling upgrades with canary: 5% traffic for 30 minutes, then full rollout
- DB migrations: schema changes must be backward-compatible with the current running binary (add columns before removing them)
- Blue/green deployment where possible for zero-downtime schema migrations
