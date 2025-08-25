#!/usr/bin/env python3
"""
Plan and task files management script for Claude Code.

This script handles the deterministic logic for creating/updating plan and task files.
It outputs JSON for the Claude command to process.
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path


def sanitize_filename(name):
    """Make a string safe for use in filenames."""
    import re
    return re.sub(r'[^a-zA-Z0-9_-]', '_', name)


def main():
    # Parse command line arguments
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Missing required arguments. Usage: script.py folder_name [prefix]",
            "success": False
        }))
        sys.exit(1)
    
    folder_name = sanitize_filename(sys.argv[1])
    # Use folder_name as prefix if no second argument provided
    prefix = sanitize_filename(sys.argv[2]) if len(sys.argv) > 2 else folder_name
    
    # Get current working directory (project root)
    project_root = Path.cwd()
    specs_dir = project_root / "specs"
    target_dir = specs_dir / folder_name
    
    # Create specs directory if it doesn't exist
    try:
        specs_dir.mkdir(exist_ok=True)
    except Exception as e:
        print(json.dumps({
            "error": f"Failed to create specs directory: {e}",
            "success": False
        }))
        sys.exit(1)
    
    # Create target directory if it doesn't exist
    try:
        target_dir.mkdir(exist_ok=True)
    except Exception as e:
        print(json.dumps({
            "error": f"Failed to create target directory: {e}",
            "success": False
        }))
        sys.exit(1)
    
    # Verify directory is writable
    if not os.access(target_dir, os.W_OK):
        print(json.dumps({
            "error": "Target directory is not writable",
            "success": False
        }))
        sys.exit(1)
    
    # Generate filenames
    plan_filename = f"{prefix}-plan.md"
    tasks_filename = f"{prefix}-tasks.md"
    plan_filepath = target_dir / plan_filename
    tasks_filepath = target_dir / tasks_filename
    
    # Create empty files if they don't exist
    plan_exists = plan_filepath.exists()
    tasks_exists = tasks_filepath.exists()
    
    if not plan_exists:
        try:
            plan_filepath.touch()
        except Exception as e:
            print(json.dumps({
                "error": f"Failed to create plan file: {e}",
                "success": False
            }))
            sys.exit(1)
    
    if not tasks_exists:
        try:
            tasks_filepath.touch()
        except Exception as e:
            print(json.dumps({
                "error": f"Failed to create tasks file: {e}",
                "success": False
            }))
            sys.exit(1)
    
    # Output structured data for Claude to process
    result = {
        "success": True,
        "folder_name": folder_name,
        "prefix": prefix,
        "plan_file": {
            "filepath": str(plan_filepath.relative_to(project_root)),
            "absolute_filepath": str(plan_filepath),
            "filename": plan_filename,
            "exists": plan_exists
        },
        "tasks_file": {
            "filepath": str(tasks_filepath.relative_to(project_root)),
            "absolute_filepath": str(tasks_filepath),
            "filename": tasks_filename,
            "exists": tasks_exists
        },
        "target_dir": str(target_dir.relative_to(project_root)),
        "specs_dir": str(specs_dir.relative_to(project_root))
    }
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()