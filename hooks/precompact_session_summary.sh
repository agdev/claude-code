#!/bin/bash

# PreCompact Hook: Auto-generate session summary with intelligent naming
# This hook runs before context compaction to create session summaries

# Get current working directory
working_dir=$(pwd)

# The command now automatically uses ./sessions, so we just need to check if files exist there
sessions_dir="$working_dir/sessions"

# Find latest .md file in sessions directory (by modification time) if it exists
if [ -d "$sessions_dir" ]; then
    latest_file=$(find "$sessions_dir" -name "*.md" -type f -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2-)
else
    latest_file=""
fi

if [ -n "$latest_file" ]; then
    # Extract base name from latest file
    basename=$(basename "$latest_file" .md)
    
    # Remove date pattern _YYYYMMDD and any trailing content
    session_name=$(echo "$basename" | sed 's/_[0-9]\{8\}.*$//')
    
    # Remove _continued suffix if present
    session_name=$(echo "$session_name" | sed 's/_continued$//')
    
    # Remove _session_summary suffix if present  
    session_name=$(echo "$session_name" | sed 's/_session_summary$//')
    
    echo "Derived session name '$session_name' from latest file: $(basename "$latest_file")"
else
    # If no files found, let the command derive the name (it will use git branch or default)
    session_name=""
    echo "No existing session files found, will let command derive session name"
fi

# Debug output
echo "=== PreCompact Hook Debug Info ==="
echo "Working directory: $working_dir"
echo "Latest file: $latest_file"
echo "Derived session name: $session_name"
echo "=================================="

# Call the session summary command - it will handle directory creation and naming
if [ -n "$session_name" ]; then
    echo "Calling: /create_update_session_summary \"$session_name\""
    /create_update_session_summary "$session_name"
else
    echo "Calling: /create_update_session_summary"
    /create_update_session_summary
fi