---
title: "Runbook: LLM Cost Spike"
tags:
  - astra
  - operations
  - runbook
  - llm
  - cost
---

# Runbook: LLM Cost Spike

**Alert:** `LLMCostSpike` — >2x daily average LLM cost.

## Detection

1. Check today's cost by model: query Postgres for `model`, `SUM(tokens_in)`, `SUM(tokens_out)`, and `SUM(cost_dollars)` from `llm_usage` where `created_at > date_trunc('day', now())`, grouped by `model` and ordered by total cost descending.
2. Identify which agents are responsible: query `agent_id`, `model`, and `SUM(cost_dollars)` from `llm_usage` where `created_at > now() - interval '1 hour'`, grouped by agent and model, ordered by cost descending, limited to 20 rows.

## Containment

1. Disable premium model routing immediately by setting `ASTRA_DISABLE_PREMIUM=true` on the `llm-router` deployment: run `kubectl set env deployment/llm-router -n workers ASTRA_DISABLE_PREMIUM=true`.
2. Alternatively, lower the inflight cap to reduce throughput: run `kubectl set env deployment/llm-router -n workers ASTRA_LLM_MAX_INFLIGHT=10`.

## Identify root cause

| Pattern | Likely cause |
|---|---|
| One agent consuming all cost | Agent loop, misconfigured max_retries, or runaway planner |
| Spike on `premium` tier | Routing bug — tasks not classified correctly |
| Cache miss rate high | Memcached down, or prompts not deterministic (random seeds in prompts) |
| Cost per task much higher than baseline | Context window bloat — agent documents too large? |

## Check for agent loops

Query Postgres for agents that submitted more than 10 goals in the last hour: select `agent_id`, `count(*)`, `min(created_at)`, and `max(created_at)` from `goals` where `created_at > now() - interval '1 hour'`, grouped by `agent_id`, filtered with `HAVING count(*) > 10`, ordered by count descending.

## Remediation

1. If a looping agent is identified, stop it via `POST /agents/{id}/stop`.
2. Fix the routing rule that caused premium tier overuse.
3. Review agent documents for context bloat — large `context_doc` type docs inflate every LLM call.
4. Re-enable premium routing only after root cause is addressed.

## Verify

Confirm cost is returning to baseline: query Postgres for `date_trunc('hour', created_at)` and `SUM(cost_dollars)` from `llm_usage` where `created_at > now() - interval '24 hours'`, grouped by hour and ordered by hour.
