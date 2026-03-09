import subprocess
import os

BASE_DIR = "/Users/mikkel/AgentService"
GEMINI_PATH = "/opt/homebrew/bin/gemini"
ROVER_CONFIG_PATH = os.path.join(BASE_DIR, "agents/Rover.config")
gemini_md_path = os.path.join(BASE_DIR, "GEMINI.md")

with open(ROVER_CONFIG_PATH, 'r') as f:
    rover_config = f.read()
with open(gemini_md_path, 'r') as f:
    gemini_md = f.read()

clean_text = "What is the current time?"

gemini_cmd = [
    GEMINI_PATH,
    "--yolo",
    f"System Context: {gemini_md}. Your Config: {rover_config}. Instruction: {clean_text}"
]

result = subprocess.run(gemini_cmd, capture_output=True, text=True, check=False)
print("STDOUT:")
print(result.stdout)
print("STDERR:")
print(result.stderr)
