---
description: Convert PRD documents into structured task lists using Claude's AI analysis
allowed-tools: ["Read", "Write", "MultiEdit", "LS", "Bash", "WebSearch"]
---

# PRD to Tasks Command

When user executes `/project:prd-to-tasks <prd_file> <output_folder>`, analyze the PRD document at `$ARGUMENTS` and generate comprehensive task breakdown in `$ARGUMENTS`.

## Step 1: Input Validation and Setup

### Validate Arguments
- **PRD File**: Verify `$ARGUMENTS` exists and is readable (.md, .txt, .docx supported)
- **Output Folder**: Ensure `$ARGUMENTS` is accessible or can be created
- **File Format**: Check PRD file format and content structure

### Initialize Variables
- Set project name from PRD filename or content
- Generate timestamp for tracking
- Initialize task counter starting at T001
- Create output directory structure if needed

## Step 2: PRD Analysis Using Claude's AI

### Requirement Extraction
Using my built-in AI capabilities, analyze the PRD to extract:

**Core Requirements Analysis:**
- **Business Objectives**: What problem does this solve?
- **User Stories**: Who are the users and what do they need?
- **Functional Requirements**: What features must be implemented?
- **Technical Requirements**: What technologies, platforms, constraints?
- **Success Criteria**: How will success be measured?
- **Nice-to-Have Features**: Optional enhancements

**Technical Analysis:**
- **System Architecture**: Frontend, backend, database, external services
- **Technology Stack**: Frameworks, libraries, platforms mentioned
- **Integration Points**: External APIs, third-party services
- **Performance Requirements**: Speed, scale, availability needs
- **Security Considerations**: Authentication, authorization, data protection

### Complexity Assessment Framework
For each identified requirement, assess complexity using these factors:

**Technical Complexity (1-10):**
- **1-2**: Simple CRUD operations, basic UI components
- **3-4**: Standard API integration, moderate UI complexity
- **5-6**: Complex business logic, multiple system integration
- **7-8**: Real-time features, authentication systems, complex algorithms
- **9-10**: Distributed systems, advanced ML/AI, major architectural changes

**Scope Analysis:**
- **Files/Modules**: How many parts of the system are affected?
- **Dependencies**: How many other components depend on this?
- **Testing**: How complex is validation and testing?
- **Documentation**: How much explanation and documentation needed?

## Step 3: Task Generation and Structuring

### Task Creation Algorithm
1. **Extract Discrete Features**: Break PRD into implementable features
2. **Generate Task Titles**: Clear, actionable task descriptions
3. **Assess Complexity**: Use complexity framework for each task
4. **Infer Dependencies**: Determine technical and logical prerequisites
5. **Assign Priorities**: Based on business impact and technical dependencies
6. **Estimate Effort**: Time estimates based on complexity and scope

### Task Categorization
Organize tasks into these categories:

**Development Tasks:**
- Frontend components and UI
- Backend APIs and business logic
- Database design and implementation
- Integration with external services

**Infrastructure Tasks:**
- Environment setup and configuration
- Deployment and DevOps
- Security configuration
- Performance optimization

**Quality Assurance Tasks:**
- Unit testing strategies
- Integration testing
- End-to-end testing
- Security testing

**Documentation Tasks:**
- API documentation
- User guides
- Technical documentation
- Architecture decisions

### Dependency Inference Logic
Automatically infer dependencies using these rules:

**Technical Dependencies:**
- Database schema → API endpoints → Frontend components
- Authentication → User-specific features
- Core services → Dependent features
- Configuration → Implementation

**Logical Dependencies:**
- User registration → User profile management
- Payment setup → Purchase flows
- Admin features → User features (usually)

**Resource Dependencies:**
- Shared libraries → Features using them
- External service setup → Integration features

## Step 4: Enhanced Markdown Generation

### Create Main TASKS.md File
Generate the primary task list using the enhanced markdown format:

```markdown
# $ARGUMENTS Task List
Generated from: $ARGUMENTS | Updated: [timestamp]

## Task Summary
- **Total Tasks:** [count] | **Est. Effort:** [total_hours]h | **Complexity:** [high_count]H/[med_count]M/[low_count]L
- **Completed:** 0 (0%) | **In Progress:** 0 | **Future:** [count]

## Completed Tasks
(Initially empty)

## In Progress Tasks  
(Initially empty)

## Future Tasks
[Generated task list with metadata]

## Implementation Plan
[Phase-based development roadmap]

## Next Steps
1. **Start with [first_task_id]** - [title] (No dependencies, foundational)
2. **Review dependencies** - Ensure logical implementation order
3. **Set up environment** - [specific setup requirements from PRD]

## Relevant Files
[Inferred file structure based on requirements]

## Task Details
[Detailed sections for complex tasks]
```

### Task Complexity Breakdown Trigger
For tasks with complexity > 6:
- Add ⚡ indicator in task list
- Mark as "Needs breakdown" 
- Automatically call task-breakdown command for detailed subtasks
- Merge breakdown results into main task list

### Priority Assignment Logic
**High Priority:**
- Core functionality blocking other features
- User-facing features mentioned as primary requirements
- Security and authentication components
- Critical infrastructure setup

**Medium Priority:**
- Important features enhancing user experience
- Performance optimizations
- Integration with external services
- Comprehensive testing strategies

**Low Priority:**
- Nice-to-have features
- Advanced optimizations
- Extensive documentation
- Future enhancement preparation

## Step 5: Advanced Analysis Features

### Research Enhancement (Optional)
If WebSearch is available, enhance task generation with:
- **Technology Best Practices**: Current recommendations for mentioned technologies
- **Security Standards**: Industry security requirements for the domain
- **Performance Patterns**: Optimization strategies for the use case
- **Integration Guides**: Documentation for mentioned external services

### Effort Estimation Algorithm
Calculate time estimates based on:
- **Complexity Score**: Base hours = complexity × 2-4 hours
- **Technology Familiarity**: Add 50% for new/complex technologies
- **Integration Complexity**: Add time for external integrations
- **Testing Requirements**: Add 30-50% for comprehensive testing
- **Documentation Needs**: Add time for technical documentation

### Risk Assessment
Identify and flag potential risks:
- **High Complexity Tasks**: Complexity > 7, recommend breaking down
- **External Dependencies**: Third-party services, APIs
- **Technology Risks**: New or complex technologies
- **Timeline Risks**: Tasks that could become bottlenecks

## Step 6: Output File Generation

### Primary Outputs
1. **`TASKS.md`**: Main enhanced markdown task list
2. **`task-breakdown-queue.md`**: List of tasks needing detailed breakdown
3. **`project-analysis.md`**: PRD analysis summary and insights

### Automatic Task Breakdown Integration
For tasks marked as complex (complexity > 6):
1. Create entry in task-breakdown-queue.md
2. Automatically call `/project:task-breakdown` for each complex task
3. Merge breakdown results into main TASKS.md
4. Update task numbering and dependencies consistently

### File Structure Creation
Based on PRD analysis, suggest project file structure in Relevant Files:
```markdown
## Relevant Files
- src/[component]/ - [Component description] ⚡ (To be created)
- tests/[component].test.js - [Test description] ⚡ (To be created)
- docs/[feature].md - [Documentation description] ⚡ (To be created)
```

## Step 7: Quality Validation

### Validation Checks
- **Task Completeness**: All PRD requirements covered
- **Dependency Validation**: No circular dependencies
- **Effort Realism**: Time estimates are reasonable
- **Format Compliance**: Follows enhanced markdown specification
- **Task Actionability**: Each task is implementable independently

### Error Handling
- **Invalid PRD Path**: Show clear error and usage example
- **Inaccessible Output**: Suggest alternative paths or permission fixes
- **Empty/Malformed PRD**: Request clearer requirements document
- **Analysis Failures**: Provide partial results with warnings

## Step 8: Success Reporting

Generate completion summary:
```markdown
## PRD Analysis Complete

**Source:** $ARGUMENTS
**Output:** $ARGUMENTS
**Generated:** [timestamp]

**Results:**
- Tasks Generated: [count]
- Complex Tasks (breakdown needed): [count]
- Total Estimated Effort: [hours]h
- Implementation Phases: [count]

**Next Actions:**
1. Review generated task list for accuracy
2. Complex tasks will be automatically broken down
3. Begin with: [first_task_id] - [title]
```

## Integration with task-breakdown Command

When complex tasks are detected:
1. **Queue Complex Tasks**: Create list of tasks needing breakdown
2. **Auto-Execute Breakdown**: Call task-breakdown for each complex task
3. **Merge Results**: Integrate subtasks into main task list
4. **Update Dependencies**: Adjust dependencies based on new subtasks
5. **Renumber Tasks**: Maintain consistent task ID sequence

This command transforms PRDs into actionable, well-structured task lists using Claude Code's built-in AI analysis capabilities, providing the foundation for systematic project implementation.