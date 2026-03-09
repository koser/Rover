#!/bin/bash

# StartRover.sh - Supervised Launcher for AgentService
# This script stays in the foreground and kills all agents when it exits.

echo "--- Starting AgentService in Supervised Mode ---"

# Array to keep track of PIDs
AGENT_PIDS=()

# Cleanup function
cleanup() {
    echo ""
    echo "--- Shutting down AgentService ---"
    for PID in "${AGENT_PIDS[@]}"; do
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID"
        fi
    done
    exit 0
}

# Trap exit signals (including closing the terminal)
trap cleanup SIGINT SIGTERM SIGHUP EXIT

# 1. Launch SlackBridge (Real-time listener)
# This MUST stay running to hear your Slack commands.
./run_agent.sh SlackBridge tasks/05_listen_for_mentions.md &
AGENT_PIDS+=($!)

# 2. Launch Rover (The Manager / Scheduler)
# Rover wakes up every 10 mins to check if the 24h cycle for others is due.
./run_agent.sh Rover tasks/00_scheduler.md &
AGENT_PIDS+=($!)

echo "System active. SlackBridge is listening."
echo "Rover is managing the 24-hour cycle for Diary, GitAgent, and SystemCheckup."
echo "---"

# Wait for all background agents (this keeps the script in the foreground)
wait
