---
title: Redis Keys
tags:
  - astra
  - reference
  - redis
  - cache
---

# Redis Keys

All Redis key patterns, types, TTLs, and purposes. Keys follow `{namespace}:{entity}:{id}` convention.

## Structured state (Redis Hash / String)

| Key Pattern | Type | TTL | Purpose |
|---|---|---|---|
| `actor:state:<actor_id>` | Hash | 5m | Working memory for active actors |
| `lock:task:<task_id>` | String (SET NX PX) | 30s | Distributed lock for task claiming (Redlock) |
| `worker:heartbeat:<worker_id>` | String | 30s | Worker liveness tracking |
| `agent:profile:<agent_id>` | Hash | 5m | Cached agent profile (system_prompt, config) |
| `agent:docs:<agent_id>` | String (JSON) | 5m | Cached agent documents list (rules, skills, context_docs) |
| `user:<user_id>` | Hash | 5m | Cached user profile (email, name, is_super_admin) |
| `user:orgs:<user_id>` | String (JSON) | 5m | Cached org memberships for user |
| `org:members:<org_id>` | String (JSON) | 5m | Cached org member list |
| `org:teams:<org_id>` | String (JSON) | 5m | Cached team list for org |
| `task:<task_id>` | String (JSON) | short | Cached task read (`CachedStore`) |
| `graph:<graph_id>` | String (JSON) | short | Cached graph read (`CachedStore`) |
| `agent:<id>:tokens:YYYY-MM-DD` | String (counter) | 24h from midnight | Daily token budget admission counter (O(1) check) |

## Distributed locking

Worker task claiming uses `SET NX PX 30000` on `lock:task:<task_id>`. This is Redlock-style single-node locking — sufficient for the current single-Redis deployment. For a Redis Cluster, implement the full Redlock algorithm across cluster nodes.

## Invalidation

Writes invalidate cache keys immediately:
- `PATCH /agents/{id}` → `DEL agent:profile:<id>`, `DEL agent:docs:<id>`
- Agent document create/delete → `DEL agent:docs:<id>`
- User update → `DEL user:<id>`, `DEL user:orgs:<id>`

## Stream keys

| Stream | Consumer groups |
|---|---|
| `astra:events` | `astra-consumers` |
| `astra:tasks:shard:<n>` | `worker-group`, one per shard |
| `astra:agent:events` | `agent-consumers` |
| `astra:worker:events` | `worker-monitor` |
| `astra:evaluation` | `eval-consumers` |
| `astra:usage` | `usage-writer` (writes to `llm_usage` + `events`) |

All streams use `MAXLEN ~ 1000000` to prevent unbounded growth. Messages are ACK'd after successful processing. Unacked messages after 3 attempts go to dead-letter.
