# Suggested Commands

## Development Commands
Since this is a documentation-focused project with no build system, most commands are file operations:

### Git Commands
```bash
git status                    # Check repository status
git add .                     # Stage changes
git commit -m "message"       # Commit changes
git push                      # Push to remote
git pull                      # Pull from remote
```

### File Operations
```bash
ls -la                        # List files with details
find . -name "*.md"           # Find markdown files
grep -r "pattern" .           # Search for patterns
cat filename.md               # View file contents
```

### Claude Code Commands
```bash
/project:prd-to-tasks <prd_file> <output_folder>    # Convert PRD to tasks
/project:task-breakdown <input> <output_folder>     # Break down tasks
```

### Directory Navigation
```bash
cd specs/                     # Navigate to specifications
cd command/                   # Navigate to command rules
cd .claude/commands/          # Navigate to slash commands
```

## No Build/Test Commands
- No npm, yarn, or package manager commands
- No testing framework (jest, mocha, etc.)
- No linting tools (eslint, prettier)
- No compilation or build process

## Project-Specific Operations
- Create task lists in markdown format
- Update task status with checkbox syntax
- Maintain "Relevant Files" sections
- Follow MDC format for command rules