---
title: macOS Production Deployment
tags:
  - astra
  - deployment
  - macos
  - apple-silicon
  - metal
---

# macOS Production Deployment

macOS is a supported production deployment target. Not "works on your laptop" supported — actually production-ready, with Metal/Neural Engine acceleration for inference and embedding workloads.

This is the deployment for dedicated Mac Mini or Mac Studio hardware used as edge inference nodes or small-scale production environments where Apple Silicon's performance-per-watt matters.

## Why macOS in production?

- **Apple Silicon (M-series)** provides Metal GPU and Neural Engine (ANE) for inference and embedding — competitive with NVIDIA GPU performance at a fraction of the power
- **Mac Mini / Mac Studio** are dense, quiet, power-efficient servers for on-prem deployment
- **Native binaries** — no emulation, no JVM overhead, no container startup penalty

## Hardware acceleration config

Set the following environment variables to control backend selection:

- `ASTRA_USE_METAL=true` to enable Metal (Apple GPU) for inference and embeddings
- `ASTRA_USE_ANE=true` to enable Neural Engine when available via Core ML
- `ASTRA_USE_CUDA=false` to disable CUDA (Linux-only)

Backend selection happens at runtime (`runtime.GOOS == "darwin"`) or via build tags. The fallback chain is: Metal → ANE → CPU. If `ASTRA_USE_METAL=false`, the system falls straight to CPU.

The active backend is logged at startup and exposed in metrics (`inference_backend=metal|ane|cpu`). If you expect Metal to be active and see `cpu`, the detection path failed.

## Deployment approach

macOS doesn't have `systemd`. Two options:

**launchd** (recommended for production): Create a plist file at `~/Library/LaunchAgents/com.astra.<service-name>.plist` for each service. Each plist defines the service label, the path to the binary under `ProgramArguments`, required environment variables (including `POSTGRES_DSN`) under `EnvironmentVariables`, and sets both `RunAtLoad` and `KeepAlive` to true so the service starts on login and restarts automatically on crash. See `deploy/macos/` in the Astra repo.

**Process manager (Supervisor or similar)** for simpler management.

## Infrastructure on macOS

Docker Desktop for Mac handles Postgres, Redis, Memcached, and MinIO via docker-compose. Same compose file as local dev. No k8s needed unless you're running multiple Macs as a cluster.

## Native binary builds

Build for Apple Silicon with `GOOS=darwin GOARCH=arm64 go build -o bin/darwin-arm64/ ./cmd/...`. Build for Intel Mac with `GOOS=darwin GOARCH=amd64 go build -o bin/darwin-amd64/ ./cmd/...`. CI should produce both; deploy the right architecture for the hardware.

!!! note
    No macOS-specific APIs (Metal, ANE) are called in the kernel. The acceleration APIs are used only in the inference and embedding pipelines (connected via backend interfaces). The kernel stays platform-agnostic.
