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
