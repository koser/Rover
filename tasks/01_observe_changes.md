# Task: Observe Changes

## Goal
Identify any files created, modified, or deleted within the `~/AgentService/` folder since the last cycle and record these events in the system diary.

## Constraints
- **Scope**: ~/AgentService only.
- **Safety**: Do not delete or modify any files except the `logs/diary.log`.

## Steps
1. [x] **Analyze**: List all files in the root, `tasks/`, `skills/`, and `agents/` directories.
2. [x] **Identify**: Compare the current file list and timestamps against the last known state (if available).
3. [x] **Log**: Use the `system-event-logger` skill to record each change as a `FILE_EVENT` in `logs/diary.log`.
4. [x] **Self-Check**: Log your own wake-up cycle as an `AGENT_HEARTBEAT`.

## Desired Output
A series of timestamped entries in `logs/diary.log` representing the current state of the system.
