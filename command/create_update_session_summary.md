I need to create or update a session summary file with the following parameters:

- First argument (optional): Session name (e.g., "database-integration")
- Default location: ./sessions/ (at the project root where command is executed)

Usage: /create_update_session_summary [session_name]

Steps:

1. Parse optional session name argument
2. If no session name provided, derive from context (e.g., git branch name)
3. Create the filename format: {session_name}_session_summary_{current_date}.md where current_date is in YYYYMMDD_HHMM format
4. Use ./sessions as the target directory (relative to current working directory)
5. Ensure the sessions directory exists
6. Check if the file already exists
7. If the file exists, read its current content and update it with new session information
8. If the file doesn't exist, create a new one with a detailed session summary template
9. Generate a comprehensive summary of the current session including:
   - Session overview and objectives
   - Key tasks completed
   - Code changes made
   - Issues encountered and resolved
   - Next steps and follow-up items
   - Technical decisions and rationale

Let me parse the arguments and create the session summary:

```bash
# Parse optional session name argument
session_name="$ARGUMENTS"

# If no session name provided, try to derive from git branch or use default
if [ -z "$session_name" ]; then
    # Try to get current git branch name
    if git rev-parse --git-dir > /dev/null 2>&1; then
        branch_name=$(git branch --show-current 2>/dev/null)
        if [ -n "$branch_name" ]; then
            # Clean branch name to make it filename-safe
            session_name=$(echo "$branch_name" | sed 's/[^a-zA-Z0-9_-]/_/g')
            echo "Using git branch name for session: $session_name"
        else
            session_name="session"
            echo "No git branch found, using default session name: $session_name"
        fi
    else
        session_name="session"
        echo "Not in a git repository, using default session name: $session_name"
    fi
fi

# Get current working directory (project root)
project_root=$(pwd)
target_directory="${project_root}/sessions"

echo "=== SESSION SUMMARY CREATION ==="
echo "Project root: $project_root"
echo "Session name: $session_name"
echo "Target directory: $target_directory"

# Create the sessions directory if it doesn't exist
mkdir -p "$target_directory"
if [ $? -ne 0 ]; then
    echo "Error: Failed to create sessions directory at $target_directory"
    exit 1
fi

# Verify the directory was created and is accessible
if [ ! -d "$target_directory" ]; then
    echo "Error: Sessions directory does not exist after creation"
    exit 1
fi

if [ ! -w "$target_directory" ]; then
    echo "Error: Sessions directory is not writable"
    exit 1
fi

# Get current date in YYYYMMDD_HHMM format
current_date=$(date +%Y%m%d_%H%M)

# Create the filename
filename="${session_name}_session_summary_${current_date}.md"
filepath="${target_directory}/${filename}"

echo "Target file: $filepath"
echo "=================================="

# Check if file exists and handle accordingly
if [ -f "$filepath" ]; then
    echo "✓ Updating existing session summary: $filename"
    echo "Current content of $filename:"
    cat "$filepath"
    echo "---"
    echo "Please provide additional information to update this session summary."
else
    echo "✓ Creating new session summary file: $filename"
    
    # Create the file with proper permissions
    touch "$filepath"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create file $filepath"
        exit 1
    fi
    
    echo "✓ File created successfully at: $filepath"
    echo "File location: ./sessions/$filename (relative to project root)"
fi
```

Now I'll create or update the session summary with detailed information about the current session. The file will be placed in the ./sessions directory at the project root.
