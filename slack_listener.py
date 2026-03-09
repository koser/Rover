import os
import time
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime

# Path Configuration
BASE_DIR = "/Users/mikkel/AgentService"
LOG_DIR = os.path.join(BASE_DIR, "logs")
TASK_DIR = os.path.join(BASE_DIR, "tasks")
DIARY_PATH = os.path.join(LOG_DIR, "diary.log")
ALERTS_PATH = os.path.join(LOG_DIR, "ALERTS.log")
CONFIG_PATH = os.path.join(BASE_DIR, "config.env")

def load_config(path):
    config = {}
    if not os.path.exists(path):
        return config
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                config[key] = value.strip('"').strip("'")
    return config

# Load Config
config = load_config(CONFIG_PATH)
SLACK_BOT_TOKEN = config.get("SLACK_BOT_TOKEN") or os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = config.get("SLACK_APP_TOKEN") or os.environ.get("SLACK_APP_TOKEN")

if not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN:
    print(f"Error: SLACK_BOT_TOKEN and SLACK_APP_TOKEN must be set. (Found in config: {bool(config.get('SLACK_BOT_TOKEN'))}, {bool(config.get('SLACK_APP_TOKEN'))})")
    exit(1)

app = App(token=SLACK_BOT_TOKEN)

def log_event(event_type, description, status):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [SlackBridge] [{event_type}] [{status}]: {description}\n"
    
    # Ensure logs dir exists
    os.makedirs(LOG_DIR, exist_ok=True)
    
    with open(DIARY_PATH, "a") as f:
        f.write(log_entry)
    
    if status in ("ERROR", "WARNING"):
        with open(ALERTS_PATH, "a") as f:
            f.write(log_entry)

@app.event("app_mention")
def handle_app_mentions(body, say, logger):
    event = body["event"]
    text = event.get("text", "").strip()
    user_id = event["user"]
    
    # Remove the @mention part
    clean_text = re.sub(r'<@.*?>', '', text).strip()
    
    print(f"[{datetime.now()}] Received mention from {user_id}: {clean_text}")
    
    if clean_text.lower() == 'ping!':
        say(f"pong! 🏓 The current system time is {datetime.now().strftime('%H:%M:%S')}.")
        log_event("USER_REQUEST", f"Received ping! from {user_id}", "SUCCESS")
        return

    # Task Delegation: Translate a Slack message into a new .md task file
    timestamp_ms = int(time.time() * 1000)
    task_filename = f"slack_{timestamp_ms}.md"
    task_path = os.path.join(TASK_DIR, task_filename)
    
    task_content = f"# Task: Slack Instruction from {user_id}\n\n## Goal\n{clean_text}\n\n## Status\nPending\n"
    
    try:
        os.makedirs(TASK_DIR, exist_ok=True)
        with open(task_path, "w") as f:
            f.write(task_content)
        
        say(f"🚀 Instruction received, <@{user_id}>. Task created: {task_filename}")
        log_event("USER_REQUEST", f"Created task {task_filename} from {user_id}: \"{clean_text}\"", "SUCCESS")
    except Exception as e:
        log_event("SYSTEM_ERROR", f"Failed to create task file for {user_id}: {str(e)}", "ERROR")
        say(f"⚠️ Error creating task: {str(e)}")

if __name__ == "__main__":
    try:
        handler = SocketModeHandler(app, SLACK_APP_TOKEN)
        print("⚡️ Rover Slack Bridge (Python) is ACTIVE and listening for mentions...")
        log_event("AGENT_START", "SlackBridge listener starting...", "SUCCESS")
        handler.start()
    except Exception as e:
        log_event("AGENT_START", f"Failed to start SlackBridge: {str(e)}", "ERROR")
        print(f"Error starting SlackBridge: {e}")
