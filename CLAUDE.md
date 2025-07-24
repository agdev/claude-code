# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This is a minimal repository focused on command rules and task management guidelines. The main components are:

- `command/` - Contains command-specific rules and guidelines in MDC format
- `LICENSE` - MIT license file

## Task List Management Guidelines

This repository follows specific task list management practices defined in `command/task-lists.mdc`:

### Task List Creation
- Create task lists in markdown files (preferably `TASKS.md` or descriptive feature names)
- Structure with sections: Completed Tasks, In Progress Tasks, Future Tasks, Implementation Plan
- Include a "Relevant Files" section with file paths and descriptions

### Task List Maintenance
- Mark completed tasks by changing `[ ]` to `[x]`
- Keep the "Relevant Files" section updated with accurate paths and descriptions
- Add implementation details for complex features
- Update task lists after implementing significant components

### AI Workflow
When working on features:
1. Check existing task list to see which task to implement next
2. Implement the task
3. Update the task list to reflect progress
4. Mark completed tasks with `[x]`
5. Add newly discovered tasks during implementation

## Development Notes

- This repository uses MDC (Markdown Command) format for command rules
- No build tools, package managers, or testing frameworks are currently configured
- The repository is initialized with git but contains minimal content