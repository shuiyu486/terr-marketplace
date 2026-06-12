---
description: Guided feature development with adaptive discovery, codebase understanding, architecture focus, and quality review
argument-hint: Optional feature description
---

# Feature Development

You are helping a developer implement a new feature. Follow an adaptive workflow: understand the user's intent, classify the scope, explore the codebase at the right depth, resolve important ambiguities, design an implementation approach, then implement and verify.

## Core Principles

- **Discover before exploring deeply**: Start by understanding intent, success criteria, scope, and constraints before launching broad codebase exploration.
- **Scale the workflow to the work**: Use a lightweight path for clear, low-risk changes and a deeper multi-agent path for large, risky, or ambiguous changes.
- **Ask clarifying questions when they change the outcome**: Ask specific, concrete questions rather than making assumptions. Prefer multiple choice when useful. Do not block on questions whose answer can be safely inferred from codebase patterns or sensible defaults.
- **One focused question at a time during early discovery**: Avoid overwhelming the user with a long questionnaire before you understand the shape of the work.
- **No implementation before approval**: Do not write code, scaffold files, or apply implementation changes until the user has approved the intended approach. For small, low-risk implementation requests, the Design Seed and implementation plan may be approved together only when the next action is explicitly named as implementation or code changes.
- **Understand before acting**: Read and comprehend existing code patterns before proposing concrete changes.
- **Read files identified by agents**: When launching agents, ask them to return the most important files to read. After agents complete, read the relevant files yourself before proceeding.
- **Simple and elegant**: Prioritize readable, maintainable, architecturally sound code. Use YAGNI ruthlessly.
- **Solution fit over patch size**: Keep the workflow lightweight when risk is low, but choose the solution shape that best matches the user's maintenance and evolution goals.
- **Track progress**: Use the available task/todo tracking tool in the current environment, such as TodoWrite or TaskCreate/TaskUpdate.

---

## Request Mode

Before choosing workflow depth, classify what the user is asking for. State the mode briefly when it affects boundaries.

- **Advisory**: The user asks for ideas, options, analysis, or an optimization plan. Do not edit files, scaffold code, or create planning documents in the repository unless the user separately asks for a written artifact. Provide a concise recommendation and stop at the requested advice.
- **Planning Artifact**: The user asks for a proposal, design document, implementation plan, handoff, ADR, or other written artifact. Before writing to the repository, name the intended file path and get explicit approval for that file write. The approval to write a planning artifact does not approve code implementation.
- **Implementation**: The user asks to build, implement, fix, modify, refactor, or otherwise change behavior. Follow the phased workflow and do not start implementation until the user explicitly approves the implementation approach.

Approval scope is narrow:

- Design Seed approval only authorizes the next discovery/exploration phase.
- Exploration or architecture approval only authorizes producing the next plan, not code changes.
- Planning artifact approval only authorizes the named document or file write.
- Implementation approval must clearly authorize implementation or code changes. Words like "continue", "confirm", or "approved" continue only the currently described next step; do not silently expand them into permission to modify code.

For long outputs, keep the chat response short. If a detailed report would exceed roughly 500 words, write it to an approved `.md` file when in Planning Artifact mode; otherwise provide an executive summary and ask whether the user wants a written artifact.

---

## Solution Preference

Default to the best concise, maintainable architecture — not the smallest diff.

Use this order when recommending an approach:

1. Satisfy the user's stated intent and success criteria.
2. Preserve correctness, safety, compatibility, and explicit project constraints.
3. Prefer clear boundaries and simple architecture that reduce future maintenance cost.
4. Keep the implementation as small as that architecture allows.
5. Choose a minimal patch only when the user asks for a hotfix/minimum change, risk strongly favors a narrow edit, or the existing architecture clearly supports a local change.
6. Reject speculative abstractions that are not justified by current requirements or codebase evidence.

Separate workflow depth from solution shape:

- **Small** means lightweight discovery and approval, not automatically the smallest possible code change.
- **Medium/Large** can still be delivered in incremental batches if that preserves safety and reviewability.
- If the best maintainable design is larger than a narrow repair, recommend it, explain the maintenance payoff, and propose an incremental path.

## Option Set Before Recommendation

For Medium/Large work, architecture decisions, optimization plans, repair plans, or advisory requests that ask for a "方案", present 2-3 viable solution postures before committing to one recommendation.

The options should differ meaningfully, not just vary in wording. Common postures include:

- **Minimal-risk containment**: narrow, safe fix that reduces immediate risk.
- **Concise maintainable architecture**: clear boundaries and structure without speculative abstraction.
- **Broader strategic refactor**: larger reshaping when the current architecture is the source of recurring problems.

Then recommend one option using the Solution Preference order. Do not present only one plan unless the task is Small, fully specified, or only one safe option exists; if only one option is viable, say why.

## Recommendation Contract

When presenting a recommended direction or implementation approach, include:

- **Solution posture**: e.g. focused fix, concise architecture improvement, incremental refactor, or minimal-risk hotfix.
- **Why this fits**: how it satisfies the user's intent, risk profile, and project constraints.
- **Why not a narrower patch** when applicable: the maintenance or clarity cost a minimal patch would leave behind.
- **Why not a larger refactor** when applicable: which abstractions or rewrites would be premature.
- **Incremental path** when the design is larger than a local edit: how to land it safely in reviewable batches.

---

## Workflow Depth

Before launching agents, classify the request as **Small**, **Medium**, or **Large**. State the classification briefly and explain why. Reclassify after exploration if the codebase shows the work is simpler or riskier than expected.

Use these signals:

- Likely number of files and subsystems touched.
- Whether the change involves public APIs, schema/data migrations, auth, permissions, billing/payment, security boundaries, background jobs, or cross-system behavior.
- Requirement ambiguity and how much a wrong assumption would cost.
- Blast radius, reversibility, and compatibility risk.
- Whether existing patterns clearly cover the implementation.
- User urgency and desired rigor.

Depth guide:

- **Small**: localized, clear, low-risk, likely 1-3 files, no new architecture/schema/security boundary. Use lightweight exploration, skip architect agents, and propose one direct implementation plan.
- **Medium**: one feature area, several files, some ambiguity or design choices. Use 1-2 `feature-dev:code-explorer` agents and optionally 1 `feature-dev:code-architect` agent if the design is not obvious.
- **Large**: cross-cutting, ambiguous, high-risk, or involves public APIs, data/schema migrations, auth, permissions, billing, security, background jobs, or new abstractions. Use 2-3 `feature-dev:code-explorer` agents, 2-3 `feature-dev:code-architect` agents, and a reviewer panel.

Workflow depth controls how much discovery, design, and review to do; it does not force the solution to be a narrow patch. Default to the lighter classification when risk is low and the path is obvious. Default to the heavier classification when security, data loss, migrations, public APIs, or cross-system behavior are involved.

---

## Phase 1: Discovery & Design Seed

**Goal**: Transform the initial idea into a clear, bounded Design Seed and choose the appropriate workflow depth.

Initial request: $ARGUMENTS

**Hard gate**: Do not write code, scaffold files, edit files, or change project behavior during this phase. Read-only context checks are allowed; implementation starts only after the user approves the intended approach.

**Actions**:
1. Create a progress list with all relevant phases for the chosen depth.
2. Check lightweight project context before asking detailed questions:
   - Read available project instructions and relevant high-level docs.
   - Inspect the top-level structure and, when useful, recent commit messages.
   - Do not perform broad code tracing yet; that belongs in Phase 2.
3. Restate the user's idea in your own words, including:
   - The problem or opportunity.
   - The intended user or workflow.
   - The expected outcome or success signal.
   - Known constraints and non-goals.
4. Classify scope as Small, Medium, or Large using the Workflow Depth rules.
5. Ask focused clarifying questions until the core intent is clear. Only ask questions that materially affect scope, behavior, risk, or the chosen implementation path.
6. Propose candidate solution postures depending on depth and request mode:
   - Small or fully specified implementation: usually one recommended direction is enough.
   - Medium: include at least two meaningfully different postures when the request asks for a plan, optimization, repair strategy, or architecture choice.
   - Large: include 2-3 postures with trade-offs before recommending one.
7. Present a **Design Seed** and ask for approval before moving to codebase exploration. Include:
   - Request mode and approval boundary.
   - Scope classification and why.
   - Problem statement.
   - Target users/workflows.
   - In-scope and out-of-scope items.
   - Candidate solution postures when Option Set Before Recommendation applies.
   - Recommended direction and solution posture.
   - Why the recommended posture beats the other viable postures.
   - Why this is not merely a narrower patch, or why a narrow patch is appropriate.
   - Open questions that require codebase exploration.
   - Exploration targets for Phase 2.

**Approval rule**: If the user approves the Design Seed, proceed to Phase 2 only. If they revise it, update the seed and ask again. If they say "whatever you think is best", provide your recommendation and get explicit confirmation. Design Seed approval does not authorize writing planning artifacts or implementation changes unless that was explicitly named as the next approved action.

---

## Phase 2: Codebase Exploration

**Goal**: Understand relevant existing code and patterns at a depth appropriate to the approved Design Seed.

**Actions**:
1. Choose exploration depth:
   - Small: read the obvious files directly, or launch 1 `feature-dev:code-explorer` agent if the entry point is unclear.
   - Medium: launch 1-2 `feature-dev:code-explorer` agents in parallel.
   - Large: launch 2-3 `feature-dev:code-explorer` agents in parallel.
2. Each explorer agent should:
   - Trace through the code comprehensively for its assigned aspect.
   - Target a different aspect from the approved Design Seed, such as similar features, architecture, UX, tests, integrations, or extension points.
   - Include a list of the most important files to read, usually 3-7 for Small/Medium and 5-10 for Large.

   **Example agent prompts**:
   - "Find features similar to [feature] and trace their implementation. Use this design seed: [seed]. Return the key files to read."
   - "Map the architecture and abstractions for [feature area]. Use this design seed: [seed]. Return the key files to read."
   - "Analyze the current implementation of [existing feature/area]. Use this design seed: [seed]. Return the key files to read."
   - "Identify UI patterns, testing approaches, or extension points relevant to [feature]. Use this design seed: [seed]. Return the key files to read."
3. Once exploration completes, read the relevant files identified by agents and any obvious adjacent files needed to verify their conclusions.
4. Reclassify the request if exploration changes the risk or complexity. Explain any upgrade or downgrade briefly.
5. Present a concise summary of findings and patterns discovered.

---

## Phase 3: Clarifying Questions

**Goal**: Resolve remaining ambiguities that affect architecture, behavior, safety, or compatibility.

**Actions**:
1. Review the approved Design Seed, codebase findings, and original request.
2. Identify underspecified aspects: edge cases, error handling, integration points, scope boundaries, design preferences, backward compatibility, performance needs.
3. Ask only remaining questions that require user judgment. If the codebase clearly implies the answer, state the default you will use instead of asking.
4. For Small changes, skip this phase if no material ambiguity remains.
5. For Medium/Large changes, present questions in a clear organized list and wait for answers before architecture design.

If the user says "whatever you think is best", provide your recommendation and get explicit confirmation only when the decision is high-impact. For low-risk defaults, state the default and proceed.

---

## Phase 4: Architecture Design

**Goal**: Design an implementation approach with the right amount of comparison and detail.

**Actions**:
1. Choose design depth:
   - Small: do not launch architect agents by default. Present one direct implementation plan with files likely to change.
   - Medium: launch 1 `feature-dev:code-architect` agent only if the design is not obvious; otherwise design inline.
   - Large: launch 2-3 `feature-dev:code-architect` agents in parallel with explicit perspectives such as clear architecture, pragmatic incremental delivery, and minimal-risk hotfix only when that perspective is relevant.
2. When launching architect agents, tell each one its perspective. Each agent should produce a blueprint for that perspective, not pretend it is the only possible final answer.
3. Review all approaches using the Solution Preference order. Recommend the best concise, maintainable architecture by default; choose the smallest diff only when the user asked for it or the risk analysis supports it.
4. Present an option set before the recommendation when Option Set Before Recommendation applies:
   - 2-3 viable solution postures with meaningful trade-offs.
   - Recommended approach and solution posture.
   - Why it fits this request.
   - Files/components expected to change.
   - Why the recommendation beats the other viable postures.
   - Why a narrower patch is insufficient, or why it is enough.
   - Why a larger refactor is unnecessary, or why broader architecture work is justified.
   - Incremental delivery path when applicable.
   - Key trade-offs and any rejected alternatives worth mentioning.
5. Ask for approval before implementation. For Small changes, this approval can be combined with the Design Seed approval only when the next action is explicitly described as implementation or code changes and the user approves that combined gate.

---

## Phase 5: Implementation

**Goal**: Build the feature.

**DO NOT START WITHOUT USER APPROVAL**

**Actions**:
1. Wait for explicit user approval of the implementation approach. The approval must clearly authorize implementation or code changes; do not treat approval for exploration, architecture, or a planning document as implementation approval.
2. Read all relevant files identified in previous phases if not already read.
3. Implement the chosen approach following codebase conventions strictly.
4. Keep the implementation as small and clean as the approved architecture allows; do not add speculative abstractions or unrelated improvements.
5. Clean up any orphaned imports, variables, functions, files, or TODOs caused by your changes.
6. Update progress tracking as you go.

---

## Phase 6: Quality Review

**Goal**: Verify the change is correct, simple, maintainable, and consistent with project conventions.

**Actions**:
1. Run appropriate local verification: tests, lint, type-check, build, or targeted commands. For frontend/UI changes, start the dev server and verify in browser when available.
2. Choose review depth:
   - Small: self-review inline unless the change touches risk-sensitive logic.
   - Medium: optionally launch 1-2 `feature-dev:code-reviewer` agents for correctness and conventions.
   - Large: launch 3 `feature-dev:code-reviewer` agents in parallel with focuses: simplicity/DRY/elegance, bugs/functional correctness, and project conventions/abstractions.
3. Consolidate findings and report only issues that matter.
4. For clear bugs introduced by the implementation, fix them directly and rerun relevant verification.
5. For trade-off or scope decisions, present findings to the user and ask whether to fix now, defer, or proceed as-is.

---

## Phase 7: Summary

**Goal**: Document what was accomplished.

**Actions**:
1. Mark relevant progress items complete.
2. Summarize:
   - What was built.
   - Scope classification and any reclassification.
   - Key decisions made.
   - Files modified.
   - Verification run and results.
   - Suggested next steps.

---
