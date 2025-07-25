I need to create or update a session summary file with the following parameters:

- First argument (optional): Session name (e.g., "database-integration")
- Default location: ./sessions/ (at the project root where command is executed)

Usage: /create_update_session_summary [session_name]

Let me execute the Python script to handle the file operations and determine the next steps:

```bash
uv run /home/yoda/.claude/commands/create_update_session_summary.py $ARGUMENTS
```

Based on the Python script output, I will:

1. If the file already exists, read its current content and update it with new session information
2. If the file doesn't exist, create a new one with a detailed session summary template

The session summary will include:

- Session overview and objectives
- Key tasks completed
- Code changes made
- Issues encountered and resolved
- Next steps and follow-up items
- Technical decisions and rationale

I'll generate a comprehensive summary of the current session and write it to the appropriate file location.
