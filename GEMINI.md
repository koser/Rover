# AgentService Architecture: Persona-Mission-Skill

## Core Principles
1. **Personas**: Every agent has a defined character and operational style.
2. **Missions**: Long-term objectives that guide an agent's decision-making process.
3. **Skills**: Modular capabilities defined in `skills/SKILL.md` files. Skills are agnostic of agents and can be shared or upgraded independently.

## Agent Structure
- **Agent Config (`agents/*.config`)**: Defines the persona, mission, and assigned skills.
- **Task Source (`tasks/*.md`)**: Concrete goals for agents to fulfill.
- **Agent Logs (`logs/*.log`)**: Detailed activity trace for each specific agent.
- **The Diary (`logs/diary.log`)**: The immutable source of truth for all system-wide events.

## Hard Rules (Mandatory)
1. **Scope Restriction**: Never perform file operations (read, write, delete, move) on files outside of the `~/AgentService/` directory tree.
2. **Deletion Protocol**: STRICTLY FORBIDDEN from deleting or overwriting files without explicit user permission.
3. **Skill Adherence**: When using a skill, strictly follow the execution pattern defined in its `SKILL.md`.

## Lifecycle
- **The Hub**: Orchestrates the spinning up of agents using their configuration.
- **The Diary Agent**: The first agent in the system, responsible for logging all events.
