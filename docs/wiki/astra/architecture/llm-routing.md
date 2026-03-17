---
title: LLM Routing
tags:
  - astra
  - architecture
  - llm
  - cost
---

# LLM Routing

LLM routing is infrastructure in Astra, not application code. The `llm-router` service (`cmd/llm-router`, gRPC port 9093) handles model selection, response caching, usage tracking, and cost controls. Agents and workers call the router — they don't call LLM providers directly.

## Model tiers

`ModelTier` is a string type with three values: `local` (fast, cheap, runs on-device), `premium` (high-capability, expensive), and `code` (code-optimised models). See `internal/llm/` in the Astra repo.

## Routing logic

The `Router.Route` method takes a task type and priority and returns a `ModelTier`. Classification tasks always return `local`. Code generation tasks return `code`. High-priority tasks (priority < 50) return `premium`. All other tasks default to `local`. This is the 90% path — override via task payload for edge cases. See `internal/llm/` in the Astra repo.

## Supported backends

| Backend | Notes |
|---|---|
| OpenAI | `tokens_in`/`tokens_out` parsed from provider response |
| Other REST chat APIs | Usage tracking when the adapter exposes token counts in the response |
| Gemini | Full usage tracking |
| Ollama | Local inference; tries `/v1/chat/completions` then `/chat/completions` (fallback for older versions) |
| MLX | Apple Silicon inference via `mlx_lm.server`; tries `/v1/chat/completions` then `/chat/completions` |

## Response caching

Memcached key: `llm:resp:{model}:{sha256(prompt)}`, TTL 24h.

On cache hit, the router returns the cached response **including stored token counts** — cached responses don't appear as zero-usage. This matters for accurate cost tracking.

## Async usage audit

Every LLM response emits usage to the `astra:usage` Redis stream. The stream consumer writes to `llm_usage` and appends a `LLMUsage` event to `events`. This keeps the request path under 10ms — no synchronous DB write on the LLM response path.

The `llm_usage` table (migration 0009) stores a UUID primary key, a `request_id` string, optional references to `agent_id` and `task_id`, the `model` name, `tokens_in` and `tokens_out` counts, `latency_ms`, `cost_dollars` (numeric to 6 decimal places), and `created_at`. See `migrations/0009_phase_history.sql` in the Astra repo.

## Cost controls

| Control | Mechanism |
|---|---|
| Token quota per agent | Redis key `agent:{id}:tokens:YYYY-MM-DD`, O(1) admission check |
| Daily budget cap | Hard cap with admin approval flow for override |
| Response caching | Memcached — identical prompts never hit the provider twice |
| Model downgrade | Cost spike alert disables premium routing automatically |
| LLM inflight cap | `ASTRA_LLM_MAX_INFLIGHT` env var limits concurrent LLM calls |

## Metrics

Prometheus counters exported by the router: `astra_llm_token_usage_total` (tokens consumed) and `astra_llm_cost_dollars` (cost in USD).

Alerts: cost spike >2x daily average → page; automatic premium tier disable. See [Operations: LLM Cost Spike](../operations/runbook-cost-spike.md).
