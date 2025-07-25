# Enhanced Markdown Format Specification

## Overview

This document defines the enhanced markdown format for task management that combines human readability (from task-lists.mdc) with embedded metadata (from claude-task-master) while remaining compatible with Claude Code's capabilities.

## Task ID System (T003 Complete)

### Format: `[T###]`
- **Pattern**: T followed by zero-padded 3-digit number
- **Examples**: `[T001]`, `[T042]`, `[T153]`
- **Scope**: Unique within a project/PRD context
- **Sequence**: Sequential assignment starting from T001

### Usage in Markdown
```markdown
- [ ] **[T001]** Task title (metadata)
- [x] **[T002]** Completed task (metadata)
```

### Reference Format
- **Dependencies**: `deps: T001,T002` (comma-separated, no spaces after commas)
- **Cross-references**: Use `T001` in plain text for readability
- **Breakdown indicators**: `→ See T001.1, T001.2` for subtasks

## Metadata Embedding Syntax (T004 Complete)

### Primary Task Format
```markdown
- [status] **[TID]** Task title (effort, deps: dependencies, complexity: score) [indicators]
```

**Components:**
- `[status]`: `[ ]` pending, `[x]` completed
- `**[TID]**`: Bold task ID for easy scanning
- `Task title`: Clear, actionable description
- `(effort, deps: TID1,TID2, complexity: N)`: Inline metadata
- `[indicators]`: ⚡ needs breakdown, 🔄 in progress, ⚠️ blocked

### Examples
```markdown
- [ ] **[T001]** Setup project configuration (2h, deps: none, complexity: 3)
- [ ] **[T002]** User authentication system (18h, deps: T001, complexity: 8) ⚡ *Needs breakdown*
- [x] **[T003]** Database schema design (6h, deps: T001, complexity: 5)
- [ ] **[T004]** API endpoints (12h, deps: T002,T003, complexity: 6) 🔄 *In progress*
```

### Metadata Fields
- **effort**: Time estimate (Nh for hours, Nd for days)
- **deps**: Dependencies as comma-separated task IDs
- **complexity**: 1-10 scale (1=trivial, 10=extremely complex)

### Special Indicators
- **⚡** Needs breakdown (complexity > 6)
- **🔄** Currently in progress
- **⚠️** Blocked by dependencies
- **✅** File completed (in Relevant Files section)
- **⚡** File to be created (in Relevant Files section)

## Main TASKS.md Template (T005 Complete)

```markdown
# [Project Name] Task List
Generated from: [source-file] | Updated: [timestamp]

## Task Summary
- **Total Tasks:** [N] | **Est. Effort:** [Nh] | **Complexity:** [N]H/[N]M/[N]L
- **Completed:** [N] ([%]%) | **In Progress:** [N] | **Future:** [N]

## Completed Tasks
- [x] **[T001]** Task title (effort, deps: dependencies, complexity: score)

## In Progress Tasks  
- [ ] **[T002]** Task title (effort, deps: dependencies, complexity: score) 🔄

## Future Tasks
- [ ] **[T003]** Task title (effort, deps: dependencies, complexity: score)
- [ ] **[T004]** Complex task title (effort, deps: dependencies, complexity: score) ⚡ *Needs breakdown*

## Implementation Plan

### Phase 1: Foundation ([timeframe])
Description of initial phase and key tasks

**Critical Path:** T001 → T002 → T003  
**Parallel Options:** T004 & T005 can run after T001  
**Estimated Duration:** [timeframe]

### Phase 2: Core Development ([timeframe])
Description of main development phase

### Phase 3: Testing & Polish ([timeframe])
Description of final phase

## Next Steps
1. **Start with [T###]** - [Title] (No dependencies, foundational)
2. **Review dependencies** - Ensure logical implementation order
3. **Set up environment** - [Specific setup requirements]

## Relevant Files
- [path/to/file] - Description ✅ (Completed)
- [path/to/file] - Description ⚡ (To be created)
- [path/to/file] - Description 🔄 (In progress)

## Task Details

### **[T###]** Complex Task Title
**Priority:** High/Medium/Low | **Complexity:** N/10 | **Est:** Nh  
**Dependencies:** [List of prerequisite tasks]  
**Status:** [Current status] → *[Action needed]*

**Requirements:**
- [Specific requirement 1]
- [Specific requirement 2]

**Acceptance Criteria:**
- [ ] [Specific measurable outcome]
- [ ] [Specific measurable outcome]

**Implementation Notes:**
[Technical guidance, research findings, considerations]

**Subtasks** (if broken down):
- [ ] **[T###.1]** Subtask 1 (effort, complexity: N)
- [ ] **[T###.2]** Subtask 2 (effort, complexity: N)

---
*Generated by Claude Code PRD Analysis*  
*Last Updated: [timestamp]*
```

## Individual Task File Format (T006 Complete)

```markdown
# Task [TID]: [Title]

**Project:** [Project Name]  
**Parent Task:** [Parent TID] ([Parent Title])  
**Priority:** High/Medium/Low  
**Complexity:** N/10  
**Estimated Effort:** Nh  
**Dependencies:** [List with explanations]  
**Status:** [Current status]

## Description
[Detailed description of what this task accomplishes and why it's needed]

## Context
[How this task fits into the larger feature/project scope]

## Requirements
[Detailed functional and technical requirements]

## Acceptance Criteria
- [ ] [Specific measurable outcome 1]
- [ ] [Specific measurable outcome 2]
- [ ] [Specific measurable outcome 3]

## Implementation Approach
[Technical approach, architecture decisions, key considerations]

### Key Components
- **[Component 1]**: [Description and purpose]
- **[Component 2]**: [Description and purpose]

### Technology Stack
- [Technology/Framework]: [Purpose and rationale]
- [Library/Tool]: [Purpose and rationale]

## Test Strategy
[How to validate this task is complete and working correctly]

### Test Types
- **Unit Tests**: [What to test at unit level]
- **Integration Tests**: [What to test at integration level]
- **Manual Testing**: [Manual validation steps]

## Implementation Notes
[Technical details, gotchas, references, research findings]

### Research Findings
- [Key insight from research]
- [Best practice or pattern to follow]
- [Security/performance consideration]

### External References
- [Documentation link]: [Description]
- [Stack Overflow/Blog post]: [Description]

## Dependencies

### Prerequisites
- **[TID]**: [Title] - [Why this is needed before current task]

### Enables
- **[TID]**: [Title] - [How completing this task enables that one]

## Subtasks
- [ ] **[TID.1]** [Subtask title] (effort, complexity: N)
  - [Brief description of subtask]
- [ ] **[TID.2]** [Subtask title] (effort, complexity: N)
  - [Brief description of subtask]

## Progress Tracking
- **Started:** [Date/time]
- **Last Updated:** [Date/time]
- **Completion:** [Percentage or milestone]

---
*Generated by Claude Code Task Breakdown*  
*Source: [PRD or parent task file]*  
*Task ID: [TID]*
```

## Complexity Scoring Criteria (T007 Complete)

### Scale: 1-10 (Fibonacci-inspired with clear breakpoints)

#### 1-2: Trivial
- **Time**: < 2 hours
- **Scope**: Single file, simple change
- **Dependencies**: None or minimal
- **Examples**: Update documentation, fix typo, simple configuration change

#### 3-4: Simple
- **Time**: 2-6 hours
- **Scope**: Few files, straightforward implementation
- **Dependencies**: 1-2 clear dependencies
- **Examples**: Add new API endpoint, create simple UI component, basic database migration

#### 5-6: Medium
- **Time**: 6-16 hours
- **Scope**: Multiple files, moderate complexity
- **Dependencies**: 2-4 dependencies with some complexity
- **Examples**: Feature with multiple components, integration with external API, complex UI workflow

#### 7-8: Complex (⚡ Auto-breakdown trigger)
- **Time**: 16-40 hours
- **Scope**: Multiple modules, significant complexity
- **Dependencies**: 4+ dependencies or complex relationships
- **Examples**: Authentication system, real-time features, data migration

#### 9-10: Very Complex (⚡ Mandatory breakdown)
- **Time**: 40+ hours
- **Scope**: Cross-cutting concerns, architectural changes
- **Dependencies**: Complex dependency web
- **Examples**: Complete system redesign, major framework migration, complex algorithms

### Assessment Factors
1. **Technical Complexity**: New technologies, complex algorithms, performance requirements
2. **Scope**: Number of files/modules affected, breadth of changes
3. **Dependencies**: Number and complexity of prerequisite tasks
4. **Risk**: Uncertainty, potential for blockers, external dependencies
5. **Testing**: Difficulty of validation and testing requirements

## Dependency Notation System (T008 Complete)

### Basic Format
```
deps: T001,T002,T003
```

### Advanced Notation (for complex relationships)
```
deps: T001(critical),T002(soft),T003(async)
```

**Types:**
- **No qualifier**: Standard dependency (must complete before starting)
- **(critical)**: Blocking dependency (cannot proceed without)
- **(soft)**: Preferred dependency (can start but better to wait)
- **(async)**: Parallel dependency (can run simultaneously)

### Dependency Validation Rules
1. **No Circular Dependencies**: T001 → T002 → T003 → T001 (invalid)
2. **Existence Check**: All referenced task IDs must exist
3. **Status Validation**: Dependencies should be completed or in-progress
4. **Logical Sequence**: Dependencies should make technical sense

### Dependency Visualization in Markdown
```markdown
## Dependency Graph
```
T001 → T002 → T004
T001 → T003 → T005
T004,T005 → T006
```

**Critical Path:** T001 → T002 → T004 → T006 (Total: 32h)
**Parallel Opportunities:** T002 & T003 can run after T001
**Bottlenecks:** T001 blocks multiple tasks, T006 is final integration point
```

## Parsing Guidelines for Commands

### Task ID Extraction
```regex
\*\*\[T(\d{3})\]\*\*\s+([^(]+)\s+\(([^)]+)\)
```
- Group 1: Task ID number
- Group 2: Task title
- Group 3: Metadata string

### Metadata Parsing
```regex
(\d+h),\s*deps:\s*([^,\s]+(?:,[^,\s]+)*),\s*complexity:\s*(\d+)
```
- Group 1: Effort (hours)
- Group 2: Dependencies (comma-separated)
- Group 3: Complexity score

### Status Indicators
- `⚡ *Needs breakdown*`: Complexity > 6, requires subtask generation
- `🔄 *In progress*`: Currently being worked on
- `⚠️ *Blocked*`: Cannot proceed due to unmet dependencies

## Format Evolution and Compatibility

### Version 1.0 (Current)
- Basic metadata embedding
- Task ID system
- Dependency notation
- Complexity scoring

### Future Enhancements
- Estimated dates and deadlines
- Assignee information
- Progress percentage
- Tag system for categorization
- Risk assessment indicators

### Backward Compatibility
- Commands should handle missing metadata gracefully
- Default values for missing complexity scores
- Flexible parsing for various formatting styles
- Clear error messages for format violations

This enhanced markdown format provides the perfect balance between human readability and machine parseability, enabling sophisticated task management while maintaining the simplicity that makes task-lists.mdc effective.