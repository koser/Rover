# Skill: Slack Notifier

## Description
Provides a standardized interface for agents to send real-time notifications, alerts, and system status updates to a Slack channel.

## Tools / Methods
- `post_to_slack(message, status)`: Sends a formatted message to the Slack channel.
  - `message`: The text to post.
  - `status`: SUCCESS, WARNING, or ERROR (changes the icon/prefix).

## Execution Pattern
1. Verify the SLACK_WEBHOOK_URL is available in `config.env`.
2. Format the payload:
   - `SUCCESS`: "✅ [ROVER] $message"
   - `WARNING`: "⚠️ [ROVER] $message"
   - `ERROR`: "🚨 [ROVER] $message"
3. Use `curl` to send a POST request with the JSON payload to the Slack Webhook URL.
4. Log the result of the post in the system diary.
