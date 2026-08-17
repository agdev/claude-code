# User Level instructions for claude code

## Response Style

- Respond in plain English — clear, simple language. Use the terminology already in the context; when a new term is genuinely needed, say it is new and define it. When the user uses a term you do not fully understand, ask before assuming a definition.
- Be succinct: use as few words as possible without losing detail, meaning, or intent.
- Separate fact from inference: verify claims before stating them when tools allow, and present anything unverified as unverified, never as fact.
- Claims about a document's contents come from reading it in this session — re-read or grep the actual file first, not memory. When comparing artifacts (skills, files, docs, plans) for overlap, contradiction, or duplication, read both in full and compare specific content claims, not titles, headings, or remembered structure.
- Explain scenario-first: lead findings, test results, and design consequences with the concrete story of what happens in the real system, step by step, in plain words. Define every term at first use; mechanism labels, severity ratings, and shorthand come only after the story, if at all. The bar: someone who didn't follow the internals could retell the scenario after one read.

## Web Search

- Use Brave Search MCP tools (`mcp__brave-search__*`, e.g. `brave_web_search`) for all web searches and research. Fall back to the built-in WebSearch tool only if Brave Search is unavailable or fails.

## Workspace Folders

### Scratch & Working Folders

- Place all test files and snapshots in 'claude-code-test-ground' folder at the root of the project
- If 'claude-code-test-ground' folder does not exist, create it first
- When making code changes: create backup file of code before making changes and move it to 'claude-backup-files' folder at root directory
- If 'claude-backup-files' folder does not exist, create it first

### Documentation Folders (`claude-code-docs/`)

When creating documentation files at user's request:

#### Active Development Guides (`claude-code-docs/guides/`)

Place ongoing reference material in appropriate subcategory:

- `guides/setup/` - Setup and configuration guides
- `guides/reference/` - API and technical references
- `guides/testing/` - Testing documentation

#### Lessons Learned (`claude-code-docs/lessons/`)

Place ongoing lessons that you learned

#### Open Subjects (`claude-code-docs/open-subjects/`)

Place open subjects/issues

### Related Project Folders

- `docs/` - Project-wide documentation (architecture, APIs, design patterns)
- `server/docs/` - Backend API documentation
- `client/docs/` - Frontend component documentation
- `.claude-archive/` - Historical/superseded documentation

## Documentation Guidelines

### Plan-Based Execution Reports
- Save all related reports, design, and deliverables in the **same folder where plan and task files are located**
- If plan/task files are not in a specific folder, see "Workspace Folders" above

### File Naming Conventions

- Use descriptive UPPERCASE filenames: `JWT_HELPER_QUICK_REFERENCE.md`
- Include "Last Updated" dates in document headers
- Cross-reference related documentation
- Update claude-code-docs/README.md when adding new files

## Design Principles

- Keep code as simple as possible, **NEVER** over engineer. Simplicity always wins
- **NEVER** commit anything without my explicit instruction
- **NEVER** defer tasks for efficiency under any circumstances
- When making technical decisions, **NEVER** give any weight to development cost. Instead, prefer quality, simplicity, robustness, scalability, and long term maintainability.
- **No Timelines in Plans** - When creating plans (plan files, task files, specs), **NEVER** include:
    - Timeline sections
    - Time estimates
    - Day-by-day breakdowns
    - Duration predictions
    - "Day 1", "Day 2" style phases

  Focus on: what needs to be done, in what order, and how to verify completion.

## Git Merge Workflow

When merging branches:

### Phase 1: Assess (BEFORE merging)

1. **Fetch latest** — `git fetch origin`
2. **See what the incoming branch changed since divergence** — `git diff HEAD...origin/branch-name --stat`
   - 3-dot syntax uses the common ancestor, not the branch tip. This shows what B actually contributed, not a tip-to-tip comparison.
3. **See unique commits on the incoming branch** — `git log main..origin/branch-name --oneline`
   - Use the local branch name, not `HEAD`. `HEAD` resolves to a commit SHA and will miss commits if your local branch is behind.

### Phase 2: Merge with Safeguards

4. **Test merge for conflicts** — `git merge --no-commit --no-ff origin/branch-name`
5. **Review staged changes** — `git diff --cached --stat`
   - Look at deletions specifically. Files you created on your branch should not appear as deleted here.
6. **Complete merge** — `git commit`

### Key Insight

- `git diff A B --stat` (2-dot) shows tip-to-tip divergence, not what the merge will do.
- `git diff A...B --stat` (3-dot) shows what B changed since the common ancestor. Use this for pre-merge assessment.

**Why use remote refs:** Local branches may be outdated. Always use `origin/` refs after fetching to ensure you're merging the latest remote version.
