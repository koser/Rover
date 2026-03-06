# Task: Connectivity Audit

## Goal
Verify that external connections (specifically GitHub) are accessible and that other agents can perform their missions.

## Constraints
- **Scope**: ~/AgentService only.
- **Safety**: Do not delete or modify configuration files.

## Steps
1. [ ] **Analyze**: Check `git ls-remote origin` to confirm that GitHub is reachable from this project.
2. [ ] **Verify**: Read the `logs/GitAgent.log` to see if the `GitAgent` has reported any push failures.
3. [ ] **Report**: Log a `NETWORK_STATUS` or `AGENT_HEALTH` event in `logs/diary.log`.
4. [ ] **Update**: Use the `dashboard-manager` skill to refresh `dashboard.html` with the latest agent activity and status.
5. [ ] **Self-Check**: Confirm your own cycle is running as expected.

## Desired Output
A verification entry in the system diary confirming that GitHub connectivity is healthy.
