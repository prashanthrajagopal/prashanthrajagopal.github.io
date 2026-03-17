---
title: Message Types
tags:
  - astra
  - reference
  - messaging
  - events
---

# Message Types

Messages carry **type**, **source**, **target**, **payload**, and **metadata** (e.g. trace correlation). **PRD §12** defines categories and payloads in full.

## Event bus vs streams

**Durable audit** for many lifecycle events lives in the **database event log**. **Redis streams** carry **operational** traffic: dispatch, worker signals, async usage recording. Encoding (JSON vs binary) is an implementation detail.

**Partitioning:** dispatch traffic is **sharded** so no single stream becomes the only scalability bottleneck.

## Categories (high level)

| Area | Examples |
|------|----------|
| Goal / plan | Goal created, plan generated |
| Task | Scheduled, started, completed, failed |
| Worker | Heartbeat, register |
| LLM | Usage / cost audit (async path) |

!!! note
    **Exact type names and JSON shapes** are in the PRD — not listed here.
