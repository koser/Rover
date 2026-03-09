#!/bin/bash
source "$HOME/AgentService/config.env"

AGENT_NAME=$1
CONFIG_FILE="$HOME/AgentService/agents/${AGENT_NAME}.config"
TASK_FILE=$2

if [ -z "$AGENT_NAME" ] || [ ! -f "$CONFIG_FILE" ] || [ -z "$TASK_FILE" ]; then
    echo "Usage: ./run_agent.sh <agent_name> <path_to_task_file>"
    exit 1
fi

AGENT_LOG="$LOG_DIR/${AGENT_NAME}.log"
PID_FILE="$AGENT_DIR/${AGENT_NAME}.pid"
HEARTBEAT_LOG="$LOG_DIR/heartbeat.log"

# --- Execution Loop ---
RUN_ONCE=false
if [ "$3" == "--once" ]; then
    RUN_ONCE=true
fi

while true; do
    WAKE_MSG="--- [$AGENT_NAME] Waking Up: $(date +%H:%M:%S) ---"
    echo "$WAKE_MSG" >> "$HEARTBEAT_LOG"
    
    # Load agent's full context (Persona, Mission, and Task)
    CORE_CONTEXT="Context: $(cat "$HOME/AgentService/GEMINI.md"). Agent Config: $(cat "$CONFIG_FILE"). Task: $(cat "$TASK_FILE")"
    
    # Dynamically load assigned skills from the config
    SKILLS_CONTEXT=""
    IN_SKILLS_SECTION=false
    while read -r line; do
        if [[ "$line" == "## Assigned Skills"* ]]; then
            IN_SKILLS_SECTION=true
            continue
        elif [[ "$line" == "## "* ]] && $IN_SKILLS_SECTION; then
            IN_SKILLS_SECTION=false
            break
        fi
        
        if $IN_SKILLS_SECTION && [[ "$line" =~ ^-[[:space:]]\`([^\`]+)\`: ]]; then
            SKILL_NAME="${BASH_REMATCH[1]}"
            SKILL_PATH="$HOME/AgentService/skills/$SKILL_NAME/SKILL.md"
            if [ -f "$SKILL_PATH" ]; then
                SKILLS_CONTEXT="$SKILLS_CONTEXT Skill Definition ($SKILL_NAME): $(cat "$SKILL_PATH")"
            fi
        fi
    done < "$CONFIG_FILE"

    $AI_ENGINE --yolo "$CORE_CONTEXT $SKILLS_CONTEXT" >> "$AGENT_LOG" 2>&1
    
    if $RUN_ONCE; then
        echo "[$AGENT_NAME] Single execution complete. Exiting."
        break
    fi

    sleep 600
done
