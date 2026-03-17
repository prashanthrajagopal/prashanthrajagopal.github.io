---
title: gRPC Contracts
tags:
  - astra
  - reference
  - grpc
  - protobuf
---

# gRPC Contracts

Protobuf definitions live in `/proto/`. Generated Go stubs are in `proto/kernel/` and `proto/tasks/` (via `buf generate`).

## kernel.proto — `astra.kernel.KernelService`

`KernelService` (package `astra.kernel`) exposes five RPCs: `SpawnActor` (takes actor type and config bytes, returns an actor ID), `SendMessage` (takes target actor ID, message type, source, and payload bytes; returns empty), `QueryState` (takes entity type string and a string map of filters; returns a list of serialized result bytes), `SubscribeStream` (takes stream name, consumer group, and consumer ID; returns a server-streaming `Event`), and `PublishEvent` (takes stream name, event type, actor ID, and payload bytes; returns an event ID string).

The `Event` message carries an ID, type, actor ID, payload bytes, and a Unix timestamp.

Server: `cmd/agent-service`, port `AGENT_GRPC_PORT` (default 9091). See `proto/kernel.proto` in the Astra repo.

## task.proto — `astra.tasks.TaskService`

`TaskService` (package `astra.tasks`) exposes six RPCs: `CreateTask` (takes graph ID, agent ID, task type, payload bytes, priority, and a list of dependency task IDs; returns a task ID), `ScheduleTask` (takes a task ID; returns empty), `CompleteTask` (takes task ID and result bytes; returns empty), `FailTask` (takes task ID and error string; returns empty), `GetTask` (takes task ID; returns full task details including ID, graph ID, agent ID, type, status, payload, result, priority, retries, and timestamps), and `GetGraph` (takes graph ID; returns all tasks in the graph along with their dependency edges as `TaskDependency` messages).

Server: `cmd/task-service`, port `TASK_GRPC_PORT` (default 9090). See `proto/task.proto` in the Astra repo.

## Generating stubs

Run `buf generate` from the repo root to regenerate Go stubs. Configuration is in `buf.yaml` and `buf.gen.yaml`. Output is written to `proto/kernel/*.pb.go` and `proto/tasks/*.pb.go`.
