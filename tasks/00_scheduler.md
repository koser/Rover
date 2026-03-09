# Task: Agent Scheduler

## Goal
Manage the 24-hour execution cycle for support agents (Diary, GitAgent, SystemCheckup).

## Current Schedule Status
Check `logs/agent_schedule.json` for the last run timestamps.

## Constraints
- **Diary Agent**: Run once every 24 hours.
- **GitAgent**: Run once every 24 hours.
- **SystemCheckup Agent**: Run once every 24 hours.
- **SlackBridge**: Stays real-time (handled by StartRover.sh).

## Steps
1. [ ] **Analyze**: Read `logs/agent_schedule.json`. If it doesn't exist, assume all agents need to run.
2. [ ] **Calculate**: For each support agent, check if more than 24 hours (86,400 seconds) have passed since the `last_run`.
3. [ ] **Execute**: If 24 hours have passed, use the `run_agent.sh` tool with the `--once` flag to trigger the agent's task.
4. [ ] **Update**: After successful execution, update the `last_run` timestamp for that agent in `logs/agent_schedule.json`.
5. [ ] **Log**: Record the scheduling check and any triggered executions in the system diary.

## Desired Output
A strictly controlled 24-hour cycle for high-API-usage agents, managed autonomously by Rover.
