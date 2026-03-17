---
title: Database Schema
tags:
  - astra
  - reference
  - database
  - postgres
  - migrations
---

# Database Schema

All migrations are in `/migrations/`. All are idempotent (`IF NOT EXISTS`, `IF NOT EXISTS` on columns). Run order is the filename prefix.

## Extensions

Two Postgres extensions are required: `uuid-ossp` (for `uuid_generate_v4()`) and `vector` (pgvector, for embedding storage and search). See `migrations/` in the Astra repo.

## Migration index

| Migration | Description |
|---|---|
| 0001 | Core schema: `agents`, `goals`, `tasks` |
| 0002 | Task dependencies: `task_dependencies` |
| 0003 | Memories with pgvector: `memories` |
| 0004 | Artifacts: `artifacts` |
| 0005 | Workers: `workers` |
| 0006 | Indexes on core tables |
| 0007 | Events table: `events` |
| 0008 | Status constraints + `update_updated_at` trigger |
| 0009 | Phase history, LLM usage: `phase_runs`, `phase_summaries`, `llm_usage` |
| 0010 | Worker task tracking: `tasks.worker_id` column |
| 0011 | Prompts: `prompts` table |
| 0012 | Approval requests: `approval_requests` |
| 0013 | Agent profile + documents: `agents.system_prompt`, `agent_documents` |
| 0014 | Approval requests plan type: `request_type`, `goal_id`, `graph_id`, `plan_payload` |
| 0015 | Agents unique name: `UNIQUE(agents.name)` |
| 0016 | Chat: `chat_sessions`, `chat_messages`, `agents.chat_capable` |
| 0018 | Multi-tenancy: `users`, `organizations`, `org_memberships`, `teams`, `team_memberships`, `agent_collaborators`, `agent_admins` |
| 0022 | Agent ingest + Slack: `ingest_source_type`, `ingest_source_config`, `slack_notifications_enabled` on agents |
| 0024 | Agent platform hardening: `agent_config_revisions`, `tool_definitions`, drain mode, token budgets |

## Core tables

### `agents`

Stores registered agents. Columns: UUID primary key, `name` (unique text, enforced in migration 0015), `status` (active/stopped/error), `config` JSONB, `system_prompt` text (added in migration 0013), `chat_capable` boolean (migration 0016), and multi-tenancy columns added in migration 0018: `org_id` (references `organizations`), `owner_id` (references `users`), `team_id` (references `teams`), and `visibility` (global/public/team/private, defaulting to private). Also `created_at` and `updated_at`. See `migrations/0001_core.sql` in the Astra repo.

### `goals`

Stores agent goals. Columns: UUID primary key, `agent_id` (references `agents`, cascade delete), `goal_text`, `priority` (integer, default 100), `status` (default pending), and multi-tenancy columns `org_id` and `user_id` added in migration 0018. See `migrations/0001_core.sql` in the Astra repo.

### `tasks`

Stores task execution units. Columns: UUID primary key, `graph_id` UUID, `goal_id` (references `goals`, set null on delete), `agent_id` UUID, `type` text, `status` text (created/pending/queued/scheduled/running/completed/failed), `payload` JSONB, `result` JSONB, `priority` integer, `retries` integer, `max_retries` integer (default 5), `worker_id` UUID (added in migration 0010), `org_id` UUID (added in migration 0018), `created_at`, and `updated_at`. See `migrations/0001_core.sql` in the Astra repo.

### `task_dependencies`

Stores DAG edges between tasks. Columns: `task_id` and `depends_on`, both UUID foreign keys referencing `tasks` with cascade delete, forming a composite primary key. See `migrations/0002_task_dependencies.sql` in the Astra repo.

### `events`

Stores the event sourcing log. Columns: `id` bigserial primary key, `event_type` text, `actor_id` UUID, `payload` JSONB, `org_id` UUID (migration 0018), and `created_at`. Indexed on `actor_id`, `event_type`, and `created_at`. See `migrations/0007_events.sql` in the Astra repo.

### `memories`

Stores agent episodic and semantic memories. Columns: UUID primary key, `agent_id` (references `agents`, cascade delete), `memory_type` text, `content` text, `embedding` vector(1536) for pgvector, `org_id` UUID (migration 0018), and `created_at`. Indexed with an `ivfflat` index on the embedding column using cosine distance ops. See `migrations/0003_memories.sql` in the Astra repo.

### `workers`

Stores registered execution workers. Columns: UUID primary key, `hostname` text, `status` text (active/draining/offline), `capabilities` JSONB array, `last_heartbeat` timestamp, `org_id` UUID (migration 0018), and `created_at`. See `migrations/0005_workers.sql` in the Astra repo.

### `llm_usage`

Stores LLM call audit records. Columns: UUID primary key, `request_id` text, optional references to `agent_id` and `task_id`, `model` text, `tokens_in` and `tokens_out` integers, `latency_ms` integer, `cost_dollars` numeric(12,6), `org_id` and `user_id` UUIDs (migration 0018), and `created_at`. See `migrations/0009_phase_history.sql` in the Astra repo.

### `agent_documents`

Stores structured documents attached to agents (rules, skills, context docs, references). Columns: UUID primary key, `agent_id` (references `agents`, cascade delete), `goal_id` (references `goals`, set null; NULL means global to agent), `doc_type` text (rule/skill/context_doc/reference), `name` text, `content` text, `uri` text (for large docs stored in MinIO/GCS), `metadata` JSONB, `priority` integer, `created_at`, and `updated_at`. See `migrations/0013_agent_profile.sql` in the Astra repo.

### Multi-tenancy tables (migration 0018)

`users`, `organizations`, `org_memberships`, `teams`, `team_memberships`, `agent_collaborators`, `agent_admins` — see [Multi-Tenancy Architecture](../architecture/multi-tenancy.md) for full schema.
