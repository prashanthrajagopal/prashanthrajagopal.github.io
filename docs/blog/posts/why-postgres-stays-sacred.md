---
title: Why Postgres stays sacred
date: 2026-03-24
authors:
  - prashanth
categories:
  - Systems
tags:
  - postgres
  - databases
  - astra
  - architecture
draft: false
---

Every few months someone pitches me on replacing Postgres with something else. A document store for "flexibility." A time-series database for "observability." A distributed NewSQL thing for "scale." I listen politely. Then I keep using Postgres. Not because I'm stubborn — because **Postgres is the last place in the stack where I know the data is true**, and I'm not trading that for a benchmark slide.

<!-- more -->

## Source of truth means something

"Source of truth" is one of those phrases that gets nodded at in design reviews and violated in production. Here's what it means in practice: when two systems disagree about the state of the world, **one of them is wrong and you need to know which one.** If your source of truth is a cache, you're guessing. If it's an event log with eventual consistency, you're hoping. If it's Postgres with a transaction that committed, you know.

Astra stores actor state, task graphs, agent metadata, and scheduling records in Postgres. Not because Postgres is fast — it's fast *enough* — but because when an actor restarts after a crash and asks "what was I doing?", the answer needs to be **correct**, not **recent**.

## The consistency tax is worth paying

Yes, writing to Postgres is slower than writing to Redis. Yes, a synchronous commit adds latency. Yes, you can build faster systems by relaxing consistency guarantees. You can also build a house faster by skipping the foundation.

The consistency tax buys you:

- **Transactions that mean what they say.** `BEGIN`, do work, `COMMIT`. If it committed, it happened. If it didn't, it didn't. No "well, it was written to the leader but maybe the replica hasn't seen it yet."
- **Constraints that enforce your model.** Foreign keys, unique constraints, check constraints. The database rejects bad data before your application has to. This is defense in depth that costs you nothing at read time.
- **A recovery story you can explain.** WAL-based replication. Point-in-time recovery. `pg_dump`. These aren't exciting. They're the reason you sleep through the night.

## What doesn't belong in Postgres

I'm not a zealot. Astra uses Redis for caching and pub/sub. Memcached sits in the hot read path. MinIO handles object storage. These aren't compromises — they're correct tool selection. Postgres is sacred for *state that matters*. It's not sacred for ephemeral counters, session caches, or blob storage.

The discipline is knowing which is which. An actor's mailbox contents? Ephemeral — they live in memory (a Go channel) and die with the process. An actor's *registration* — its ID, its type, its owning agent? Sacred. That's Postgres.

Task state transitions are sacred. Task execution logs are less sacred — they could live in an append-only store or object storage and nobody would cry. The gradient from "must survive a datacenter fire" to "nice to have for debugging" is the gradient from Postgres to everything else.

## The "but it doesn't scale" conversation

Postgres scales further than most people think and less far than some people need. For Astra today — a system that's designed for serious workloads but isn't yet running a million agents — Postgres is not the bottleneck. The kernel, the network, the LLM latency — those are the constraints I'm designing around.

When Postgres becomes the bottleneck, the playbook is boring and proven: read replicas, connection pooling (PgBouncer is already in the stack), partitioning, and if you really must, sharding by tenant or agent ID. Citus exists. Postgres-compatible distributed layers exist. The ecosystem has answers.

What I'm not going to do is replace the source of truth preemptively with something that's faster but weaker, and then discover at 3am that two agents think they own the same task because the eventually-consistent store hadn't caught up.

## Sacred doesn't mean untouchable

Calling Postgres sacred doesn't mean I worship the schema or refuse to change it. It means I treat writes to Postgres like I treat commits to main: **intentionally, with the understanding that this is the record.** Schema migrations get reviewed. Data model changes get thought through. The sacred thing isn't the table structure — it's the contract that says *if it's in Postgres, it's real.*

Everything else in the stack is allowed to lie, within tolerance. Caches are lies with TTLs. Replicas are lies with lag. In-memory state is a lie that ends when the process does. Postgres is where the lies stop.

That's why it stays sacred.
