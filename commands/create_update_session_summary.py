#!/usr/bin/env python3
"""
Session summary file management script for Claude Code.

This script handles the deterministic logic for creating/updating session summary files.
It outputs JSON for the Claude command to process.
"""

import sys
import os
import json
import subprocess
import glob
import shutil
from datetime import datetime
from pathlib import Path


def get_git_branch():
    """Get current git branch name if in a git repository."""
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def sanitize_filename(name):
    """Make a string safe for use in filenames."""
    import re
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)


def find_latest_session_file(sessions_dir, session_name):
    """Find the most recent session file for today with the given session name."""
    today = datetime.now().strftime("%Y%m%d")
    pattern = f"{session_name}_session_summary_{today}_*.md"
    search_path = sessions_dir / pattern
    
    matching_files = glob.glob(str(search_path))
    
    if not matching_files:
        return None
    
    # Sort by timestamp (filename contains timestamp)
    matching_files.sort(reverse=True)  # Most recent first
    return Path(matching_files[0])


def copy_session_file(source_path, target_path):
    """Copy session file from source to target path."""
    try:
        shutil.copy2(source_path, target_path)
        return True
    except Exception as e:
        return False, str(e)


def main():
    # Parse command line arguments
    session_name = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Derive session name if not provided
    if not session_name:
        # Try to get git branch name
        branch_name = get_git_branch()
        if branch_name:
            session_name = sanitize_filename(branch_name)
        else:
            session_name = "session"
    
    # Get current working directory (project root)
    project_root = Path.cwd()
    sessions_dir = project_root / "sessions"
    
    # Create sessions directory if it doesn't exist
    try:
        sessions_dir.mkdir(exist_ok=True)
    except Exception as e:
        print(json.dumps({
            "error": f"Failed to create sessions directory: {e}",
            "success": False
        }))
        sys.exit(1)
    
    # Verify directory is writable
    if not os.access(sessions_dir, os.W_OK):
        print(json.dumps({
            "error": "Sessions directory is not writable",
            "success": False
        }))
        sys.exit(1)
    
    # Generate filename with timestamp
    current_date = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{session_name}_session_summary_{current_date}.md"
    filepath = sessions_dir / filename
    
    # Look for existing session file from today
    existing_file = find_latest_session_file(sessions_dir, session_name)
    file_exists = existing_file is not None
    existing_content = ""
    source_file = ""
    is_copy = False
    
    if file_exists:
        # Check if we're trying to copy to the same file (same minute)
        if existing_file == filepath:
            # File already exists with current timestamp, just read it
            is_copy = False
            source_file = ""
            try:
                existing_content = filepath.read_text(encoding='utf-8')
            except Exception as e:
                print(json.dumps({
                    "error": f"Failed to read existing file: {e}",
                    "success": False
                }))
                sys.exit(1)
        else:
            # Copy existing file to new timestamp
            copy_result = copy_session_file(existing_file, filepath)
            if copy_result is True:
                is_copy = True
                source_file = str(existing_file.relative_to(sessions_dir.parent))
                try:
                    existing_content = filepath.read_text(encoding='utf-8')
                except Exception as e:
                    print(json.dumps({
                        "error": f"Failed to read copied file: {e}",
                        "success": False
                    }))
                    sys.exit(1)
            else:
                print(json.dumps({
                    "error": f"Failed to copy existing file: {copy_result[1]}",
                    "success": False
                }))
                sys.exit(1)
    
    # Output structured data for Claude to process
    result = {
        "success": True,
        "filepath": str(filepath.relative_to(project_root)),
        "absolute_filepath": str(filepath),
        "session_name": session_name,
        "exists": file_exists,
        "content": existing_content,
        "sessions_dir": str(sessions_dir.relative_to(project_root)),
        "filename": filename,
        "is_copy": is_copy,
        "source_file": source_file if source_file else ""
    }
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()