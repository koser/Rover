# Task: Agent Scheduler

## Goal
Manage the 24-hour execution cycle for support agents (Diary, GitAgent, SystemCheckup).

## Current Schedule Status
Check `logs/agent_schedule.json` for the last run timestamps.

## Constraints
- **Diary Agent**: Run once every 24 hours.
- **GitAgent (Local Versioning)**: Run frequently (every 1-2 hours) for local commits.
- **GitAgent (GitHub Backup)**: Run exactly once every 24 hours.
- **SystemCheckup Agent**: Run once every 24 hours.

## Steps
1. [ ] **Analyze**: Read `logs/agent_schedule.json`.
2. [ ] **Calculate (Diary/Checkup)**: If 24h passed, trigger `run_agent.sh` for Diary and SystemCheckup with the `--once` flag.
3. [ ] **Calculate (GitAgent)**:
    - **Local**: Trigger `GitAgent` every 1-2 hours for `atomic_commit` operations.
    - **Backup**: Trigger `GitAgent` to check the 24h `GitAgent_push` threshold.
4. [ ] **Execute**: Run the agents as required.
5. [ ] **Update Schedule**: Record new `last_run` or `GitAgent_push` timestamps.
6. [ ] **Log**: Update the system diary.

## Desired Output
A strictly controlled repository and system state that balances local frequency with remote efficiency.
