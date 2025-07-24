# Claude Code Task Management Slash Commands

Custom slash commands for Claude Code that transform Product Requirements Documents (PRDs) into structured, actionable task lists using Claude's built-in AI analysis capabilities.

## Overview

These commands replace external task management tools by leveraging Claude Code's native AI capabilities to provide sophisticated project planning and task breakdown functionality directly within your development workflow.

## Available Commands

### `/project:prd-to-tasks <prd_document> <output_folder>`

Converts Product Requirements Documents into comprehensive task structures with intelligent analysis and breakdown.

**Usage:**
```bash
/project:prd-to-tasks ./docs/requirements.md ./tasks/project
```

**What it does:**
- Analyzes PRD using Claude's AI capabilities
- Extracts requirements, user stories, and technical specifications
- Generates structured task hierarchy with dependencies
- Creates comprehensive task breakdown with complexity analysis
- Outputs both JSON database and markdown task lists

### `/project:task-breakdown <input_source> <output_folder>`

Breaks down complex tasks or requirements into detailed, actionable subtasks with intelligent decomposition.

**Usage:**
```bash
/project:task-breakdown ./requirements/feature.md ./tasks/feature-breakdown
```

**What it does:**
- Analyzes complex tasks or requirements
- Uses domain-aware breakdown strategies
- Generates detailed subtask hierarchies
- Provides implementation sequencing and dependency analysis
- Creates comprehensive breakdown reports

## Features

### 🧠 AI-Powered Analysis
- **Smart Requirement Extraction**: Automatically identifies core features, user stories, and technical requirements
- **Intelligent Task Generation**: Creates actionable tasks from natural language descriptions
- **Complexity Assessment**: AI-driven complexity scoring (1-10) with breakdown recommendations
- **Dependency Inference**: Automatically detects task dependencies and prerequisites

### 📊 Structured Output
- **JSON Task Database**: Complete task metadata with hierarchical relationships
- **Markdown Task Lists**: Human-readable task organization following established patterns
- **Individual Task Files**: Detailed files for complex tasks requiring focused work
- **Implementation Roadmaps**: Phased development plans with critical path analysis

### 🔄 Intelligent Task Management
- **Hierarchical Structure**: Tasks → Subtasks → Sub-subtasks with clear relationships
- **Priority Assignment**: Business impact and technical complexity-based prioritization
- **Effort Estimation**: Realistic time estimates based on complexity analysis
- **Quality Validation**: Comprehensive acceptance criteria and test strategies

## Generated Output Structure

### Task JSON Schema
```json
{
  "id": 1,
  "title": "User Authentication System",
  "description": "Implement secure user authentication with OAuth2",
  "status": "pending",
  "priority": "high",
  "complexity": 8,
  "estimatedHours": 24,
  "dependencies": [2, 5],
  "category": "development",
  "tags": ["backend", "security", "authentication"],
  "details": "Comprehensive implementation requirements...",
  "testStrategy": "Unit tests, integration tests, security testing...",
  "acceptanceCriteria": [
    "Users can register with email/password",
    "OAuth2 integration with Google/GitHub works"
  ],
  "subtasks": [
    {
      "id": 1,
      "title": "OAuth2 Configuration Setup",
      "complexity": 4,
      "estimatedHours": 4
    }
  ]
}
```

### Markdown Task List Format
```markdown
# Feature Implementation
Auto-generated from: {source_file}
Generated: {timestamp}

## Project Overview
Summary of requirements and scope

## Task Summary
- **Total Tasks:** 12
- **Estimated Effort:** 156 hours
- **Complexity Distribution:** 3 High, 5 Medium, 4 Low

## Development Tasks (8 tasks, 112 hours)

### 🔧 **[T001]** User Authentication System (High Priority, 24h)
**Dependencies:** T002 (Database Setup), T003 (Security Config)
**Complexity:** 8/10

Implement secure user authentication with OAuth2 support...

**Subtasks:**
- [ ] OAuth2 Configuration Setup (4h)
- [ ] JWT Token Management (6h)
- [ ] User Registration Flow (8h)

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
Core infrastructure and database setup

### Phase 2: Core Features (Week 3-4)
Main functionality implementation

## Next Steps
1. **Start with T002** - Database setup (no dependencies)
2. **Review dependencies** - Ensure logical order
3. **Set up environment** - Development infrastructure

## Relevant Files
- src/auth/oauth.js - OAuth2 implementation ⚡ (To be created)
- tests/auth.test.js - Authentication tests ⚡ (To be created)
```

## Quick Start Example

### 1. Create a test PRD
```markdown
# Chat Application Requirements
Build a real-time chat app with user authentication and channels.

## Core Features
- User registration and authentication
- Real-time messaging with WebSocket
- Chat channels and direct messaging
- Message history and search
```

### 2. Generate tasks from PRD
```bash
/project:prd-to-tasks ./test-prd.md ./chat-tasks
```

### 3. Break down complex tasks
```bash
/project:task-breakdown ./chat-tasks/tasks.json ./detailed-tasks
```

## Advanced Features

### Complexity-Based Breakdown
- Tasks with complexity > 6 automatically generate subtasks
- Intelligent subtask count based on complexity score
- Recursive breakdown for deeply complex requirements

### Domain-Aware Analysis
- **Frontend**: Components, state management, styling, routing
- **Backend**: APIs, authentication, database models, business logic
- **Testing**: Unit tests, integration tests, E2E testing
- **DevOps**: Configuration, deployment, monitoring

### Smart Dependency Management
- Automatic dependency inference
- Circular dependency detection and resolution
- Critical path identification
- Parallel execution opportunity detection

### Implementation Sequencing
- Priority-based task ordering
- Dependency-aware scheduling
- Phase-based development planning
- Risk assessment and mitigation

## Command Structure

Both commands are stored as markdown files in `.claude/commands/`:
- `.claude/commands/prd-to-tasks.md` - PRD analysis and task generation
- `.claude/commands/task-breakdown.md` - Task decomposition and breakdown

Each command includes:
- Detailed processing steps
- AI analysis instructions
- Output format specifications
- Error handling procedures
- Quality validation checks

## Integration with Development Workflow

### 1. Planning Phase
```bash
# Convert business requirements to technical tasks
/project:prd-to-tasks ./docs/business-requirements.md ./project-tasks
```

### 2. Analysis Phase
```bash
# Break down complex technical tasks
/project:task-breakdown ./project-tasks/tasks.json ./detailed-implementation
```

### 3. Implementation Phase
- Follow generated task sequence
- Use individual task files for implementation guidance
- Update task status as work progresses

### 4. Review Phase
- Validate completed tasks against acceptance criteria
- Use generated test strategies for quality assurance

## Benefits Over External Tools

### Native Integration
- No external dependencies or API keys required
- Uses Claude Code's built-in AI capabilities
- Direct integration with your development environment

### Contextual Intelligence
- Understands your specific project context
- Adapts to your codebase patterns and conventions
- Provides relevant technical recommendations

### Structured Output
- Follows established task management patterns
- Creates both human-readable and machine-processable formats
- Maintains consistency across projects

### Quality Assurance
- Built-in validation and quality checks
- Comprehensive test strategy generation
- Risk assessment and mitigation planning

## Files Structure

```
.claude/
└── commands/
    ├── prd-to-tasks.md     # PRD analysis command
    └── task-breakdown.md   # Task breakdown command

Generated Output:
├── tasks.json              # Master task database
├── TASKS.md               # Structured task list
├── task-{id}.md           # Individual task files
├── BREAKDOWN.md           # Breakdown analysis (task-breakdown only)
└── complexity-report.md   # Complexity analysis
```

## Success Criteria

Commands succeed when:
1. **Complete Analysis**: All requirements transformed into actionable tasks
2. **Realistic Estimates**: Time estimates within reasonable accuracy ranges
3. **Clear Dependencies**: Logical implementation sequences established
4. **Quality Standards**: All tasks include acceptance criteria and test strategies
5. **Implementation Ready**: Tasks provide sufficient detail for independent execution

These slash commands provide enterprise-grade project planning capabilities directly within Claude Code, eliminating the need for external task management tools while leveraging Claude's sophisticated AI analysis capabilities.