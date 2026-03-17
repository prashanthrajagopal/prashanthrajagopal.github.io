---
title: The kernel's first 10ms
date: 2026-03-19
authors:
  - prashanth
categories:
  - Astra
tags:
  - astra
  - go
  - kernel
draft: false
---

People love quoting p99s on a slide. Fewer people can tell you what actually runs in the millisecond *before* that number even becomes possible. In Astra, the kernel is the choke point for everything that moves: actors, messages, later tasks and streams. This post is about the slice of time between "the process is alive" and "an actor has a message in its hands" — not because I've benchmarked it to four decimal places today, but because **what you allow into that window** decides whether the rest of the system is allowed to be fast.

<!-- more -->

## Cold start vs the path that matters

Boot is honest work: parse config, open Postgres, maybe shake hands with Redis, bind gRPC. That can be tens or hundreds of milliseconds and nobody should pretend otherwise. The interesting budget is **steady state**: a client already connected, an actor already registered, someone calls something that ends with `Receive` on a running goroutine.

That's the path I'm designing like a miser's ledger. Not every RPC deserves that treatment — `SpawnActor` might touch the database to persist an agent row; fine. But **`SendMessage` to an existing actor** should not secretly become a tour of your infrastructure. Lookup, enqueue, return. If you're blocking on a planner, a cache fill, or a "quick" consistency check inside that path, you've already lost the game — you just haven't measured it yet.

## What the kernel actually does (conceptually)

At the core it's boring in a good way: a registry (`map` + lock), a bunch of actors, each with a **buffered mailbox** (channel, in the Go implementation). Spawn registers the actor and starts its loop. Send does a read lock, finds the target, hands the message to the mailbox — non-blocking if the buffer is full, which is a deliberate backpressure signal, not an accident.

No drama. No allocation festival per message if you can help it. The handler goroutine wakes up, runs your `Receive`, and the world moves on.

The **first** message after spawn is special only emotionally. Technically it's the same hot path: the actor is in the map, the channel has capacity, the write succeeds. If the first message is slow, the Nth will be slow for the same reason.

## What I keep out of that path

- **Postgres on Send** — state changes belong elsewhere or on explicit transitions, not on every envelope delivery.
- **Hidden sync over the network** — if delivering a message waits on another service, you've built a distributed monolith with a kernel-shaped hat.
- **Unbounded work in the handler** — the kernel gives you a thread of execution; what you do inside `Receive` is your funeral. The kernel's job is to get you the message cheaply; not to save you from a 30s LLM call blocking the mailbox.

The PRD says uncomfortable things about API reads (Redis/Memcached, not Postgres on the hot path). Same religion: **the hot path is a place of worship; only cheap operations get to enter.**

## Why 10ms is a cultural number, not just a target

Ten milliseconds is roughly the threshold where humans stop perceiving something as instant. It's also a good club to beat feature creep with. "Can we add a policy check here?" Maybe — but not *here*. Wrong layer. That's how you keep an OS-shaped thing from growing barnacles until it behaves like a Spring app that happened to be written in Go.

I'm not claiming every deployment hits single-digit milliseconds on day one. I *am* claiming that if you don't carve that path early, you never will — you'll optimize around the barnacles until retirement.

## Bottom line

The kernel's first 10ms — really, every **Send** on a live actor — should be **lookup, enqueue, done**. Boot can be slow. Planning can be slow. The world can be slow. But the moment you decide "this message has arrived," that decision had better be almost free.

Everything else is commentary. Possibly Ruby-flavoured commentary elsewhere. Not in the mailbox path.
