---
title: The 10ms lie we all tell
date: 2026-03-24
description: That cache hit on the whiteboard is measuring the wrong thing. Cache discipline is architecture discipline — every cache is a bet, and we only count the wins.
authors:
  - prashanth
categories:
  - Architecture
tags:
  - caching
  - latency
  - astra
draft: false
---

Every architecture review I've sat through has a box labelled "cache" with an arrow that says something like "< 1ms." It's the most trusted line on the whiteboard and the least questioned number in the system. We all nod. We all move on. And then production teaches us what we should have asked: **cached *what*, for *whom*, checked *when*?**

<!-- more -->

## The lie is in the defaults

Nobody sets out to build a slow cache layer. The lie creeps in because caching feels solved — you drop Redis or Memcached in front of something expensive and declare victory. The problem is that "in front of" is doing load-bearing work in that sentence. What you're really saying is: "I've added a new consistency boundary to my system, and I'm going to pretend it doesn't exist."

The moment you cache, you've made a bet: **the data won't change in a way that matters before the TTL expires.** That bet is correct often enough to be dangerous. It's wrong just often enough to ruin an on-call rotation.

## Cache discipline is architecture discipline

In Astra, caching isn't an afterthought bolted onto the read path — it's a decision that lives inside the same design conversation as the data model. The questions I force myself to answer before anything gets a TTL:

- **Who reads this, and how stale can they tolerate?** An actor looking up its own state has different freshness needs than a dashboard rendering aggregate counts.
- **What invalidates this, and who knows?** If the answer is "a write to Postgres that happens in a different service," congratulations — you've built a distributed cache invalidation problem. The two hardest things in computer science aren't a joke; they're a warning.
- **What happens when the cache is wrong?** Not "how do we fix it" — what does the *user* experience? If a stale actor registry means messages route to a dead actor, that's not a cache miss. That's an outage with a caching costume on.

## The hot path religion, continued

I wrote about the kernel's first 10ms before — lookup, enqueue, done. Caching fits into that story, but only if you're honest about what it costs. A cache hit on the actor registry? Legitimate speedup. A cache hit on task state that was written 400ms ago by a different node? That's not a speedup. That's a time machine pointed in the wrong direction.

The rule I've landed on: **cache the structure, not the state.** The shape of the actor graph changes slowly. The contents of a mailbox change constantly. One of those belongs in a cache. The other belongs in the source of truth, queried honestly.

## TTLs are not a strategy

A TTL is a confession that you don't know when the data changes. Sometimes that's fine — truly static config, feature flags that update once a quarter, reference data that an intern updates on Tuesdays. For those, set a TTL and stop thinking about it.

For everything else, a TTL is a prayer. "Please let nothing important change in the next 30 seconds." Production answers prayers with incidents.

The alternative is event-driven invalidation, which is harder and uglier and makes your architecture diagrams look like a bowl of spaghetti. It's also correct. You don't have to like it. You have to decide whether you'd rather debug stale data at 3am or draw a messy diagram at 3pm.

## The 10ms that isn't

Here's the thing about that "< 1ms" on the whiteboard: it's measuring the wrong thing. Yes, the Redis `GET` took 0.8ms. But the decision to trust that value — to skip the database, to serve a response built on a foundation of "probably still true" — that decision has a cost measured in incidents, not milliseconds.

I'm not anti-cache. I cache aggressively in Astra where the contract is clear. But I've stopped pretending that adding a cache is free. Every cache is a bet. The 10ms lie is that we only count the wins.

The honest version: caching makes your system faster *and* less correct, and your job is to decide how much of each you can afford.
