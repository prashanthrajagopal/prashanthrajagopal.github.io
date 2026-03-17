---
title: Getting Started
tags:
  - astra
  - setup
  - getting-started
---

# Getting Started

High-level orientation for **Astra**. Implementation setup, repo layout, and contributor workflows are intentionally **not** documented on this public wiki — they live with the source tree for people who already have access.

## What Astra is

Applications use the **Astra SDK**, which talks to a **small kernel**: actor runtime, task graph, scheduler, messaging, and durable state coordination. Under that sits **Postgres** (source of truth), **Redis** (streams and fast ephemeral state), **Memcached** (LLM-related caching), and **object storage**. Agent and product logic stay **outside** the kernel via documented APIs — see the [architecture overview](../architecture/overview.md) and **PRD §3–5** in the Astra repo.

## If you contribute

1. Read **PRD §1–9** for vision, kernel boundaries, and services.  
2. Read the [Glossary](../glossary.md) and [Architecture overview](../architecture/overview.md).  
3. Follow the **contributor onboarding and tooling** in the private Astra repository (local run, tests, migrations).

## Public API smoke test

If you have a running environment, health and basic flows are described at a high level in **PRD §15** and the [API endpoints](../reference/api-endpoints.md) summary. Exact request bodies and port defaults may change — verify against your deployment.

## Further reading

| Topic | Page |
|-------|------|
| Architecture | [Overview](../architecture/overview.md), [Services](../architecture/services.md) |
| Security | [Security](../security.md) |
| Operations | [Operations](../operations/index.md) |
| Deployment | [Deployment](../deployment/index.md) |
