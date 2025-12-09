#!/usr/bin/env python3
import json
import os
import subprocess
import sys


def find_git_dir(start_path):
    """Walk up directories to find .git folder or file (for submodules)."""
    path = os.path.abspath(start_path)
    while path != "/":
        git_path = os.path.join(path, ".git")
        if os.path.exists(git_path):
            return git_path
        path = os.path.dirname(path)
    return None


def get_git_branch(git_path):
    """Get branch name or short commit hash for detached HEAD."""
    # Handle submodules where .git is a file pointing to the real git dir
    if os.path.isfile(git_path):
        try:
            with open(git_path, "r") as f:
                content = f.read().strip()
                if content.startswith("gitdir: "):
                    git_path = content.replace("gitdir: ", "")
        except:
            return ""

    head_path = os.path.join(git_path, "HEAD") if os.path.isdir(git_path) else git_path
    if not os.path.isdir(git_path):
        return ""

    head_path = os.path.join(git_path, "HEAD")
    try:
        with open(head_path, "r") as f:
            ref = f.read().strip()
            if ref.startswith("ref: refs/heads/"):
                return ref.replace("ref: refs/heads/", "")
            else:
                # Detached HEAD - return short commit hash
                return ref[:7]
    except:
        return ""


def get_dirty_status(git_dir):
    """Check if working tree has uncommitted changes."""
    try:
        # Get the repo root from git_dir
        repo_root = os.path.dirname(git_dir) if git_dir.endswith(".git") else os.path.dirname(git_dir)
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=0.5
        )
        return "*" if result.stdout.strip() else ""
    except:
        return ""


# Read JSON from stdin
data = json.load(sys.stdin)

# Extract values
model = data["model"]["display_name"]
workspace_dir = data["workspace"]["current_dir"]
current_dir = os.path.basename(workspace_dir)

# Find git directory by walking up from workspace
git_branch = ""
git_path = find_git_dir(workspace_dir)
if git_path:
    branch = get_git_branch(git_path)
    if branch:
        dirty = get_dirty_status(git_path)
        git_branch = f" | \U0001F33F {branch}{dirty}"

print(f"[{model}] \U0001F4C1 {current_dir}{git_branch}")
