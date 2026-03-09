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

# 1. Launch agents in the background of THIS shell
./run_agent.sh Diary tasks/01_observe_changes.md &
AGENT_PIDS+=($!)

./run_agent.sh GitAgent tasks/02_sync_repo.md &
AGENT_PIDS+=($!)

./run_agent.sh SystemCheckup tasks/03_connectivity_audit.md &
AGENT_PIDS+=($!)

./run_agent.sh SlackBridge tasks/05_listen_for_mentions.md &
AGENT_PIDS+=($!)

echo "All agents are running. Keeping this window open will keep them alive."
echo "Closing this window or pressing Ctrl+C will shut down all agents."
echo "---"

# Wait for all background agents (this keeps the script in the foreground)
wait
