# cc-statusline

A feature-rich status line for Claude Code.

## Features

- Model name with ANSI colors
- Effort level (max/xhigh/high/medium/low) with color coding
- Context window usage percentage with color thresholds
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

One-click update to the latest version — finds, builds, and relinks.

## Configuration

```
/cc-statusline:configure
```

Toggle display options:
- Effort level
- Token statistics line
- Current path
- Context percentage thresholds

## Requirements

- Node.js 18+
- Claude Code CLI

## How It Works

The status line reads JSON data from stdin (provided by Claude Code), parses the session transcript for token/cost tracking, and renders a 3-line ANSI-colored display.

The setup command automatically configures your `~/.claude/settings.json` with the correct `statusLine` command.
