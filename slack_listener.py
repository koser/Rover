import os
import time
import re
import subprocess
import threading
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
ROVER_CONFIG_PATH = os.path.join(BASE_DIR, "agents/Rover.config")
GEMINI_PATH = "/opt/homebrew/bin/gemini"

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
    print(f"Error: SLACK_BOT_TOKEN and SLACK_APP_TOKEN must be set.")
    exit(1)

app = App(token=SLACK_BOT_TOKEN)

# Global state for tracking active tasks
active_tasks = 0
active_tasks_lock = threading.Lock()

def log_event(event_type, description, status):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [SlackBridge] [{event_type}] [{status}]: {description}\n"
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(DIARY_PATH, "a") as f:
        f.write(log_entry)
    if status in ("ERROR", "WARNING"):
        with open(ALERTS_PATH, "a") as f:
            f.write(log_entry)

def run_gemini_task(task_filename, clean_text, user_id, say):
    global active_tasks
    stop_timer = threading.Event()

    def progress_timer():
        start_time = time.time()
        # Initial wait before the first "still working" message
        if stop_timer.wait(60):
            return
        while not stop_timer.is_set():
            elapsed = int(time.time() - start_time)
            say(f"I'm still working on your request, <@{user_id}>. It's been about {elapsed} seconds, and I'm continuing to process it. I'll let you know as soon as I'm finished! ⏳")
            if stop_timer.wait(60): # Update every minute
                break

    try:
        # Combined context for the Rover Agent
        with open(ROVER_CONFIG_PATH, 'r') as f:
            rover_config = f.read()
        gemini_md_path = os.path.join(BASE_DIR, "GEMINI.md")
        with open(gemini_md_path, 'r') as f:
            gemini_md = f.read()
        
        # Enhanced instruction to ensure natural language response
        instruction = (
            f"User Instruction: {clean_text}. \n\n"
            f"IMPORTANT: You are responding to <@{user_id}> on Slack. "
            "Provide a helpful, friendly, and natural language response. "
            "If you performed actions, summarize them clearly. "
            "If you found information, present it in an easy-to-read format."
        )

        gemini_cmd = [
            GEMINI_PATH,
            "--yolo",
            f"System Context: {gemini_md}. Your Config: {rover_config}. Instruction: {instruction}"
        ]

        log_event("AGENT_ACTION", f"Rover Agent starting task: {task_filename}", "PENDING")
        
        # Start the progress timer thread
        timer_thread = threading.Thread(target=progress_timer)
        timer_thread.start()

        try:
            result = subprocess.run(gemini_cmd, capture_output=True, text=True, check=False)
        finally:
            stop_timer.set()
            timer_thread.join()
        
        if result.returncode == 0:
            log_event("AGENT_ACTION", f"Rover Agent successfully completed task: {task_filename}", "SUCCESS")
            
            # Format response: prioritize stdout, but keep it within Slack's limits
            response = result.stdout.strip()
            if not response:
                response = "I've finished the task, but I don't have a specific message to report. Please let me know if there's anything else you need!"
            
            if len(response) > 3000:
                response = response[:3000] + "\n\n...(Response truncated due to length)..."
            
            say(f"✅ <@{user_id}>, I've completed your request!\n\n{response}")
            
            # Update task file status
            task_path = os.path.join(TASK_DIR, task_filename)
            if os.path.exists(task_path):
                with open(task_path, 'r') as f:
                    content = f.read()
                updated_content = content.replace("Status\nPending", f"Status\nCompleted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                with open(task_path, 'w') as f:
                    f.write(updated_content)
        else:
            log_event("SYSTEM_ERROR", f"Rover Agent failed task {task_filename}: {result.stderr}", "ERROR")
            error_details = result.stderr.strip() or result.stdout.strip() or "No error details available."
            if len(error_details) > 1000:
                error_details = error_details[:1000] + "..."
            say(f"I'm sorry <@{user_id}>, but I ran into a bit of trouble while working on that:\n\n```{error_details}```\n\nIf you'd like, I can try again or you can try rephrasing the request.")
            
    except Exception as e:
        log_event("SYSTEM_ERROR", f"Error in background task {task_filename}: {str(e)}", "ERROR")
        say(f"⚠️ I'm very sorry <@{user_id}>, but a system error occurred: {str(e)}")
    finally:
        with active_tasks_lock:
            active_tasks -= 1

@app.event("app_mention")
def handle_app_mentions(body, say, logger):
    global active_tasks
    event = body["event"]
    text = event.get("text", "").strip()
    user_id = event["user"]
    clean_text = re.sub(r'<@.*?>', '', text).strip()
    
    if clean_text.lower() == 'ping!':
        say(f"pong! 🏓 I'm alive and well. The current system time is {datetime.now().strftime('%H:%M:%S')}.")
        log_event("USER_REQUEST", f"Received ping! from {user_id}", "SUCCESS")
        return

    timestamp_ms = int(time.time() * 1000)
    task_filename = f"slack_{timestamp_ms}.md"
    task_path = os.path.join(TASK_DIR, task_filename)
    task_content = f"# Task: Slack Instruction from {user_id}\n\n## Goal\n{clean_text}\n\n## Status\nPending\n"
    
    try:
        os.makedirs(TASK_DIR, exist_ok=True)
        with open(task_path, "w") as f:
            f.write(task_content)
        
        with active_tasks_lock:
            if active_tasks > 0:
                say(f"Hi <@{user_id}>! I've received your request: \"{clean_text}\". I'm currently handling {active_tasks} other task(s), so I've added yours to my queue and will start on it as soon as I'm free. ⏳")
            else:
                say(f"Hi <@{user_id}>! I'm on it. I'll start working on your request right away: \"{clean_text}\". I'll update you as soon as I'm finished! 🚀")
            active_tasks += 1

        log_event("USER_REQUEST", f"Created task {task_filename} from {user_id}: \"{clean_text}\"", "SUCCESS")

        # Start Gemini task in a background thread
        thread = threading.Thread(target=run_gemini_task, args=(task_filename, clean_text, user_id, say))
        thread.start()

    except Exception as e:
        log_event("SYSTEM_ERROR", f"Failed to process instruction for {user_id}: {str(e)}", "ERROR")
        say(f"⚠️ Error processing instruction: {str(e)}")

if __name__ == "__main__":
    try:
        handler = SocketModeHandler(app, SLACK_APP_TOKEN)
        print("⚡️ Rover Slack Bridge (Python) is ACTIVE and listening for mentions...")
        log_event("AGENT_START", "SlackBridge listener starting...", "SUCCESS")
        handler.start()
    except Exception as e:
        log_event("AGENT_START", f"Failed to start SlackBridge: {str(e)}", "ERROR")
        print(f"Error starting SlackBridge: {e}")

