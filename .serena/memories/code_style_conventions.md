# Code Style and Conventions

## Markdown Formatting
- Use standard GitHub-flavored Markdown
- Task lists use `[ ]` for pending and `[x]` for completed
- File names use kebab-case (e.g., `task-lists.md`)
- Headers use proper hierarchy (#, ##, ###)

## Task List Structure
- **File naming**: `TASKS.md` or descriptive feature names
- **Required sections**:
  - Completed Tasks
  - In Progress Tasks  
  - Future Tasks
  - Implementation Plan
  - Relevant Files

## File Organization
- Commands stored in `.claude/commands/`
- Specifications in `specs/`
- Project configuration in `.serena/`
- Memory files in `.serena/memories/`

## Naming Conventions
- Task IDs: `[T001]` format for numbered tasks
- Files: kebab-case with descriptive names
- Directories: lowercase with hyphens
- Memory files: snake_case with `.md` extension

## Documentation Standards
- Include timestamps for generated content
- Maintain "Relevant Files" sections with file paths and descriptions
- Use status indicators (✅, ⚡) for file states
- Include complexity scoring (1-10) for tasks