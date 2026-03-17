---
title: "Runbook: Postgres Outage"
tags:
  - astra
  - operations
  - runbook
  - postgres
  - database
---

# Runbook: Postgres Outage

**Alert:** DB connection errors platform-wide. Services failing to write state.

## Detection

1. Test connectivity by running `psql -c "SELECT 1;"`.
2. Check the Postgres pod or process: run `kubectl get pods -n infrastructure | grep postgres` for Kubernetes, or `pg_isready -h localhost -p 5432` for native deployments.

## Immediate response

**If primary is down:**

1. Promote the read replica by running `pg_ctl promote -D /var/lib/postgresql/data` (for Postgres streaming replication).
2. Switch services to read-only mode while promoting. The `api-gateway` can serve cached reads from Redis during the outage. New writes (goals, task transitions) will fail — this is acceptable for the duration of promotion.
3. Update `POSTGRES_DSN` for all services to point to the promoted replica, then do a rolling restart: use `kubectl set env deployment -n kernel POSTGRES_DSN="postgres://..." --all`, `kubectl set env deployment -n workers POSTGRES_DSN="postgres://..." --all`, and `kubectl set env deployment -n control-plane POSTGRES_DSN="postgres://..." --all`.

**For GCP (Cloud SQL):**

Cloud SQL automatic failover to the HA replica is immediate. Monitor failover status in GCP Console → Cloud SQL → Operations. No manual promotion is needed.

## Verify recovery

1. Confirm the write path is operational: run `psql -c "INSERT INTO events (event_type, actor_id) VALUES ('HealthCheck', uuid_generate_v4()) RETURNING id;"`.
2. Check for missed events during the outage — events are buffered in the `astra:events` Redis stream and can be replayed after recovery.

## Event replay after recovery

During the outage, Redis Streams continued buffering events. After Postgres recovery:

1. Events stream consumers will automatically retry with exponential backoff.
2. Verify no messages are stuck by running `redis-cli XPENDING astra:events astra-consumers - + 100`.
3. If messages are stuck (more than 3 failed attempts), they are in dead-letter and require manual replay.

!!! warning "Data loss risk"
    If the primary failed without replication lag, the replica may be behind. Check `SELECT pg_last_wal_receive_lsn()` on the replica vs the primary's last known LSN. Events in `events` table are the canonical audit trail — if rows are missing, they may need replay from application logs.
