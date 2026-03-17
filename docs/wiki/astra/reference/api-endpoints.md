---
title: API Endpoints
tags:
  - astra
  - reference
  - api
  - rest
---

# API Endpoints

All REST endpoints are served by `cmd/api-gateway` on port 8080.

## Authentication

| URL | Auth |
|---|---|
| `GET /health` | None |
| `POST /users/login` | None |
| All other routes | JWT (`Authorization: Bearer <token>`) |

JWT tokens issued by `identity` service carry: `user_id`, `email`, `is_super_admin`, `scopes`.

## Agents

| Method | Path | Description |
|---|---|---|
| `POST` | `/agents` | Create agent |
| `GET` | `/agents/{id}` | Get agent |
| `PATCH` | `/agents/{id}` | Update agent profile (system_prompt, config) |
| `GET` | `/agents/{id}/profile` | Get agent profile (Redis cache, 5min TTL) |
| `POST` | `/agents/{id}/documents` | Attach document to agent |
| `GET` | `/agents/{id}/documents` | List agent documents (`?doc_type=rule|skill|context_doc|reference`) |
| `DELETE` | `/agents/{id}/documents/{doc_id}` | Remove document |

## Goals & Tasks

| Method | Path | Description |
|---|---|---|
| `POST` | `/agents/{id}/goals` | Submit goal (accepts optional `documents` array) |
| `GET` | `/tasks/{id}` | Get task state |
| `GET` | `/graphs/{id}` | Get full task graph |
| `POST` | `/tasks/{id}/complete` | Mark task completed (internal) |

## Chat (Phase 10)

| Method | Path | Description |
|---|---|---|
| `POST` | `/chat/sessions` | Create chat session (`agent_id`, `title`) |
| `GET` | `/chat/sessions` | List chat sessions |
| `GET` | `/chat/sessions/{id}` | Get chat session |
| `GET` | `/chat/ws` | WebSocket upgrade for streaming chat |

## Dashboard

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/superadmin/dashboard/` | super_admin JWT | Platform dashboard UI |
| `GET` | `/superadmin/api/dashboard/snapshot` | JWT | Service health, workers, agents, approvals, cost, logs |
| `GET` | `/superadmin/api/dashboard/goals/{id}` | JWT | Goal detail with tasks |

## Internal

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/internal/slack/post` | `X-Slack-Internal-Secret` header | Proactive Slack post (Phase 12) |
| `POST` | `/internal/apply-plan/{approval_id}` | Internal | Execute approved plan |

## Identity

| Method | Path | Description |
|---|---|---|
| `POST` | `/users/login` | Email + password → JWT |
| `POST` | `/users` | Create user |
| `GET` | `/users/{id}` | Get user |
| `PATCH` | `/users/{id}` | Update user |
