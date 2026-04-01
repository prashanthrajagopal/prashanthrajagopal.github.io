---
title: API Endpoints
tags:
  - astra
  - reference
  - api
  - rest
---

# API Endpoints

The **API gateway** exposes **REST** (and **WebSocket** for chat). **Internal-only** routes are marked accordingly. Full detail: **PRD** (gateway sections).

**Auth:** most routes require **JWT**; health and login are exceptions. **Rate limits** depend on deployment.

## Authentication

| Pattern | Auth |
|---------|------|
| Health / login | None (login returns token) |
| Everything else | `Authorization: Bearer <JWT>` |

## Identity

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/users/login` | Login with email + password; returns JWT |
| `POST` | `/users` | Create user |
| `GET` | `/users` | List users |
| `GET` | `/users/{id}` | Get user |
| `PATCH` | `/users/{id}` | Update user |

## Agents

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/agents` | Create agent |
| `GET` | `/agents/{id}` | Get agent |
| `PATCH` | `/agents/{id}` | Update agent profile (`system_prompt`, `config`) |
| `GET` | `/agents/{id}/profile` | Get profile — Redis cached, 5 min TTL |

### Agent documents

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/agents/{id}/documents` | Attach document (`rule` / `skill` / `context_doc` / `reference`) |
| `GET` | `/agents/{id}/documents` | List documents; optional `?doc_type=` filter |
| `DELETE` | `/agents/{id}/documents/{doc_id}` | Remove document |

## Goals & tasks

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/agents/{id}/goals` | Submit goal |
| `GET` | `/tasks/{id}` | Task state |
| `GET` | `/graphs/{id}` | Task graph |

## Chat (Phase 10)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/chat/sessions` | Create session (`agent_id`, `title`) |
| `GET` | `/chat/sessions` | List sessions for authenticated user |
| `GET` | `/chat/sessions/{id}` | Session details |
| `GET` | `/chat/ws` | WebSocket upgrade for streaming |
| `POST` | `/chat/sessions/{id}/inject` | External message injection into session |

## Approvals

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/approvals/{id}/decide` | Submit approval decision; supports dual-approval |

## Slack

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/webhooks/{source_id}` | Webhook ingest with HMAC-SHA256 verification |
| `POST` | `/internal/slack/post` | Proactive Slack posting — **internal**, requires `X-Slack-Internal-Secret` |

## Internal / Olympus

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/internal/goals` | Agent-to-agent goal posting with rate limiting |
| `POST` | `/internal/apply-plan` | Called by access-control to apply an approved plan (goal-service) |

## Dashboard (super-admin)

| Path | Description |
|------|-------------|
| `/superadmin/dashboard/` | Platform dashboard UI |
| `/superadmin/api/dashboard/snapshot` | Summary snapshot |
| `/superadmin/api/dashboard/approvals` | Pending approvals |
| `/superadmin/api/dashboard/goals` | Goal list |
| `/superadmin/api/dashboard/tasks` | Task list |
| `/superadmin/api/dashboard/agents` | Agent list |
| `/superadmin/api/dashboard/chat` | Chat sessions |
| `/superadmin/api/dashboard/slack` | Slack config |
| `/superadmin/api/slack/*` | Slack app configuration |

!!! note
    All `/superadmin/api/*` routes enforce super-admin role and apply `redactForSuperAdmin()` to response payloads.
