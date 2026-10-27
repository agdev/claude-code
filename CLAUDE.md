# User Level instructions for claude code

## Response Style

- Write in clear, simple language: short sentences, no jargon unless necessary, no filler words. Use as few words as possible without losing detail, meaning, or intent. Use the terminology already in the context; when a new term is genuinely needed, say it is new and define it. When the user uses a term you do not fully understand, ask before assuming a definition.
- These wording rules apply to the final reply only, not to your reasoning.
- Completeness and precise technical terms come before brevity: never drop a finding, caveat, or exact technical term to save words.
- Separate fact from inference: verify claims before stating them when tools allow, and present anything unverified as unverified, never as fact.
- Claims about a document's contents come from reading it in this session — re-read or grep the actual file first, not memory. When comparing artifacts (skills, files, docs, plans) for overlap, contradiction, or duplication, read both in full and compare specific content claims, not titles, headings, or remembered structure.
- Explain scenario-first: lead findings, test results, and design consequences with the concrete story of what happens in the real system, step by step, in plain words. Define every term at first use; mechanism labels, severity ratings, and shorthand come only after the story, if at all. The bar: someone who didn't follow the internals could retell the scenario after one read.

## Web Search

- Use Brave Search MCP tools (`mcp__brave-search__*`, e.g. `brave_web_search`) for all web searches and research. Fall back to the built-in WebSearch tool only if Brave Search is unavailable or fails.

## Shell

- The Bash working directory persists across tool calls — never use a bare `cd`; use absolute paths and `git -C <absolute-path>`, so a directory change in one call cannot break the next.

## Workspace Folders

### Scratch & Working Folders

- Place all test files and snapshots in 'claude-code-test-ground' folder at the root of the project
- If 'claude-code-test-ground' folder does not exist, create it first
- When making code changes: create backup file of code before making changes and move it to 'claude-backup-files' folder at root directory
- If 'claude-backup-files' folder does not exist, create it first
- Temporary folders (/tmp, the session scratchpad) are only for your own intermediate files that can be recreated. Never put a product there: decisions, drafts of designs or decisions, reports, deliverables, or anything a later step or another session reads. This includes the paths you give subagents, and a subagent brief always names where its product goes.

### Documentation Folders (`claude-code-docs/`)

When creating documentation files at user's request:

#### Active Development Guides (`claude-code-docs/guides/`)

Place ongoing reference material in appropriate subcategory:

- `guides/setup/` - Setup and configuration guides
- `guides/reference/` - API and technical references
- `guides/testing/` - Testing documentation

#### Lessons Learned (`claude-code-docs/lessons/`)

Place ongoing lessons that you learned

#### Research (`claude-code-docs/research/`)

Place research that you did

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
- Design and decision work (designs, technical designs, their drafts, decision records) goes in the topic's spec folder (`specs/<topic>/`), next to its design files, from the first write.

### File Naming Conventions

- Use descriptive UPPERCASE filenames: `JWT_HELPER_QUICK_REFERENCE.md`
- Include "Last Updated" dates in document headers
- Cross-reference related documentation
- Update claude-code-docs/README.md when adding new files

## Design Principles

- Keep code and instructions as simple as possible, **NEVER** over engineer. Simplicity always wins
- **NEVER** defer tasks for efficiency under any circumstances
- When making technical decisions, **NEVER** give any weight to development cost. Instead, prefer quality, simplicity, robustness, scalability, and long term maintainability.
- **No Timelines in Plans** - When creating plans (plan files, task files, specs), **NEVER** include:
    - Timeline sections
    - Time estimates
    - Day-by-day breakdowns
    - Duration predictions
    - "Day 1", "Day 2" style phases

## Writing documents/instructions/designs
- Write counts and line numbers only where you absolutely must, they drift easily so avoid them where you can 

  Focus on: what needs to be done, in what order, and how to verify completion.

## Delegation-First Workflow

Keep the main session context clean. The main session is a **command center** — it coordinates, decides, and communicates with the user. Heavy lifting goes to subagents.

### Always Delegate

- **Codebase exploration** — use Explore agents for any research touching more than 1 file
- **Code reviews** — use code-reviewer agents, never review inline
- **Verification & testing** — delegate compile checks, lint, test runs to agents
- **Debugging investigation** — use debugger agents for root cause analysis
- **Plan/task file updates** — never update plan or task files directly in main session
- **Multi-file edits** — when changing more than 1 file, delegate to implementation agents

### Keep in Main Session

- User interaction and decisions
- Single-file read when you know the exact path and need it for an immediate decision
- Simple, confident single-file edit
- Coordinating and sequencing subagent work
- Summarizing agent results back to the user

### Parallel by Default

When delegating 2+ independent tasks, **always launch agents in parallel** (single message, multiple tool calls). Sequential delegation wastes time when tasks don't depend on each other.