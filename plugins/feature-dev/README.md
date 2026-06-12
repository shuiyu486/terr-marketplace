# Feature Development Plugin

A comprehensive, structured workflow for feature development with adaptive discovery, codebase exploration, architecture design, implementation, and quality review.

## Overview

The Feature Development Plugin provides a systematic 7-phase approach to building new features. Instead of jumping straight into code, it first turns the initial idea into an approved Design Seed, classifies the work as Small/Medium/Large, then scales exploration, architecture design, implementation, and review to the actual risk and complexity of the request.

## Philosophy

Building features requires more than writing code. You need to:

- **Understand user intent** before choosing implementation details
- **Bound the scope** so the work stays focused
- **Match process depth to risk** instead of overusing heavyweight workflows
- **Understand the codebase** before making changes
- **Ask questions** only when answers materially affect the outcome
- **Design thoughtfully** before implementing
- **Review and verify** after building

This plugin embeds these practices into a structured workflow that runs when you use the `/feature-dev` command.

## Command: `/feature-dev`

Launches a guided feature development workflow with 7 adaptive phases.

**Usage:**

```bash
/feature-dev Add user authentication with OAuth
```

Or simply:

```bash
/feature-dev
```

The command will guide you through the process interactively.

## Adaptive Workflow Depth

The plugin classifies each request before launching agents:

| Depth | Use when | Typical agent usage |
|---|---|---|
| Small | Localized, clear, low-risk, likely 1-3 files, no schema/security/API boundary | Lightweight direct exploration or 1 `feature-dev:code-explorer`; usually no architect agent |
| Medium | One feature area, several files, some ambiguity or design choices | 1-2 `feature-dev:code-explorer`; optionally 1 `feature-dev:code-architect` |
| Large | Cross-cutting, ambiguous, high-risk, or involves public APIs, data/schema migrations, auth, permissions, billing, security, background jobs, or new abstractions | 2-3 `feature-dev:code-explorer`, 2-3 `feature-dev:code-architect`, reviewer panel |

The classification can be upgraded or downgraded after codebase exploration if the real complexity differs from the initial request.

Approval expectations:

- **Small** changes usually need one combined approval for the Design Seed and implementation plan.
- **Medium** changes usually use two gates: approve the Design Seed before exploration, then approve the implementation approach before code changes.
- **Large** changes use the same two gates as Medium, with deeper exploration, architecture comparison, and review before completion.

## The 7-Phase Workflow

### Phase 1: Discovery & Design Seed

**Goal**: Transform the initial idea into a clear, bounded Design Seed and choose the appropriate workflow depth.

**What happens:**

- Creates a progress list for the relevant phases
- Reads lightweight project context before asking detailed questions
- Restates the idea as a problem, target workflow, expected outcome, constraints, and non-goals
- Classifies the request as Small, Medium, or Large
- Detects if the request should be decomposed into smaller slices
- Asks focused clarifying questions only when they affect scope, behavior, risk, or implementation direction
- Proposes 1-3 high-level directions depending on workflow depth
- Presents a **Design Seed** and waits for approval before moving to codebase exploration

**Example:**

```text
You: /feature-dev Add caching
Claude: I understand the goal as improving response time by caching expensive results.
        I’d classify this as Medium because it likely touches one service path and has invalidation questions.
        Before exploring deeply, the biggest scope decision is:
        should this cache apply to API responses, internal computed values, or both?
```

The approved Design Seed becomes the input for Phase 2.

### Phase 2: Codebase Exploration

**Goal**: Understand relevant existing code and patterns at the right depth.

**What happens:**

- Small requests use direct reading or 1 explorer if the entry point is unclear
- Medium requests launch 1-2 `feature-dev:code-explorer` agents
- Large requests launch 2-3 `feature-dev:code-explorer` agents in parallel
- Each agent explores a different aspect from the approved Design Seed
- Agents return key files to read
- Claude reads the relevant files and presents findings
- The request may be reclassified if exploration shows it is simpler or riskier than expected

### Phase 3: Clarifying Questions

**Goal**: Resolve remaining ambiguities that affect architecture, behavior, safety, or compatibility.

**What happens:**

- Reviews the approved Design Seed, codebase findings, and original request
- Identifies underspecified aspects:
  - Edge cases
  - Error handling
  - Integration points
  - Backward compatibility
  - Performance needs
- Skips this phase for Small changes when no material ambiguity remains
- States safe defaults instead of asking unnecessary questions
- Waits for user answers when decisions require user judgment

### Phase 4: Architecture Design

**Goal**: Design an implementation approach with the right amount of comparison and detail.

**What happens:**

- Small requests usually get one direct implementation plan without architect agents
- Medium requests use inline design or 1 `feature-dev:code-architect` when the design is not obvious
- Large requests launch 2-3 `feature-dev:code-architect` agents with explicit perspectives:
  - **Minimal changes**: Smallest change, maximum reuse
  - **Clean architecture**: Maintainability, elegant abstractions
  - **Pragmatic balance**: Speed + quality
- Claude reviews all approaches and recommends one
- The user approves the implementation approach before code changes start

### Phase 5: Implementation

**Goal**: Build the feature.

**What happens:**

- Waits for explicit approval before starting
- Reads all relevant files identified in previous phases
- Implements the chosen approach
- Follows codebase conventions strictly
- Avoids speculative abstractions and unrelated improvements
- Cleans up orphaned imports, variables, functions, files, or TODOs caused by the change
- Updates progress tracking as work proceeds

### Phase 6: Quality Review

**Goal**: Ensure code is correct, simple, maintainable, and consistent with project conventions.

**What happens:**

- Runs appropriate verification: tests, lint, type-check, build, or targeted commands
- For frontend/UI changes, starts the dev server and verifies in browser when available
- Small changes use inline self-review unless they touch risk-sensitive logic
- Medium changes may launch 1-2 `feature-dev:code-reviewer` agents
- Large changes launch 3 `feature-dev:code-reviewer` agents in parallel with different focuses:
  - **Simplicity/DRY/Elegance**
  - **Bugs/Correctness**
  - **Conventions/Abstractions**
- Fixes clear implementation bugs and reruns relevant verification
- Asks the user about trade-off or scope decisions

### Phase 7: Summary

**Goal**: Document what was accomplished.

**What happens:**

- Marks progress items complete
- Summarizes:
  - What was built
  - Scope classification and any reclassification
  - Key decisions made
  - Files modified
  - Verification run and results
  - Suggested next steps

## Agents

### `feature-dev:code-explorer`

**Purpose**: Deeply analyzes existing codebase features by tracing execution paths.

**Focus areas:**

- Entry points and call chains
- Data flow and transformations
- Architecture layers and patterns
- Dependencies and integrations
- Implementation details

### `feature-dev:code-architect`

**Purpose**: Designs feature architectures and implementation blueprints from a requested perspective, such as minimal change, clean architecture, pragmatic balance, or best overall.

**Focus areas:**

- Codebase pattern analysis
- Architecture decisions
- Component design
- Implementation roadmap
- Data flow and build sequence

### `feature-dev:code-reviewer`

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
Launch feature-dev:code-explorer to trace how authentication works
```

**Design architecture:**

```text
Launch feature-dev:code-architect to design the caching layer
```

**Review code:**

```text
Launch feature-dev:code-reviewer to check my recent changes
```

By default, `feature-dev:code-reviewer` reviews the current `git diff`. If you want it to review specific files, commits, staged changes, or a broader scope, say that explicitly in the prompt.

## Best Practices

1. **Use the full workflow for complex features**: the phases prevent premature implementation.
2. **Let the workflow stay lightweight for small changes**: not every task needs a panel of agents.
3. **Treat the Design Seed seriously**: it guides exploration and design.
4. **Answer clarifying questions thoughtfully**: Phase 1 and Phase 3 prevent future confusion.
5. **Choose architecture deliberately**: Phase 4 gives options only when they are useful.
6. **Don't skip verification**: Phase 6 should run the relevant tests, lint, type-check, build, or UI checks.

## When to Use This Plugin

**Use for:**

- New features that touch multiple files
- Features requiring architectural decisions
- Complex integrations with existing code
- Features where requirements are unclear or evolving
- Medium or large changes where adaptive exploration and review reduce risk

**Don't use for:**

- Single-line bug fixes
- Trivial changes
- Urgent hotfixes where the implementation is already fully specified
- Tasks where a direct edit plus targeted verification is clearly enough

## Requirements

- Claude Code installed
- Git repository for code review workflows
- Project with existing codebase patterns to learn from

## Author

Sid Bidasaria (sbidasaria@anthropic.com), with local discovery workflow adaptation inspired by the MIT-licensed `brainstorming` skill from `obra/superpowers`.

## Version

1.2.0
