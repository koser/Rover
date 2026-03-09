# Task: Listen for Mentions

## Goal
Maintain a persistent WebSocket connection to Slack using Socket Mode and listen for any mentions of @Rover.

## Constraints
- **Scope**: ~/AgentService only.
- **Safety**: Do not delete any files. Only create new task files in the `tasks/` directory.

## Steps
1. [x] **Analyze**: Verify SLACK_APP_TOKEN and SLACK_BOT_TOKEN are available in `config.env`.
2. [x] **Listen**: Use the `slack-bridge` skill to initiate a WebSocket connection to Slack.
3. [x] **Handle**: When a mention is received, create a new task file in `tasks/slack_[timestamp].md` with the user's instruction.
4. [x] **Confirm**: Post a confirmation message back to Slack acknowledging the new task.
5. [x] **Log**: Update the system diary with the task creation details.

## Desired Output
A real-time listener that translates Slack mentions into actionable task files in the `tasks/` directory.
