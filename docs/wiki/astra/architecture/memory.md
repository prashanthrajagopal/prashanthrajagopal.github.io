---
title: Memory Subsystem
tags:
  - astra
  - architecture
  - memory
  - pgvector
  - redis
---

# Memory Subsystem

Astra agents have three types of memory, each with different persistence, latency, and search characteristics.

## Memory tiers

| Tier | Storage | TTL | Use case |
|---|---|---|---|
| **Working** | Redis Hash `actor:state:{id}` | 5m sliding | Active actor state, in-flight computation |
| **Episodic** | Postgres `memories` table | Durable | What the agent did, when |
| **Semantic** | Postgres `memories` + pgvector index | Durable | What the agent knows, searchable by meaning |

All episodic and semantic memory is served through the `memory-service` (gRPC on port 9092). Working memory is accessed directly via Redis by the actor runtime.

## Go interface

The `MemoryClient` interface in `internal/memory` defines three methods: `Write` (accepts agent ID, memory type string, content string, and a float32 embedding slice), `Search` (accepts agent ID, query string, and topK integer; returns a slice of `Memory`), and `GetByID` (accepts a UUID and returns a single `*Memory`). See `internal/memory/` in the Astra repo.

## Database schema

The `memories` table (migration 0003) stores a UUID primary key, a reference to `agent_id`, a `memory_type` string, a `content` text field, a 1536-dimensional `embedding` vector (pgvector), and a `created_at` timestamp. An `ivfflat` index on the embedding column uses cosine distance ops for approximate nearest-neighbour search. See `migrations/0003_memories.sql` in the Astra repo.

Vector dimension: 1536 (OpenAI `text-embedding-3-small` / similar models). The `ivfflat` index is approximate nearest-neighbour — trades perfect recall for query speed. At large scale, consider `hnsw` instead.

## Semantic search query

Semantic search in `internal/memory/store.go` queries the `memories` table filtering by `agent_id`, ordering by `embedding <=> $2::vector` (pgvector's cosine distance operator — lower distance means more similar), and limiting to `topK` results. See `internal/memory/store.go` in the Astra repo.

## Phase-level memory

Migration 0009 adds `phase_runs` and `phase_summaries` for tracking what an agent did across a complete goal execution. The `phase_runs` table records a UUID primary key, references to `goal_id` and `agent_id`, a name, a status (`running`, `completed`, `failed`, or `cancelled`), `started_at` and `ended_at` timestamps, a `summary` text field, a JSONB `timeline`, and a `log_file_path`. The `phase_summaries` table records a UUID primary key, a reference to `phase_id`, a `content` text field, a 1536-dimensional embedding, and a `created_at` timestamp. See `migrations/0009_phase_history.sql` in the Astra repo.

Phase summaries are searchable semantically — agents can recall "what did I do last time I tackled a problem like this?"

!!! warning "Tradeoff"
    `ivfflat` requires knowing the approximate number of vectors at index creation time (`lists` parameter). Too few lists = slow queries. Too many = poor recall. This is a tuning parameter that needs to be revisited as `memories` grows. Track the row count and reindex when it crosses 100K+ rows.
