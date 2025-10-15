---
name: feature-desing-plan-orchestrator
description: Orchestrates researcher and feature-designer agents to design and plan feature implementation with comprehensive research and user-focused design
model: opus
---

# Feature Development with Research & Design

Orchestrates the researcher and feature-designer agents to thoroughly research, design, and plan feature implementation with a focus on user value and practical solutions.

## Usage

```
/feature-development <feature_description>
```

## Workflow

### Phase 1: Comprehensive Research (researcher)

The researcher agent will:

- Parse the feature request and understand requirements
- Examine existing codebase for current patterns, dependencies, and architecture
- Research official documentation, standards, and proven implementations
- Investigate multiple aspects of the feature simultaneously
- Provide structured analysis with implementation options

**Expected Output:**

- Context summary of local codebase findings
- Industry best practices and proven approaches  
- 2-3 viable implementation approaches with clear trade-offs
- Required dependencies, packages, and configuration changes
- Performance, security, and maintainability considerations

### Phase 2: User-Focused Feature Design (feature-designer)

The feature-designer agent will:

- Analyze research findings to understand technical constraints and opportunities
- Define the core user problem being solved
- Design minimum viable feature that delivers maximum user value
- Create practical implementation scope that balances user needs with technical reality
- Establish success metrics and user value measurements

**Expected Output:**

- Clear user problem statement with pain points identified
- Feature solution focused on user workflows and interactions
- Minimum viable implementation scope for maximum user value
- User experience trade-offs and feature limitations
- Success metrics based on user behavior and value delivery

### Phase 3: Integration & Planning

The orchestrator will:

- Synthesize research findings with feature design
- Identify any gaps between technical possibilities and user needs
- Create implementation roadmap based on user value priorities
- Document technical requirements informed by research
- Establish development approach that balances user value with technical quality

## Agent Coordination

### Research → Design Flow

1. **Research Foundation**: Researcher provides technical landscape and implementation options
2. **Design Overlay**: Feature-designer uses research to design user-focused solution
3. **Gap Analysis**: Identify misalignments between technical capabilities and user needs
4. **Iterative Refinement**: Refine design based on technical constraints from research

### Quality Gates

- **Research Quality**: Authoritative sources, comprehensive local analysis, clear options
- **Design Quality**: Solves real user problems, practical implementation scope, measurable value
- **Integration Quality**: Research informs design decisions, no technical impossibilities

## Example Usage

```bash
/feature-development "User dashboard with real-time notifications and customizable widgets"
```

Expected flow:

1. **Research Phase**:
   - Analyze existing dashboard/notification patterns in codebase
   - Research real-time technologies (WebSockets, SSE, polling)
   - Investigate widget frameworks and customization patterns
   - Review performance implications and browser compatibility

2. **Design Phase**:
   - Define user problem: "Users need personalized, actionable information at a glance"
   - Design core workflows: dashboard viewing, notification management, widget customization
   - Scope MVP: basic widgets, simple notifications, user preferences
   - Establish metrics: time to key information, notification engagement, customization usage

3. **Integration**:
   - Match technical approaches to user value priorities
   - Create implementation plan prioritizing highest-value user features
   - Document technical architecture supporting user experience goals

## Success Criteria

- **Comprehensive Research**: Technical landscape fully understood with viable options identified
- **User-Focused Design**: Clear user problem solved with practical, valuable solution
- **Actionable Plan**: Implementation roadmap that delivers user value efficiently
- **Quality Foundation**: Research-informed design ready for development handoff

This command ensures features are both technically sound and user-valuable by combining thorough research with user-focused design thinking.
