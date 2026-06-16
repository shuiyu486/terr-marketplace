# cc-statusline

A feature-rich status line for Claude Code.

## Screenshot

![cc-statusline usage limits](docs/assets/cc-statusline.png)

## Features

- Model name with ANSI colors
- Effort level (max/xhigh/high/medium/low) with color coding
- Context window usage percentage with color thresholds; when Claude Code does not provide trustworthy context usage, token fields show `—` instead of a misleading `0`
- **Tool activity** — watch Claude read, edit, search, and call MCP tools; completed tool counts are accumulated for the session and wrap to two lines with `… +N` overflow when needed
- **Agent tracking** — see which subagents are running and what they're doing
- **Todo progress** — track task completion in real-time
- **Usage limits** — display 5-hour and 7-day usage bars with reset countdowns (Claude `rate_limits` or Codex header fallback)
- Token statistics: input, output, session API, total API
- Session cost tracking via transcript parsing
- Current working directory

## Installation

```bash
/plugin install cc-statusline
```

Then run the setup command:

```
/cc-statusline:setup
```

## Update

```
/cc-statusline:update
```

One-click update: pulls the latest into Claude Code's installed marketplace clone, builds the runtime cache, relinks, and restarts the running status line. It does not touch the maintainer working tree.

## Restart

```
/cc-statusline:restart
```

Restart the running status line without changing configuration or rebuilding.

## Configuration

```
/cc-statusline:configure
```

Toggle display options:
- Effort level
- Token statistics line
- Current path
- Tool activity
- Agent tracking
- Todo progress
- Usage limits
- Context percentage thresholds

Codex usage fallback probes are limited to built-in local hosts by default. Remote proxy hosts must be explicitly authorized in `codexProbeAllowedHosts`; `/cc-statusline:setup` can add the current `ANTHROPIC_BASE_URL` host identity, including an explicit port, after confirmation.

## Requirements

- Node.js 18+
- Claude Code CLI

## How It Works

The status line reads JSON data from stdin (provided by Claude Code), parses the session transcript for token/cost tracking, tool activity, agent tracking, and todo progress, and renders a multi-line ANSI-colored display. Context `in/out` uses Claude Code's `context_window` totals first, falls back to `current_usage` and the latest transcript usage when available, and displays `—` when no reliable token snapshot exists.

The setup command automatically configures your `~/.claude/settings.json` with the correct `statusLine` command. If your `ANTHROPIC_BASE_URL` points to a remote proxy, setup can also ask whether to add that host identity to `codexProbeAllowedHosts` so the Codex usage fallback can read `X-Codex-*` headers.
