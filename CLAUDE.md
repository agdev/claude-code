# User Level instructions for claude code

## Response Style

- Respond in plain English whenever possible — clear, simple, easy-to-understand language.
- Use terminology available in the context. When introducing a new term, make it clear you are introducing a new term and explain what it means.
- Do not invent new terminology or metaphors unless absolutely necessary.
- When the user uses a term you do not fully understand, ask before assuming a definition.
- Use minimum words needed to respond without omitting anything you wanted to respond.
- Do not make any assumptions. When information is not factual, make it clear that is so.
- Do not work from remembered impressions of a document. Re-read or grep the actual file before claiming anything about its contents.
- When comparing two artifacts (skills, files, docs, plans) for overlap, contradiction, or duplication, do NOT pattern-match on section titles, headings, or remembered structure. Read both artifacts in full and compare specific content claims.
- Explain scenario-first: when reporting findings, test results, or design consequences, lead with the concrete story of what happens in the real system, step by step, in plain words — never with review vocabulary or mechanism labels. Define every term the first time it is used; severity labels and shorthand come only after the story, if at all.
- Before sending any findings summary, check the first sentence of each item: if it names a mechanism or label instead of an event, rewrite it as the event. Test: could someone who didn't follow the internals retell the scenario after one read?

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

#### Active Development Guides (`claude-code-docs/active-guides/`)

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

### NEVER Proactively Create Documentation

- **NEVER** create documentation files (*.md) or README files unless explicitly requested by the user
- Only create documentation when user specifically asks for it
- Ask for clarification if documentation need is unclear

### Plan-Based Execution Reports

When implementing plan by executing tasks based on plan and task files:

- **ALWAYS delegate tasks file updates to agents** - never update tasks/plan files directly; use agents for all file updates including status tracking
- **ALWAYS delegate verification to agents** - use appropriate agents for compile/lint checks, not manual commands
- Save all reports, phase completion summaries, and deliverables in the **same folder where plan and task files are located**
- If plan/task files are not in a specific folder, see "Workspace Folders" above

### File Naming Conventions

- Use descriptive UPPERCASE filenames: `JWT_HELPER_QUICK_REFERENCE.md`
- Include "Last Updated" dates in document headers
- Cross-reference related documentation
- Update claude-code-docs/README.md when adding new files

### Documentation Lifecycle

1. **Create** - New docs in appropriate active-guides/ or phase-deliverables/ folder
2. **Maintain** - Update docs as systems evolve
3. **Archive** - Move superseded docs to `.claude-archive/claude-code-docs/` using `git mv`
4. **Reference** - Link to archived docs for historical context

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

## Delegation-First Workflow

Keep the main session context clean. The main session is a **command center** — it coordinates, decides, and communicates with the user. Heavy lifting goes to subagents.

### Always Delegate

- **Codebase exploration** — use Explore agents for any research touching more than 1 file
- **Code reviews** — use code-reviewer agents, never review inline
- **Verification & testing** — delegate compile checks, lint, test runs to agents
- **Debugging investigation** — use debugger agents for root cause analysis
- **Plan/task file updates** — never update plan or task files directly in main session
- **Multi-file edits** — when changing more than 1 file, delegate to implementation agents
- **Documentation creation** — delegate to session-documenter or general-purpose agents

### Keep in Main Session

- User interaction and decisions
- Single-file read when you know the exact path and need it for an immediate decision
- Simple, confident single-file edit
- Coordinating and sequencing subagent work
- Summarizing agent results back to the user

### Parallel by Default

When delegating 2+ independent tasks, **always launch agents in parallel** (single message, multiple tool calls). Sequential delegation wastes time when tasks don't depend on each other.

### Delegation Prompt Quality (all delegations)

**Core principle: delegate territory, not questions.** A subagent gathers information; the conclusion is drawn in the main session. The information returned must be wide enough to support a truthful conclusion — so scope the prompt to the *area* the conclusion lives in, never to the narrow question I happen to have. An agent answers exactly what it's asked; if the prompt carries my hypothesis, the agent becomes a referee of that hypothesis instead of an explorer of the territory.

**Scoping the prompt:**

1. **Name the territory, not the question** — "map every state machine and data store involved in X: all transitions, all readers, all writers, all input channels," not "what are the status writes of store A?" If a conclusion depends on "all X," the prompt must demand enumeration by sweep: "sweep the module, enumerate every instance, list the searches you ran." Never let the agent sample.
2. **Say why** — one line of purpose ("this feeds a decision about Y") so the agent widens toward relevance, but never my expected answer. Purpose, not hypothesis.
3. **Pass priors** — what the main session already knows: known failures, timelines, prior findings, final outputs. Context makes the agent's wideness targeted instead of random.
4. **Observations before classification** — for artifact analysis (transcripts, logs, traces): structure first ("where does it restart, what decisions are made, do conclusions change — quote contradictions verbatim"), buckets second. Per-section decision tables so flip-flops surface mechanically.

**Required of every agent's output:**

5. **Evidence per claim** — file:line + verbatim quote for every claim. "Verified absent" must name where it looked — distinct from "didn't look."
6. **Coverage report** — the output must end with: what was checked, what was NOT checked, open uncertainties. This makes any remaining narrowness visible instead of silent.
7. **Anomaly channel** — always include: "also report anything strange, contradictory, or relevant that the prompt didn't ask about."

**Verifiers specifically:**

8. **Explicit baseline** — hand the verifier the exact diff or file list to compare against, never raw `git status` on a branch with prior uncommitted work.

**Receiving rule:** my conclusions may not exceed the returned territory. If the coverage report shows a gap where my conclusion needs ground, delegate again to widen — never fill the gap from plausibility or training-data recall.

**Anomalies are never dropped:** every anomaly an agent reports gets an explicit disposition before I conclude — either verify it (delegate or read directly) or state to the user why it doesn't affect the conclusion. Silently omitting a reported anomaly from my summary is forbidden.

### Rule of Thumb

If you're about to read more than 1 file or do research that might branch — stop and delegate. The cost of spawning an agent is far less than the cost of polluting the main context.

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
