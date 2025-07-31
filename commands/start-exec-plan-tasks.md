---
description: "Execute project plans with mandatory real-time task tracking"
argument-hint: "<project-name>"
allowed-tools: ["Read", "Edit", "Write", "MultiEdit", "TodoWrite", "Bash", "Glob", "Grep"]
---

# Execute Project Plan and Tasks

**CRITICAL REQUIREMENT: You MUST update the project task file at `specs/[project]/[project]-tasks.md` after completing EACH individual task. This is not optional.**

## Mandatory Task Tracking Instructions

**Specifically:**

- **After completing ANY task, immediately update the task file by changing `[ ]` to `[x]`**
- **Do this BEFORE moving to the next task**
- **Never batch update multiple completed tasks at once**
- **The task file must always reflect current progress in real-time**
- **If you forget to update the task file, STOP and update it before continuing**

**Example workflow:**

1. Complete a task (e.g., 'Audit ai-ml service page content')
2. IMMEDIATELY update task file: `- [x] Audit ai-ml service page content`
3. Then and only then proceed to next task

## Command Execution

First, let's find and validate the project files:

!uv run .claude/commands/find_project_files.py $ARGUMENTS

## Project Plan Execution

Based on the validated project files, I will:

1. **Read the plan file** (`specs/[project]/[project]-plan.md`) to understand the project scope and approach
2. **Read the tasks file** (`specs/[project]/[project]-tasks.md`) to see current progress and remaining tasks
3. **Execute the plan** following the tasks in order, updating progress in real-time
4. **Track progress** using both TodoWrite tool and the project task file

## Task File Update Requirements

**This applies to:**

- Individual sub-tasks within phases
- Major phase completions  
- Any task marked with `[ ]` in the specs file

**The task file is the single source of truth for project progress.**

## Error Handling

If project files are not found, the Python script will provide:

- Clear error messages about missing files
- List of available projects in the specs directory
- Specific file paths that are missing

## Usage

```bash
/start-exec-plan-tasks dynamic-service-page
/start-exec-plan-tasks [any-project-name]
```

The command will automatically find and execute plans for any project following the pattern:

- `specs/[project-name]/[project-name]-plan.md`
- `specs/[project-name]/[project-name]-tasks.md`
