#!/bin/bash
source "$HOME/AgentService/config.env"

# Fetch recent mentions using the Conversations History API
# Note: This requires the 'channels:history' and 'groups:history' scopes on your bot token.
# If those aren't set, this will fail.

LATEST_TIMESTAMP=$(cat .slack_last_ts 2>/dev/null || echo "0")

RESPONSE=$(curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
     "https://slack.com/api/conversations.history?channel=C07P88H6N4V&oldest=$LATEST_TIMESTAMP")

# Parse the response for mentions of @Rover (using simple grep for now)
if echo "$RESPONSE" | grep -q "ping!"; then
    echo "Ping detected! Sending pong..."
    curl -s -X POST -H 'Content-type: application/json' \
         --data "{\"text\":\"pong! 🏓 The current system time is $(date).\"}" \
         "$SLACK_WEBHOOK_URL"
fi

# Update the last seen timestamp
echo "$RESPONSE" | grep -o "\"ts\":\"[^\"]*\"" | head -1 | cut -d'"' -f4 > .slack_last_ts
