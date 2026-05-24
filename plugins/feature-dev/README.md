# Feature Development Plugin

A comprehensive, structured workflow for feature development with collaborative discovery, specialized agents for codebase exploration, architecture design, and quality review.

## Overview

The Feature Development Plugin provides a systematic 7-phase approach to building new features. Instead of jumping straight into code, it first turns the initial idea into an approved design seed, then uses that seed to guide codebase exploration, clarifying questions, architecture design, implementation, and review.

## Philosophy

Building features requires more than writing code. You need to:

- **Understand user intent** before choosing implementation details
- **Bound the scope** so the work stays focused
- **Understand the codebase** before making changes
- **Ask questions** to clarify ambiguous requirements
- **Design thoughtfully** before implementing
- **Review for quality** after building

This plugin embeds these practices into a structured workflow that runs when you use the `/feature-dev` command.

## Command: `/feature-dev`

Launches a guided feature development workflow with 7 distinct phases.

**Usage:**

```bash
/feature-dev Add user authentication with OAuth
```

Or simply:

```bash
/feature-dev
```

The command will guide you through the process interactively.

## The 7-Phase Workflow

### Phase 1: Discovery & Design Seed

**Goal**: Transform the initial idea into a clear, bounded design seed that makes later codebase exploration targeted.

**What happens:**

- Creates a todo list for the workflow
- Reads lightweight project context before asking detailed questions
- Restates the idea as a problem, target workflow, expected outcome, constraints, and non-goals
- Detects if the request should be decomposed into smaller slices
- Asks focused clarifying questions one at a time
- Proposes 2-3 high-level directions with trade-offs and a recommendation
- Presents a **Design Seed** and waits for your approval before moving to codebase exploration

**Example:**

```text
You: /feature-dev Add caching
Claude: I understand the goal as improving response time by caching expensive results.
        Before exploring the codebase deeply, the biggest scope decision is:
        should this cache apply to API responses, internal computed values, or both?
```

The approved Design Seed becomes the input for Phase 2.

### Phase 2: Codebase Exploration

**Goal**: Understand relevant existing code and patterns.

**What happens:**

- Launches 2-3 `code-explorer` agents in parallel
- Each agent explores a different aspect from the approved Design Seed
- Agents return comprehensive analyses with key files to read
- Claude reads all identified files to build deep understanding
- Presents a summary of findings and patterns

**Agents launched:**

- "Find features similar to [feature] and trace implementation"
- "Map the architecture and abstractions for [area]"
- "Analyze current implementation of [related feature]"

### Phase 3: Clarifying Questions

**Goal**: Fill in gaps and resolve ambiguities that only become visible after codebase exploration.

**What happens:**

- Reviews the approved Design Seed, codebase findings, and original request
- Identifies remaining underspecified aspects:
  - Edge cases
  - Error handling
  - Integration points
  - Backward compatibility
  - Performance needs
- Presents remaining questions in an organized list
- Waits for your answers before architecture design

### Phase 4: Architecture Design

**Goal**: Design multiple implementation approaches.

**What happens:**

- Launches 2-3 `code-architect` agents with different focuses:
  - **Minimal changes**: Smallest change, maximum reuse
  - **Clean architecture**: Maintainability, elegant abstractions
  - **Pragmatic balance**: Speed + quality
- Reviews all approaches
- Presents trade-offs and a recommendation
- Asks which approach you prefer

### Phase 5: Implementation

**Goal**: Build the feature.

**What happens:**

- Waits for explicit approval before starting
- Reads all relevant files identified in previous phases
- Implements the chosen architecture
- Follows codebase conventions strictly
- Updates todos as progress is made

### Phase 6: Quality Review

**Goal**: Ensure code is simple, DRY, elegant, and functionally correct.

**What happens:**

- Launches 3 `code-reviewer` agents in parallel with different focuses:
  - **Simplicity/DRY/Elegance**: Code quality and maintainability
  - **Bugs/Correctness**: Functional correctness and logic errors
  - **Conventions/Abstractions**: Project standards and patterns
- Consolidates findings
- Presents the highest-priority issues
- Asks whether to fix now, fix later, or proceed as-is

### Phase 7: Summary

**Goal**: Document what was accomplished.

**What happens:**

- Marks todos complete
- Summarizes:
  - What was built
  - Key decisions made
  - Files modified
  - Suggested next steps

## Agents

### `code-explorer`

**Purpose**: Deeply analyzes existing codebase features by tracing execution paths.

**Focus areas:**

- Entry points and call chains
- Data flow and transformations
- Architecture layers and patterns
- Dependencies and integrations
- Implementation details

### `code-architect`

**Purpose**: Designs feature architectures and implementation blueprints.

**Focus areas:**

- Codebase pattern analysis
- Architecture decisions
- Component design
- Implementation roadmap
- Data flow and build sequence

### `code-reviewer`

**Purpose**: Reviews code for bugs, quality issues, and project conventions.

**Focus areas:**

- Project guideline compliance
- Bug detection
- Code quality issues
- Confidence-based filtering

## Usage Patterns

### Full workflow

```bash
/feature-dev Add rate limiting to API endpoints
```

Use this for new features that need discovery, design, and review.

### Manual agent invocation

**Explore a feature:**

```text
Launch code-explorer to trace how authentication works
```

**Design architecture:**

```text
Launch code-architect to design the caching layer
```

**Review code:**

```text
Launch code-reviewer to check my recent changes
```

## Best Practices

1. **Use the full workflow for complex features**: the phases prevent premature implementation.
2. **Treat the Design Seed seriously**: it guides the entire exploration and design flow.
3. **Answer clarifying questions thoughtfully**: Phase 1 and Phase 3 prevent future confusion.
4. **Choose architecture deliberately**: Phase 4 gives you options for a reason.
5. **Don't skip code review**: Phase 6 catches issues before they reach production.

## When to Use This Plugin

**Use for:**

- New features that touch multiple files
- Features requiring architectural decisions
- Complex integrations with existing code
- Features where requirements are unclear or evolving

**Don't use for:**

- Single-line bug fixes
- Trivial changes
- Urgent hotfixes
- Tasks where the implementation is already fully specified

## Requirements

- Claude Code installed
- Git repository for code review workflows
- Project with existing codebase patterns to learn from

## Author

Sid Bidasaria (sbidasaria@anthropic.com), with local discovery workflow adaptation inspired by the MIT-licensed `brainstorming` skill from `obra/superpowers`.

## Version

1.1.0
