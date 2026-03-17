---
title: API Endpoints
tags:
  - astra
  - reference
  - api
  - rest
---

# API Endpoints

The **API gateway** exposes **REST** (and **WebSocket** for chat). **Internal-only** routes are **not** listed here. Full detail: **PRD** (gateway sections).

**Auth:** most routes require **JWT**; health and login are exceptions. **Rate limits** depend on deployment.

## Authentication

| Pattern | Auth |
|---------|------|
| Health / login | None (login returns token) |
| Everything else | `Authorization: Bearer <JWT>` |

## Agents (examples)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/agents` | Create agent |
| `GET` | `/agents/{id}` | Get agent |
| `PATCH` | `/agents/{id}` | Update profile |
| `GET` | `/agents/{id}/profile` | Profile (cached) |
| Document routes | `/agents/{id}/documents` | Attach / list / remove docs |

## Goals & tasks (examples)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/agents/{id}/goals` | Submit goal |
| `GET` | `/tasks/{id}` | Task state |
| `GET` | `/graphs/{id}` | Task graph |

## Chat

Session and **WebSocket** streaming paths are specified in **PRD** (chat / Phase 10).

## Dashboard

Super-admin **dashboard** and snapshot APIs exist under the gateway; see **PRD** for paths and roles.

## Identity

Login, user CRUD — **PRD** and deployment docs.

!!! note
    **Exact** path lists and internal callbacks are omitted on this wiki.
