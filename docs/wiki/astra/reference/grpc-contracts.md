---
title: gRPC Contracts
tags:
  - astra
  - reference
  - grpc
  - protobuf
---

# gRPC Contracts

Service contracts are defined in **Protobuf** and described in **PRD §10**. **Service-to-service** calls use **mTLS**; definitions and generation steps live **inside the Astra repo** for contributors.

This wiki does **not** list RPC signatures, package paths, or ports.

## Summary

- **Kernel-oriented** APIs cover actors, messages, and stream subscription patterns.  
- **Task-oriented** APIs cover graph creation, scheduling hints, completion, and failure.  
- Other services expose their own gRPC surfaces as documented in the PRD.

## Related

- [Security](../security.md)  
- [API endpoints](api-endpoints.md) — public REST surface  
- **PRD §10** — full contract detail  
