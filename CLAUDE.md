# Model usage

## Planning mode

Opus when available

## Execution mode

Sonnet

## Project Structure

- Place all test files and snapshots in 'claude-code-test-ground' folder at the root of the project
- If 'claude-code-test-ground' folder does not exist, create it first
- When making code changes: create backup file of code before making changes and move it to 'claude-backup-files' folder at root directory
- If 'claude-backup-files' folder does not exist, create it first

## Documentation Guidelines

### NEVER Proactively Create Documentation
- **NEVER** create documentation files (*.md) or README files unless explicitly requested by the user
- Only create documentation when user specifically asks for it
- Ask for clarification if documentation need is unclear

### Plan-Based Execution Reports
When implementing plan by executing tasks based on plan and task files:
- Save all reports, phase completion summaries, and deliverables in the **same folder where plan and task files are located**
- If plan/task files are not in a specific folder, follow the documentation structure below

### Documentation Structure (claude-code-docs/)

When creating documentation files at user's request:

#### Active Development Guides (`claude-code-docs/active-guides/`)
Place ongoing reference material in appropriate subcategory:
- `active-guides/setup/` - Setup and configuration guides
- `active-guides/reference/` - API and technical references
- `active-guides/testing/` - Testing documentation

#### Session Deliverables (`claude-code-docs/phase-deliverables/`)
Place project-specific outputs and phase completion summaries here:
- Phase completion summaries
- Verification reports
- Project-specific analysis documents

#### File Naming Conventions
- Use descriptive UPPERCASE filenames: `JWT_HELPER_QUICK_REFERENCE.md`
- Include "Last Updated" dates in document headers
- Cross-reference related documentation
- Update claude-code-docs/README.md when adding new files

#### Documentation Lifecycle
1. **Create** - New docs in appropriate active-guides/ or phase-deliverables/ folder
2. **Maintain** - Update docs as systems evolve
3. **Archive** - Move superseded docs to `.claude-archive/claude-code-docs/` using `git mv`
4. **Reference** - Link to archived docs for historical context

#### Related Documentation
- `docs/` - Project-wide documentation (architecture, APIs, design patterns)
- `server/docs/` - Backend API documentation
- `client/docs/` - Frontend component documentation
- `.claude-archive/` - Historical/superseded documentation

## Design Principles

- Keep code as simple as possible, do not over engineer. Simplicity always wins
- Do not commit anything without my explicit instruction
- Do not defer tasks for effeciency under any circumstances

## Git Merge Workflow

When merging branches:
1. **Always fetch before merge** - Run `git fetch origin` first
2. **Use remote refs, not local** - Merge `origin/branch-name` instead of local `branch-name`
3. **Check for conflicts first** - Use `git merge --no-commit --no-ff origin/branch-name` to test
4. **Verify with `git diff --cached --stat`** - Review what will be merged before committing

Example workflow:
```bash
git fetch origin
git merge --no-commit --no-ff origin/feature-branch  # test for conflicts
git diff --cached --stat                              # review changes
git commit                                            # complete merge
```

**Why:** Local branches may be outdated. Always use `origin/` refs after fetching to ensure you're merging the latest remote version.