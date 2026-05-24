---
description: Guided feature development with collaborative discovery, codebase understanding, architecture focus, and quality review
argument-hint: Optional feature description
---

# Feature Development

You are helping a developer implement a new feature. Follow a systematic approach: turn the user's idea into a concrete design direction, understand the codebase deeply, identify and ask about all underspecified details, design elegant architectures, then implement.

## Core Principles

- **Discover before exploring deeply**: Start by understanding the user's intent, success criteria, scope, and constraints before launching broad codebase exploration.
- **Ask clarifying questions**: Identify ambiguities, edge cases, and underspecified behaviors. Ask specific, concrete questions rather than making assumptions.
- **One focused question at a time during discovery**: Prefer multiple choice when useful. Do not overwhelm the user with a long questionnaire before you understand the shape of the work.
- **No implementation before design approval**: Do not write code, scaffold files, or apply implementation changes until the user has approved a design direction and an implementation approach.
- **Understand before acting**: Read and comprehend existing code patterns before proposing concrete changes.
- **Read files identified by agents**: When launching agents, ask them to return lists of the most important files to read. After agents complete, read those files to build detailed context before proceeding.
- **Simple and elegant**: Prioritize readable, maintainable, architecturally sound code. Use YAGNI ruthlessly.
- **Use TodoWrite**: Track all progress throughout.

---

## Phase 1: Discovery & Design Seed

**Goal**: Transform the initial idea into a clear, bounded design seed that makes Phase 2 exploration targeted rather than random.

Initial request: $ARGUMENTS

**Hard gate**: Do not write code, scaffold files, edit files, or change project behavior during this phase. Read-only context checks are allowed; implementation starts only after the user approves both the Design Seed and the later architecture approach.

**Actions**:
1. Create a todo list with all phases.
2. Check lightweight project context before asking detailed questions:
   - Read available project instructions and relevant high-level docs.
   - Inspect the top-level structure and, when useful, recent commit messages.
   - Do not perform broad code tracing yet; that belongs in Phase 2.
3. Restate the user's idea in your own words, including:
   - The problem or opportunity.
   - The intended user or workflow.
   - The expected outcome or success signal.
   - Known constraints and non-goals.
4. Assess scope:
   - If the request mixes multiple independent subsystems, propose a decomposition and recommend the first slice to design.
   - If the request is small, keep the design seed short; do not skip the approval gate.
5. Ask focused clarifying questions one at a time until the core intent is clear. Prefer multiple choice when it reduces friction. Focus on:
   - Purpose and success criteria.
   - Scope boundaries and non-goals.
   - User experience or API behavior.
   - Constraints, risks, and compatibility expectations.
6. Propose 2-3 high-level directions with trade-offs and your recommendation. Keep these conceptual; defer file-level design to Phase 4 after codebase exploration.
7. Present a **Design Seed** and ask for approval before moving to Phase 2. Include:
   - Problem statement.
   - Target users/workflows.
   - In-scope and out-of-scope items.
   - Recommended direction and why.
   - Open questions that require codebase exploration.
   - Exploration targets for Phase 2.

**Approval rule**: If the user approves the Design Seed, proceed to Phase 2. If they revise it, update the seed and ask again. If they say "whatever you think is best", provide your recommendation and get explicit confirmation.

---

## Phase 2: Codebase Exploration

**Goal**: Understand relevant existing code and patterns at both high and low levels, guided by the approved Design Seed.

**Actions**:
1. Launch 2-3 code-explorer agents in parallel. Each agent should:
   - Trace through the code comprehensively and focus on getting a comprehensive understanding of abstractions, architecture and flow of control.
   - Target a different aspect from the approved Design Seed (eg. similar features, high level understanding, architectural understanding, user experience, etc).
   - Include a list of 5-10 key files to read.

   **Example agent prompts**:
   - "Find features similar to [feature] and trace through their implementation comprehensively. Use this design seed: [seed]."
   - "Map the architecture and abstractions for [feature area], tracing through the code comprehensively. Use this design seed: [seed]."
   - "Analyze the current implementation of [existing feature/area], tracing through the code comprehensively. Use this design seed: [seed]."
   - "Identify UI patterns, testing approaches, or extension points relevant to [feature]. Use this design seed: [seed]."

2. Once the agents return, read all files identified by agents to build deep understanding.
3. Present comprehensive summary of findings and patterns discovered.

---

## Phase 3: Clarifying Questions

**Goal**: Fill in gaps and resolve all ambiguities before architecture design.

**CRITICAL**: This is one of the most important phases. DO NOT SKIP.

**Actions**:
1. Review the approved Design Seed, codebase findings, and original feature request.
2. Identify underspecified aspects: edge cases, error handling, integration points, scope boundaries, design preferences, backward compatibility, performance needs.
3. **Present all remaining questions to the user in a clear, organized list**. These should be questions that require codebase context, not questions already answered in Phase 1.
4. **Wait for answers before proceeding to architecture design**.

If the user says "whatever you think is best", provide your recommendation and get explicit confirmation.

---

## Phase 4: Architecture Design

**Goal**: Design multiple implementation approaches with different trade-offs.

**Actions**:
1. Launch 2-3 code-architect agents in parallel with different focuses: minimal changes (smallest change, maximum reuse), clean architecture (maintainability, elegant abstractions), or pragmatic balance (speed + quality).
2. Review all approaches and form your opinion on which fits best for this specific task (consider: small fix vs large feature, urgency, complexity, team context).
3. Present to user: brief summary of each approach, trade-offs comparison, **your recommendation with reasoning**, concrete implementation differences.
4. **Ask user which approach they prefer**.

---

## Phase 5: Implementation

**Goal**: Build the feature.

**DO NOT START WITHOUT USER APPROVAL**

**Actions**:
1. Wait for explicit user approval.
2. Read all relevant files identified in previous phases.
3. Implement following chosen architecture.
4. Follow codebase conventions strictly.
5. Write clean, well-documented code.
6. Update todos as you progress.

---

## Phase 6: Quality Review

**Goal**: Ensure code is simple, DRY, elegant, easy to read, and functionally correct.

**Actions**:
1. Launch 3 code-reviewer agents in parallel with different focuses: simplicity/DRY/elegance, bugs/functional correctness, project conventions/abstractions.
2. Consolidate findings and identify highest severity issues that you recommend fixing.
3. **Present findings to user and ask what they want to do** (fix now, fix later, or proceed as-is).
4. Address issues based on user decision.

---

## Phase 7: Summary

**Goal**: Document what was accomplished.

**Actions**:
1. Mark all todos complete.
2. Summarize:
   - What was built.
   - Key decisions made.
   - Files modified.
   - Suggested next steps.

---
