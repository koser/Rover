# Skill: Project Manager

## Description
Provides a standardized method for defining, documenting, and archiving specific engineering or feature efforts within `~/AgentService/projects/`.

## Tools / Methods
- `init_project(name, summary)`: Creates a new directory in `projects/[name]/` and writes an initial `readme.txt` with the summary.
- `archive_project(name, rationale)`: Updates the `readme.txt` with a final "Paused" or "Completed" status and a summary of what was learned.
- `resume_project(name)`: Reads the `readme.txt` and `auth_details.md` to re-inject the context into Rover (me) or other agents.
- `generate_restart_prompt(name)`: Formulates a concise prompt that a future instance of Rover can use to pick up the work immediately.

## Execution Pattern
1. Create a sub-folder in `~/AgentService/projects/[project_name]`.
2. Maintain a `readme.txt` that includes:
   - **Summary**: What the project is trying to achieve.
   - **Status**: (Active, Paused, Completed).
   - **Knowledge Gained**: Key technical hurdles and findings.
   - **Restart Prompt**: A direct instruction for a future agent.
3. Use this folder to store all project-specific scripts, logs, and configuration files.
