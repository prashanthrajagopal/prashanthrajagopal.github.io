---
title: Redis Keys
tags:
  - astra
  - reference
  - redis
  - cache
---

# Redis Keys

Redis is used for **caches**, **locks**, **streams**, and **ephemeral coordination**. **PRD §12–13** is authoritative for MAXLEN, lock algorithms, and any unlisted keys.

## Cache keys

| Key pattern | Type | TTL | Description |
|-------------|------|-----|-------------|
| `agent:profile:<agent_id>` | Hash | 5 min | Cached agent profile (system_prompt, config, metadata) |
| `agent:docs:<agent_id>` | String (JSON) | 5 min | Cached agent document list |
| `user:<user_id>` | Hash | 5 min | Cached user profile |
| `user:orgs:<user_id>` | String (JSON) | 5 min | Cached org memberships for user |
| `org:members:<org_id>` | String (JSON) | 5 min | Cached org member list |
| `org:teams:<org_id>` | String (JSON) | 5 min | Cached team list for org |

Cache writes **invalidate** relevant keys on mutation so callers do not see stale data beyond the TTL.

## Budget counters

| Key pattern | Type | Description |
|-------------|------|-------------|
| `agent:{id}:tokens:YYYY-MM-DD` | String (counter) | Daily token budget counter — O(1) admission check via INCR/GET against `daily_token_budget` limit |

## Coordination keys (operational)

| Family | Purpose |
|--------|---------|
| Task / graph | Short-lived claim locks, read cache |
| Worker | Liveness / heartbeat tracking |
| Actor / agent | Working state during task execution |

## Streams

| Stream | Purpose |
|--------|---------|
| `astra:tasks:<shard>` | Sharded task dispatch to workers |
| `astra:workers:heartbeat` | Worker liveness signals |
| `astra:dead_letter` | Dead-lettered tasks (exhausted retries) |
| `astra:usage` | Async LLM usage fan-out to `llm_usage` table |
| `astra:goals:completed` | Goal completion events for cascade tracking |
| `astra:slack:incoming` | Slack inbound events from slack-adapter |
| `olympus:triggers:raw` | Webhook trigger events from Olympus ingest |

Consumer groups process messages with **ack** semantics. Unacked messages that exceed retry policy are moved to `astra:dead_letter`.
