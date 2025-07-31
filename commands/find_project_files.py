#!/usr/bin/env python3
"""
Deterministic project file finder for Claude Code custom commands.
Finds and validates plan and task files for a given project.
"""

import os
import sys
from pathlib import Path

def find_project_files(project_name, base_dir="."):
    """
    Find plan and task files for a given project name.
    
    Args:
        project_name: Name of the project (e.g., 'dynamic-service-page')
        base_dir: Base directory to search from (default: current directory)
    
    Returns:
        dict: Dictionary with 'plan_file', 'tasks_file', and 'project_dir' paths
    
    Raises:
        FileNotFoundError: If required files are missing with specific details
    """
    base_path = Path(base_dir).resolve()
    specs_dir = base_path / "specs"
    project_dir = specs_dir / project_name
    
    # Expected file patterns
    plan_file = project_dir / f"{project_name}-plan.md"
    tasks_file = project_dir / f"{project_name}-tasks.md"
    
    # Check if specs directory exists
    if not specs_dir.exists():
        raise FileNotFoundError(f"specs directory not found at: {specs_dir}")
    
    # Check if project directory exists
    if not project_dir.exists():
        available_projects = [d.name for d in specs_dir.iterdir() if d.is_dir()]
        raise FileNotFoundError(
            f"Project directory not found: {project_dir}\n"
            f"Available projects: {available_projects}"
        )
    
    # Check for required files
    missing_files = []
    if not plan_file.exists():
        missing_files.append(str(plan_file))
    if not tasks_file.exists():
        missing_files.append(str(tasks_file))
    
    if missing_files:
        raise FileNotFoundError(
            f"Missing required files for project '{project_name}':\n" +
            "\n".join(f"  - {file}" for file in missing_files)
        )
    
    return {
        'plan_file': str(plan_file),
        'tasks_file': str(tasks_file),
        'project_dir': str(project_dir),
        'project_name': project_name
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: python find_project_files.py <project_name>", file=sys.stderr)
        print("Example: python find_project_files.py dynamic-service-page", file=sys.stderr)
        sys.exit(1)
    
    project_name = sys.argv[1]
    
    try:
        result = find_project_files(project_name)
        print("✅ Project files found successfully!")
        print(f"📁 Project: {result['project_name']}")
        print(f"📋 Plan file: {result['plan_file']}")
        print(f"✅ Tasks file: {result['tasks_file']}")
        print(f"📂 Project directory: {result['project_dir']}")
        return result
    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()