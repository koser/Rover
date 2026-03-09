#!/bin/bash

# StartRover.sh - Supervised Launcher for AgentService
# This script stays in the foreground and kills all agents when it exits.

echo "--- 🤖 Starting AgentService Ecosystem ---"
echo "--- Press Ctrl+C to shut down all agents ---"
echo ""

# Array to keep track of PIDs
AGENT_PIDS=()

# Cleanup function
cleanup() {
    echo ""
    echo "--- 🛑 Shutting down AgentService ---"
    for PID in "${AGENT_PIDS[@]}"; do
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID"
        fi
    done
    exit 0
}

# Trap exit signals
trap cleanup SIGINT SIGTERM SIGHUP EXIT

# Ensure log directory exists
mkdir -p logs
touch logs/Diary.log

# 1. Launch SlackBridge (Real-time listener)
./run_agent.sh SlackBridge tasks/05_listen_for_mentions.md &
AGENT_PIDS+=($!)

# 2. Launch Rover (The Manager / Scheduler)
./run_agent.sh Rover tasks/00_scheduler.md &
AGENT_PIDS+=($!)

echo "✅ SlackBridge [Listening]"
echo "✅ Rover [Managing Schedules]"
echo "--- 📺 Live Event Stream ---"
echo ""

# 3. Stream and Format Logs
# This will tail the diary and add color/formatting for terminal readability
tail -n 0 -f logs/Diary.log | awk '
    /\[SUCCESS\]/ { $4="\033[1;32m[SUCCESS]\033[0m" }
    /\[ERROR\]/   { $4="\033[1;31m[ERROR]\033[0m" }
    /\[WARNING\]/ { $4="\033[1;33m[WARNING]\033[0m" }
    /\[Diary\]/   { $2="\033[1;34m[Diary]\033[0m" }
    /\[Rover\]/   { $2="\033[1;36m[Rover]\033[0m" }
    /\[SlackBridge\]/ { $2="\033[1;35m[SlackBridge]\033[0m" }
    /\[GitAgent\]/ { $2="\033[1;33m[GitAgent]\033[0m" }
    { print $0 }
' &
AGENT_PIDS+=($!)

# Keep the script running in the foreground
wait
