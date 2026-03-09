# Skill: Slack Bridge

## Description
Provides a real-time WebSocket connection to Slack using Socket Mode to listen for mentions of `@Rover`.

## Tools / Methods
- `listen_for_mentions()`: Connects to the Slack RTM API and waits for `@Rover` events.
- `create_task_from_message(user_id, text)`: Translates a Slack message into a new `.md` task file in `~/AgentService/tasks/`.

## Execution Pattern
1. Verify the SLACK_APP_TOKEN and SLACK_BOT_TOKEN are available in `config.env`.
2. Initialize the Slack Bolt framework and listen for the `app_mention` event.
3. **Instant Commands**: 
   - If the text is exactly "ping!", immediately use the `slack-notifier` skill to reply: "pong! 🏓 The current system time is [Timestamp]."
4. **Task Delegation**:
   - For all other text, generate a unique filename: `tasks/slack_[timestamp].md`.
   - Write a new Markdown task file.
5. Log the interaction in the system diary.
