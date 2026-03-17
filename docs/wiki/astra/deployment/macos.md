---
title: macOS production
tags:
  - astra
  - deployment
  - macos
---

# macOS production

**Apple Silicon** (and Intel) Macs are a **supported** deployment shape for edge or small-scale production — e.g. **Mac Mini / Studio** with **Metal** / **Neural Engine** for inference-heavy workloads.

## Configuration

Backend selection (**Metal**, **ANE**, **CPU**) is controlled via **environment** as described in **PRD §20**. The kernel stays **platform-agnostic**; acceleration applies in **inference / embedding** paths.

## Operations

Services can run under **launchd**, a **process supervisor**, or your org’s standard **macOS server** practice. **Infrastructure** (Postgres, Redis, etc.) may still run in **containers** on the same host.

!!! note
    **Binary build commands, plist paths, and compose files** are **not** published on this wiki — use the **private** repo.
