---
title: macOS production
tags:
  - astra
  - deployment
  - macos
---

# macOS production

**Apple Silicon** (and Intel) Macs are a **supported** deployment shape for edge or small-scale production — e.g. **Mac Mini / Studio** with **Metal** / **Neural Engine** for inference-heavy workloads.

## Hardware acceleration

| Backend | When used | Config |
|---------|-----------|--------|
| **Metal** | GPU-accelerated inference, embeddings, compute-heavy paths | `ASTRA_USE_METAL=true` |
| **Neural Engine (ANE)** | When exposed via Core ML or stable framework APIs | Detected automatically; explicit fallback to Metal or CPU |
| **CPU** | Default fallback when accelerators unavailable or disabled | Always available |

Detection via `runtime.GOOS == "darwin"` or build tags. Backend selection is explicit; fallback always to a working path. `ASTRA_USE_CUDA` is ignored on macOS.

Native binaries built for `darwin/arm64` and `darwin/amd64` — no emulation on Apple Silicon.

## Operations

Services can run under **launchd**, a **process supervisor**, or your org’s standard **macOS server** practice. **Infrastructure** (Postgres, Redis, etc.) may still run in **containers** on the same host.

!!! note
    **Binary build commands, plist paths, and compose files** are **not** published on this wiki — use the **private** repo.
