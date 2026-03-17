---
title: GCP Deployment
tags:
  - astra
  - deployment
  - gcp
---

# GCP deployment

Production on **GCP** typically uses **GKE** plus **managed** Postgres, Redis, and related services. **Helm values**, **scripts**, and **environment templates** live **only in the Astra repo**.

## Themes

- **Private networking** between workloads and data stores.  
- **Secrets** via **Vault** or cloud secret managers — not in git.  
- **Scaling** per **PRD §20**.

See also [Kubernetes / Helm](kubernetes.md) for namespace layout at a high level.
