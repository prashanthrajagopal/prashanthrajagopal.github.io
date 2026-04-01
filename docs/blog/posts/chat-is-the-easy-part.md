---
title: Chat is the easy part
date: 2026-03-20
description: What it actually took to bolt WebSocket streaming onto Astra — and why the session model matters more than the protocol.
authors:
  - prashanth
categories:
  - Astra
tags:
  - astra
  - chat
  - websocket
  - architecture
draft: false
---

Everyone thinks chat is a solved problem. You slap a WebSocket on a language model, stream tokens to the browser, ship it. The demo writes itself. What nobody tells you is that demo assumes the rest of your system is also a chat interface — a stateless request-response loop that apologizes to no prior architecture. **Astra is not that.** Astra thinks in DAGs, not turns, and making chat fit into that without either breaking the DAG semantics or building a second system was the interesting part.

<!-- more -->

## The session model is load-bearing

The first instinct was a dedicated chat service. A little microservice, pure WebSocket, no coordination with the rest of the agent runtime. Isolated, clean, easy to reason about. Also wrong.

The whole point of chat in Astra is that a conversational exchange should be able to do *everything* a goal-based agent can do — call tools, trigger sub-goals, emit task graph nodes — and that means it can't be a sidecar that makes HTTP calls over to the real system. It has to be part of the real system. So the chat surface stayed in the api-gateway, and the session model became the thing that bridges the two worlds.

A session in Astra has a user and an agent. You create it via REST — `POST /chat/sessions` — which gives you back a session ID and sets up the context: the agent's rules, its skills, its memory profile. That's the REST half. Then you upgrade to WebSocket at `/chat/ws?session_id=...` and the streaming begins. **The session is the contract.** The WebSocket is just the transport.

This matters because session scope is where you enforce the resource limits that would otherwise be non-obvious in a streaming context. `CHAT_RATE_LIMIT` — messages per minute, per session. `CHAT_TOKEN_CAP` — cumulative tokens before the session expires or throttles. `CHAT_MAX_MSG_LENGTH` — reject the message before it hits the model. These toggles live in config alongside `CHAT_ENABLED`, which is the kill switch. None of this is novel, but all of it is easier to reason about when the session is a first-class object rather than a bolt-on.

## JSON frames over raw tokens

Streaming raw token bytes is fine for a toy. For a system where a single message might trigger tool calls, kick off sub-agents, or produce structured data in the middle of a response, you need something with more semantic weight. Astra's WebSocket protocol uses typed JSON frames:

- `chunk` — a token or small string fragment from the model
- `message_start` / `message_end` — envelope delimiters for a complete message
- `tool_call` — the agent is invoking a tool; here's the name and input
- `tool_result` — here's what came back
- `done` — the turn is over, session is waiting
- `error` — something broke; here's the code and message

The client knows at every point whether it's rendering a streaming response, watching a tool execute, or waiting for the agent to plan its next move. This is not complicated to implement — it's just a discriminated union and a `type` field — but it makes the difference between a chat interface that feels like a terminal and one that can show progress, tool activity, and partial results without guessing.

## Chat agents are just agents

The detail that makes this work architecturally: **chat agents reuse the same workers and tool runtime as goal-based agents.** There's no separate chat execution path. When a chat session triggers a tool call, that call goes through the same sandboxed tool runtime, the same permission model, the same observability hooks as a tool call from a planned task. The planner that handles multi-step goals is the same planner the chat agent can invoke when a conversational request turns into something that needs a task graph.

This was the design constraint that prevented the "separate chat service" temptation. Once you decide that chat is just a different *entry point* into the same agent runtime — not a different runtime — the architecture simplifies. The session creates a context, the context gets handed to the planner, the planner produces work, the workers execute it, the results stream back through the WebSocket. The DAG semantics don't change; they just get triggered conversationally instead of programmatically.

## Injection for non-chat surfaces

One thing a pure WebSocket model doesn't handle well: inbound messages from surfaces that aren't the chat UI. Slack sends a webhook. An email arrives. A cron job wants to post a message into a running session. For these, there's `POST /chat/sessions/{id}/inject` — it drops a synthetic user message into the session and the agent processes it as if it had come over the wire. The response goes wherever the session is configured to deliver: back over the WebSocket if it's open, or buffered for next connect if it isn't.

This keeps the session model intact across surfaces without each surface needing to know about WebSocket lifecycle. Slack connects once to configure the webhook, then fires `inject` on every message. The agent doesn't know or care that this particular user message came from a chat UI versus a Slack mention.

## The hard part wasn't the protocol

WebSocket framing, JSON serialization, token streaming — none of that is hard. The hard part was making a fundamentally conversational interaction pattern — a user says something, the agent responds — coexist with a system whose core abstraction is a directed acyclic graph of tasks. Turns feel sequential; DAGs are parallel. Turns have an obvious state machine (waiting, processing, responding); DAGs have phases, dependencies, and fan-out.

The answer, in the end, was to treat chat not as a special case but as a degenerate case: a task graph where the user is the trigger for every phase. **The session is the persistent state; the DAG is what happens inside a turn.** Once that framing clicked, the rest was plumbing.

The hardest thing to build is almost never the thing that looked hard at the start.
