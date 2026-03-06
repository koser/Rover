# Skill: Git Manager

## Description
Provides a standardized interface for performing Git operations (commit, push, status) within the `~/AgentService` directory.

## Strategy: Atomic-Batch
- **Local Commits**: Perform an `atomic_commit` immediately after any file modification in `~/AgentService`.
- **Remote Pushes**: Perform a `push_to_remote` only when:
    - 30 minutes have elapsed since the last push.
    - OR more than 5 local commits are pending.
    - OR the user explicitly requests a sync.

## Tools / Methods
- `atomic_commit(message)`: `git add .` and `git commit -m "[AGENT_NAME] $message"`.
- `smart_push()`: Checks commit count (`git rev-list --count origin/main..main`). If > 5 or time threshold met, execute `git push origin main`.

## Execution Pattern
1. Verify if there are any uncommitted changes (`git status --porcelain`).
2. If changes exist, execute `git add .` and `git commit -m "[AGENT_NAME] $message"`.
3. If a remote `origin` is configured, execute `git push origin main`.
4. Log the result of the operation in the system diary.
