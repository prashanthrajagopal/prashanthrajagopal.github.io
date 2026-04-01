---
title: Agent memory is not a vector database
date: 2026-03-13
description: Working memory, episodic memory, and semantic search are three different things. pgvector is one layer, not the whole story.
authors:
  - prashanth
categories:
  - Astra
tags:
  - astra
  - memory
  - pgvector
  - architecture
draft: false
---

The default move in agent frameworks right now is to throw everything into an embedding database and call it memory. You chunk your documents, embed them, stash them in a vector store, and at inference time you do cosine similarity to retrieve "relevant context." This is semantic search. It is useful. It is also one small piece of what memory means for a running agent, and if it's the only piece you have, **your agent has amnesia with a search engine.**

<!-- more -->

## Three things, not one

Astra breaks agent memory into three tiers, each with different semantics, different backing stores, and different failure modes:

1. **Working memory** — what the agent knows right now, during this execution. Ephemeral. Lives in Redis hashes with short TTLs. Dies when the actor does.
2. **Episodic memory** — what happened, in order. Durable, time-ordered, queryable as a timeline. Lives in Postgres.
3. **Semantic memory** — what's *similar* to something. Embedding-backed, fuzzy, lives in Postgres via pgvector.

These aren't three names for the same idea. They answer different questions. Working memory answers "what's in scope right now?" Episodic memory answers "what did this agent do, and when?" Semantic memory answers "what's related to this concept?" Conflating them produces systems that can find the nearest neighbor to a query but can't reconstruct a sequence of events or access state that was explicitly set ten seconds ago.

## Working memory is a scratchpad, not a store

An agent executing a multi-step goal needs somewhere to put intermediate state: the output of step three that step five depends on, the decision branch that was taken two phases back, the accumulated evidence that the current hypothesis is wrong. That's working memory. It needs to be fast — sub-millisecond reads — and it needs to be scoped to the execution, not the agent's lifetime.

Redis hashes with a short TTL handle this cleanly. The key is the actor ID. The value is a structured map of whatever the agent is tracking. When the execution ends — success, failure, timeout — the TTL expires and the scratchpad disappears. No cleanup, no tombstoning, no orphaned records to vacuum.

**The TTL is not a bug.** If working memory survives past the execution that created it, it isn't working memory anymore — it's a cache that needs invalidation logic, and you've invented a new problem for yourself.

## Episodic memory is the timeline

A goal-based agent runs phases. Phases produce outcomes. Outcomes get written to the `phase_summaries` table in Postgres: what phase, what agent, what happened, when, what the output was. This is episodic memory — structured, durable, time-ordered.

It matters for two reasons. First, recovery: if an agent restarts mid-goal, it can reconstruct where it was from the episodic record. Working memory is gone; the timeline is not. Second, reflection: an agent that can look at its own history can do things like detect that it's running in circles, notice that a particular approach always fails in this context, or summarize what it accomplished in phase one before starting phase three.

The `phase_summaries` table has a pgvector column. That's the bridge to semantic memory — **not so that you can search summaries by topic, but so that a new goal can ask "have I done something like this before?"** The embedding is over the phase summary text. The similarity search is over the agent's own history. This is meaningfully different from searching an external knowledge base, and collapsing them into the same abstraction loses that distinction.

## Semantic memory is where pgvector lives

The `agent_documents` table is structured context — rules the agent operates under, skills it can call, reference documents it was initialized with. These aren't embeddings. They're typed rows: `rules`, `skills`, `context_docs`, `references`. The planner reads them directly, by type, at goal initialization. No cosine similarity needed to decide which rules apply — they all apply.

pgvector comes in for `context_docs` and `references` — the unstructured knowledge that the agent might need to retrieve selectively. An agent initialized with a large codebase reference, or a sprawling policy document, doesn't want all of that in every system prompt. It retrieves the chunks that are relevant to the current task. That's semantic memory: **a retrieval mechanism over things the agent might need to know, not a replacement for things the agent definitively knows.**

The distinction matters at query time. Rules and skills are fetched with `WHERE agent_id = ? AND doc_type = ?`. Context docs are fetched with a vector similarity search. Same table, different retrieval paths, because the semantics are different.

## How context flows

Goal initialization in Astra assembles the system prompt from these pieces: base rules from `agent_documents`, skills, and context retrieved from semantic search given the goal description. The planner receives that assembled context and embeds it into the task payloads it creates. Workers execute with access to the task payload — they don't query memory mid-execution; the context was baked in at planning time.

This is an intentional constraint. Workers that reach back into memory during execution are harder to reason about, harder to replay, and introduce a class of race conditions where the context changes between when the plan was made and when the work runs. **Seal the context at plan time; execute deterministically.** If the context turns out to be wrong, that's a signal to the episodic record — the phase fails, the planner gets to try again with updated retrieval.

## What you lose with just a vector store

If your agent's memory is a single vector database, here's what you don't have:

- **Scoped transient state.** Every scratchpad entry becomes a retrieval problem. You can't set a value and get it back with a key lookup — you have to embed the query and hope the nearest neighbor is what you set.
- **Ordered history.** Cosine similarity has no notion of time. "What did the agent do last?" is not a question a vector store answers well.
- **Typed structured context.** Rules are not the same as reference documents. Skills are not the same as episodic summaries. Flattening them into one embedding space makes the retrieval system do work that a schema would handle for free.

None of this is a critique of pgvector specifically — pgvector is the right call for the semantic layer, and running it inside Postgres means it shares the transaction model and durability guarantees of the rest of Astra's state. The critique is of treating it as the whole answer.

Memory is a spectrum from "what am I holding right now" to "what is vaguely related to this concept." Vector search lives at one end. An agent needs the whole thing.
