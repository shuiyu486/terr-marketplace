---
description: Create a handoff document for another Claude Code session
argument-hint: "What will the next session be used for?"
allowed-tools: ["Write", "PowerShell", "Bash"]
---

# Handoff

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save it to the temporary directory of the user's OS, not the current workspace.

Use `$ARGUMENTS`, if provided, as the description of what the next session will focus on and tailor the document accordingly.

The handoff document must include:

- Current objective and user intent.
- Important context, decisions, constraints, and assumptions.
- Current state of the work, including completed steps and remaining work.
- Relevant artifact paths or URLs instead of duplicating content already captured in PRDs, plans, ADRs, issues, commits, or diffs.
- A "suggested skills" section recommending any skills the next agent should invoke.
- Verification status, known failures, blockers, and next recommended command or action.

Before saving, redact sensitive information such as API keys, passwords, tokens, secrets, and personally identifiable information.

After saving, report the handoff file path and a concise summary of what it contains.
