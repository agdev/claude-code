# Task Completion Workflow

## When a Task is Completed

Since this project has no build system, testing framework, or linting tools, the completion workflow focuses on documentation and task management:

### 1. Update Task Lists
- Mark completed tasks with `[x]` in markdown files
- Move tasks from "In Progress" to "Completed" sections
- Update the "Relevant Files" section with new or modified files

### 2. Documentation Updates
- Update README.md if new features or commands are added
- Add memory files for new concepts or patterns discovered
- Update CLAUDE.md with any new project guidelines

### 3. Git Operations
```bash
git add .
git commit -m "descriptive commit message"
git push
```

### 4. Quality Checks
- Verify markdown formatting is correct
- Ensure task list structure follows conventions
- Check that file paths in "Relevant Files" sections are accurate
- Validate that new commands follow MDC format

### 5. Session Documentation
- Session logs are automatically created in `session/`
- No manual intervention needed for session tracking

## No Traditional QA Steps
- No unit tests to run
- No linting to execute  
- No build process to verify
- No type checking to perform

## Focus Areas
- Documentation accuracy
- Task list maintenance
- File organization
- Markdown formatting consistency