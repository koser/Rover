# Skill: Dashboard Manager

## Description
Maintains a `dashboard.html` file in the root of `~/AgentService` to provide a visual status of all agents, tasks, and system health.

## Tools / Methods
- `update_dashboard(agent_data, task_data, system_health)`: Generates a new `dashboard.html` with the latest status.
- `refresh_status()`: Scans `logs/`, `agents/`, and `tasks/` to gather metrics.

## Execution Pattern
1. Read the current list of agents from `agents/*.config`.
2. For each agent, check its `logs/*.log` for the "Cycle Start" timestamp to calculate "Last Seen".
3. **Git Metrics**:
    - Get the last local commit time: `git log -1 --format=%cd`.
    - Get the last push to GitHub time: Check the timestamp of the last "Push SUCCESS" in `logs/diary.log` or check `git log -1 origin/main --format=%cd`.
4. Read the `logs/diary.log` for the latest events.
5. Generate a clean, responsive HTML structure with:
    - **Agent Cards**: Status (Active/Idle), Last Seen, Current Mission.
    - **Backup Status**: Last Local Commit, Last GitHub Push.
    - **System Health**: Connection status, Git sync status.
    - **Latest Diary Entries**: Last 5 events.
6. Save the result to `~/AgentService/dashboard.html`.
