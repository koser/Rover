# Skill: System Event Logger

## Description
Provides a standardized interface for agents to record events, changes, and system status to the central repository log.

## Tools / Methods
- `log_event(event_type, description, status)`: Appends a timestamped entry to `~/AgentService/logs/diary.log`.
  - `event_type`: (e.g., CONFIG_CHANGE, AGENT_START, USER_REQUEST)
  - `description`: Detailed text of the event.
  - `status`: SUCCESS, WARNING, or ERROR.

## Execution Pattern
1. Validate the log file exists; create if missing.
2. Format: `[YYYY-MM-DD HH:MM:SS] [AGENT_NAME] [EVENT_TYPE] [STATUS]: DESCRIPTION`
3. Append to the end of `~/AgentService/logs/diary.log`.
4. **Alerting**: If the `status` is `ERROR` or `WARNING`, also append the formatted entry to `~/AgentService/logs/ALERTS.log`.
