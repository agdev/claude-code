# Project Structure

## Root Directory
```
claude-code/
├── .claude/                  # Claude Code configuration
│   ├── commands/            # Slash command definitions
│   │   ├── prd-to-tasks.md  # PRD analysis command
│   │   └── task-breakdown.md # Task breakdown command
│   └── settings.local.json  # Local permissions and settings
├── .serena/                 # Serena MCP configuration
│   ├── memories/            # AI memory files
│   └── project.yml          # Project configuration
├── command/                 # Command rules and guidelines
│   └── task-lists.md        # Task list management rules
├── specs/                   # Project specifications
│   └── serena-test/         # Serena testing area
├── session/                 # Session logs and history
├── CLAUDE.md                # Project instructions for Claude
├── README.md                # Project documentation
├── LICENSE                  # MIT license
└── test-prd.md              # Test PRD for development
```

## Key Directories
- **`.claude/commands/`** - Slash command implementations
- **`command/`** - MDC format command rules  
- **`specs/`** - Project specifications and analysis
- **`.serena/memories/`** - AI memory storage
- **`session/`** - Development session logs

## Generated Output (when commands run)
- `tasks.json` - Master task database
- `TASKS.md` - Structured task lists
- `task-{id}.md` - Individual task files
- `BREAKDOWN.md` - Task breakdown analysis
- `complexity-report.md` - Complexity analysis