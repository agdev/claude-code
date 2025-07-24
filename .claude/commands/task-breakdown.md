---
description: Break down complex tasks into detailed, actionable subtasks with intelligent analysis
allowed-tools: ["Read", "Write", "MultiEdit", "LS", "Bash", "WebSearch"]
---

# Task Breakdown Command

When user executes `/project:task-breakdown <task_source> <output_folder>`, analyze the input source at `$ARGUMENTS` and generate detailed task breakdown in `$ARGUMENTS`.

## Step 1: Input Source Analysis

### Supported Input Types
- **Existing Task Files**: TASKS.md or individual task files
- **Task Descriptions**: Plain text descriptions of features/requirements
- **PRD Sections**: Specific sections of larger requirement documents
- **Complex Task Entries**: Single tasks marked for breakdown
- **JSON Task Data**: Task data from previous analyses

### Input Processing
Read and analyze `$ARGUMENTS` to:
- **Identify Content Type**: Determine input format and structure
- **Extract Task Information**: Get task title, description, complexity, existing metadata
- **Assess Breakdown Scope**: Understand what level of detail is needed
- **Gather Context**: Understand how this fits into larger project

### Context Gathering
- **Project Context**: What type of project/application is this?
- **Technology Stack**: What technologies are mentioned or implied?
- **Existing Tasks**: Are there related tasks that provide context?
- **Dependencies**: What other tasks or components are involved?

## Step 2: Intelligent Task Decomposition

### Decomposition Strategy Selection
Based on task analysis, choose appropriate breakdown strategy:

#### Strategy 1: Technical Domain Breakdown
**Use when**: Task involves multiple technical areas
**Approach**: Break by technical components
- **Frontend**: UI components, state management, routing, styling
- **Backend**: API endpoints, business logic, data processing
- **Database**: Schema design, queries, migrations, optimization
- **DevOps**: Configuration, deployment, monitoring
- **Testing**: Unit tests, integration tests, end-to-end tests

#### Strategy 2: User Journey Breakdown
**Use when**: Task represents user-facing functionality
**Approach**: Break by user interaction flow
- **Entry Points**: How users access the feature
- **Core Actions**: Primary user interactions
- **Data Flow**: Information processing and storage
- **Feedback**: User notifications and responses
- **Edge Cases**: Error handling and validation

#### Strategy 3: Implementation Phase Breakdown
**Use when**: Task represents a complete feature or system
**Approach**: Break by development phases
- **Foundation**: Core setup and infrastructure
- **Core Implementation**: Main functionality
- **Integration**: Connecting with other systems
- **Validation**: Testing and quality assurance
- **Documentation**: User and technical documentation

#### Strategy 4: Complexity-Based Breakdown
**Use when**: Task is extremely complex (complexity 9-10)
**Approach**: Break by complexity reduction
- **Research Phase**: Understanding requirements and approach
- **Proof of Concept**: Basic implementation to validate approach
- **Core Implementation**: Main development work
- **Optimization**: Performance and quality improvements
- **Integration**: Connecting with existing systems

### Subtask Generation Algorithm

#### For Complexity 7-8 Tasks: Generate 4-6 Subtasks
1. **Analyze Core Components**: Identify 3-5 main functional areas
2. **Add Infrastructure**: Include setup, configuration, testing
3. **Consider Integration**: Add subtasks for connecting with other systems
4. **Include Validation**: Add testing and quality assurance subtasks

#### For Complexity 9-10 Tasks: Generate 6-8 Subtasks
1. **Research and Planning**: Understanding and approach validation
2. **Core Component Breakdown**: 3-4 main implementation areas
3. **Integration Subtasks**: Multiple integration points
4. **Testing Strategy**: Comprehensive testing approach
5. **Documentation**: Technical and user documentation
6. **Performance/Security**: Specialized requirements

### Subtask Complexity Assessment
Each generated subtask gets its own complexity score:
- **Original Task Complexity 7**: Subtasks typically 3-5
- **Original Task Complexity 8**: Subtasks typically 4-6
- **Original Task Complexity 9**: Subtasks typically 5-7
- **Original Task Complexity 10**: Subtasks typically 6-8

## Step 3: Dependency Analysis and Sequencing

### Subtask Dependency Inference
Automatically determine dependencies between subtasks:

**Technical Dependencies:**
- Database setup → API development → Frontend implementation
- Authentication setup → User-specific features
- Core services → Features that depend on them
- Testing frameworks → Test implementation

**Logical Dependencies:**
- Research → Implementation
- Foundation → Advanced features
- Individual components → Integration
- Implementation → Testing

**Resource Dependencies:**
- Shared libraries → Components using them
- Configuration → Implementation that needs it
- External services → Integration features

### Critical Path Analysis
Identify the longest sequence of dependent subtasks:
1. **Map All Dependencies**: Create dependency graph
2. **Calculate Path Lengths**: Find longest chain
3. **Identify Bottlenecks**: Tasks that block multiple others
4. **Find Parallel Opportunities**: Tasks that can run simultaneously

### Implementation Sequencing
Recommend optimal order based on:
- **Dependency Satisfaction**: Prerequisites completed first
- **Risk Mitigation**: High-risk tasks early for validation
- **Resource Optimization**: Parallel work when possible
- **Milestone Planning**: Logical groupings for progress tracking

## Step 4: Enhanced Subtask Details

### Generate Comprehensive Subtask Information

For each subtask, create:

#### Basic Information
- **Subtask ID**: T###.# format (e.g., T005.1, T005.2)
- **Title**: Clear, actionable description
- **Description**: 2-3 sentence explanation
- **Complexity**: 1-8 scale (subtasks shouldn't exceed 8)
- **Effort**: Time estimate in hours
- **Dependencies**: Other subtasks or external tasks

#### Implementation Guidance
- **Technical Approach**: Specific implementation strategy
- **Key Components**: What needs to be built/configured
- **Technologies**: Specific tools, frameworks, libraries
- **Acceptance Criteria**: Measurable completion indicators
- **Testing Strategy**: How to validate completion

#### Research Enhancement
If WebSearch is available, enhance each subtask with:
- **Best Practices**: Current industry recommendations
- **Implementation Patterns**: Proven approaches for this type of work
- **Common Pitfalls**: Known issues and how to avoid them
- **Documentation**: Links to relevant guides and references

## Step 5: Generate Breakdown Outputs

### Primary Output: BREAKDOWN.md
Create comprehensive breakdown analysis:

```markdown
# Task Breakdown Analysis
Source: $ARGUMENTS | Generated: [timestamp]

## Original Task
**[T###]** [Original task title]
**Complexity:** [score]/10 | **Est. Effort:** [hours]h
**Breakdown Strategy:** [strategy used]

[Original task description and requirements]

## Breakdown Summary
- **Strategy Used:** [technical-domain|user-journey|implementation-phase|complexity-based]
- **Reasoning:** [Why this strategy was chosen]
- **Total Subtasks Generated:** [count]
- **Complexity Reduction:** [original] → [average subtask complexity]

## Subtask Breakdown

### **[T###.1]** [Subtask Title] (Priority: [level], [hours]h, Complexity: [score])
**Dependencies:** [list]
**Category:** [development|testing|documentation|infrastructure]

**Description:** [What this subtask accomplishes]

**Implementation Approach:**
- [Technical approach and key considerations]
- [Specific components to build/configure]

**Acceptance Criteria:**
- [ ] [Specific measurable outcome]
- [ ] [Specific measurable outcome]

**Implementation Notes:**
[Technical details, research findings, best practices]

### [Additional subtasks...]

## Implementation Roadmap

### Recommended Sequence
1. **Start with:** [T###.#] - [title] (Foundation, no dependencies)
2. **Then:** [T###.#] - [title] (Builds on foundation)
3. **Parallel Options:** [T###.#] & [T###.#] can run simultaneously
4. **Integration:** [T###.#] - [title] (Combines components)
5. **Validation:** [T###.#] - [title] (Testing and quality assurance)

### Critical Path Analysis
**Longest Path:** [T###.#] → [T###.#] → [T###.#] (Total: [hours]h)
**Bottlenecks:** [T###.#] blocks [count] other subtasks
**Parallel Opportunities:** [count] subtasks can run in parallel

### Phase Planning
#### Phase 1: Foundation ([timeframe])
- [List of foundational subtasks]
- **Goal:** [What this phase achieves]

#### Phase 2: Core Implementation ([timeframe])
- [List of main implementation subtasks]
- **Goal:** [What this phase achieves]

#### Phase 3: Integration & Testing ([timeframe])
- [List of integration and testing subtasks]
- **Goal:** [What this phase achieves]

## Risk Assessment
### High-Risk Subtasks
- **[T###.#]**: [Risk description and mitigation strategy]

### External Dependencies
- [External service/API]: Required for [T###.#]
- [Technology/Framework]: Learning curve for [T###.#]

### Technical Challenges
- [Challenge description]: [Mitigation approach]

## Quality Assurance Strategy
### Testing by Subtask
- **[T###.#]**: [Testing approach]
- **[T###.#]**: [Testing approach]

### Integration Testing
- **Between [T###.#] & [T###.#]**: [Integration test strategy]
- **End-to-End Testing**: [Overall system validation]
```

### Individual Subtask Files
For complex subtasks (complexity > 5), generate individual files:

```markdown
# Subtask [T###.#]: [Title]

**Parent Task:** [T###] ([Parent Title])
**Priority:** [High/Medium/Low]
**Complexity:** [score]/10
**Estimated Effort:** [hours]h
**Dependencies:** [List with explanations]
**Status:** Pending

## Description
[Detailed description of what this subtask accomplishes]

## Context
[How this subtask fits into the parent task and larger project]

## Requirements
[Specific functional and technical requirements]

## Implementation Approach
[Technical approach, architecture decisions, key considerations]

## Acceptance Criteria
- [ ] [Specific measurable outcome]
- [ ] [Specific measurable outcome]

## Test Strategy
[How to validate this subtask is complete and working]

## Implementation Notes
[Technical details, research findings, best practices]

## Dependencies
### Prerequisites
- **[T###.#]**: [Title] - [Why needed]

### Enables
- **[T###.#]**: [Title] - [How this enables that]

---
*Generated by Claude Code Task Breakdown*
*Parent: [T###]*
```

## Step 6: Integration with Main Task List

### Update Parent Task
If breakdown is called from prd-to-tasks:
1. **Update Complexity Status**: Mark parent as "broken down"
2. **Add Subtask References**: Link to generated subtasks
3. **Update Dependencies**: Adjust based on subtask dependencies
4. **Merge into TASKS.md**: Integrate breakdown into main task list

### Maintain Task Numbering
- **Subtask IDs**: Use parent.child format (T005.1, T005.2)
- **Sequential Numbering**: Maintain order within parent task
- **Cross-References**: Update dependencies to reference subtasks
- **Consistent Format**: Follow enhanced markdown specification

## Step 7: Validation and Quality Checks

### Breakdown Quality Validation
- **Coverage**: All aspects of original task addressed
- **Granularity**: Subtasks are 2-8 hour chunks
- **Dependencies**: Logical and implementable sequence
- **Testability**: Each subtask has clear validation criteria
- **Completeness**: Breakdown adds up to original task scope

### Dependency Validation
- **No Circular Dependencies**: Validate dependency graph
- **Logical Sequence**: Dependencies make technical sense
- **External Dependencies**: All external requirements identified
- **Resource Conflicts**: No impossible parallel requirements

## Step 8: Success Reporting

Generate completion summary:
```markdown
## Task Breakdown Complete

**Source:** $ARGUMENTS
**Output:** $ARGUMENTS
**Generated:** [timestamp]

**Results:**
- Original Task: [T###] (Complexity: [score])
- Subtasks Generated: [count]
- Complexity Reduction: [original] → [avg_subtask]
- Total Effort: [hours]h
- Implementation Phases: [count]

**Files Created:**
- BREAKDOWN.md - Comprehensive breakdown analysis
- [Individual subtask files for complex subtasks]

**Next Actions:**
1. Review breakdown for accuracy and completeness
2. Begin with: [T###.#] - [title] (Foundation task)
3. Follow recommended implementation sequence
```

This command provides sophisticated task decomposition using Claude Code's built-in AI analysis, enabling detailed project planning and systematic implementation of complex requirements.