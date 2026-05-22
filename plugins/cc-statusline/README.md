# cc-statusline

A feature-rich status line for Claude Code.

## Features

- Model name with ANSI colors
- Effort level (max/xhigh/high/medium/low) with color coding
- Context window usage percentage with color thresholds
- **Tool activity** — watch Claude read, edit, and search files as it happens
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

One-click update: pulls the latest from remote marketplace, builds, relinks, and restarts the running status line. No git push/commit needed.

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

## Requirements

- Node.js 18+
- Claude Code CLI

## How It Works

The status line reads JSON data from stdin (provided by Claude Code), parses the session transcript for token/cost tracking, tool activity, agent tracking, and todo progress, and renders a multi-line ANSI-colored display.

The setup command automatically configures your `~/.claude/settings.json` with the correct `statusLine` command.
