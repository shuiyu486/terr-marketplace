---
description: Set up cc-statusline in Claude Code settings (detect platform, build, configure statusLine)
allowed-tools: ["Bash", "Read", "Edit", "Write", "AskUserQuestion"]
---

# cc-statusline Setup

Configure Claude Code's status line to use cc-statusline. This command detects your platform, builds the plugin, and writes the `statusLine` configuration to `~/.claude/settings.json`.

## Step 1: Detect Environment

Check that Node.js is available and find the plugin's installed path.

**On any platform**, run:

```bash
node --version
```

If node is not found, tell the user:

> Node.js 18+ is required. Install from https://nodejs.org or via your package manager, then re-run `/cc-statusline:setup`.

**Find the plugin cache directory** — the plugin is installed under `~/.claude/plugins/cache/`:

**macOS / Linux:**

```bash
ls -d "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins/cache/*/cc-statusline/*/ 2>/dev/null | sort -V | tail -1
```

**Windows (Git Bash):**

```bash
ls -1d "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins/cache/*/cc-statusline/*/ 2>/dev/null | sort -V | tail -1
```

**Windows (PowerShell):**

```powershell
$claudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
(Get-ChildItem (Join-Path $claudeDir 'plugins\cache\*\cc-statusline\*') -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '^\d+(\.\d+)+$' } | Sort-Object { [version]$_.Name } -Descending | Select-Object -First 1).FullName
```

If no path is found, tell the user to install the plugin first: `/plugin install cc-statusline`.

## Step 2: Build and Generate Command

**Build the plugin** (install dependencies and compile TypeScript):

```bash
cd "<PLUGIN_PATH>" && npm install && npm run build
```

Verify `dist/index.js` exists:

```bash
ls -la "<PLUGIN_PATH>/dist/index.js"
```

**Generate the statusLine command.** The command is simply:

```
node "<PLUGIN_PATH>/dist/index.js"
```

On Windows, use forward slashes in the path for the command string (Claude Code handles this correctly).

**Test the command** — pipe a minimal JSON to verify output:

```bash
echo '{"model":{"display_name":"test"},"context_window":{"used_percentage":50,"context_window_size":200000,"total_input_tokens":1000,"total_output_tokens":500},"effort":{"level":"medium"},"transcript_path":""}' | node "<PLUGIN_PATH>/dist/index.js"
```

If this produces output (colored text with model name, context, tokens), the command works. If it errors or hangs, do NOT proceed — tell the user to check Node.js and the plugin installation.

## Step 3: Write Configuration

Merge the `statusLine` field into `~/.claude/settings.json`, preserving all existing settings.

**Settings file location:**
- **macOS/Linux:** `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json`
- **Windows:** Inside `$env:CLAUDE_CONFIG_DIR` when set, otherwise `Join-Path $HOME '.claude'` → `settings.json`

**The config to merge:**

```json
{
  "statusLine": {
    "type": "command",
    "command": "node \"<PLUGIN_PATH>/dist/index.js\""
  }
}
```

**Merge logic:**

If `settings.json` doesn't exist, create it with just the `statusLine` field.

If it exists, read it, parse as JSON, add/update the `statusLine` field, and write back. **Preserve all existing fields** (model, permissions, env, enabledPlugins, etc.).

**Windows PowerShell — UTF-8 without BOM:**

```powershell
$settingsPath = Join-Path $claudeDir 'settings.json'
$existing = @{}
if (Test-Path $settingsPath) {
    try {
        $raw = [System.Text.Encoding]::UTF8.GetString([System.IO.File]::ReadAllBytes($settingsPath))
        $existing = $raw | ConvertFrom-Json
    } catch {
        Write-Output "settings.json parse error, creating backup"
        Copy-Item $settingsPath "$settingsPath.bak" -Force
    }
}
$existing | Add-Member -NotePropertyName statusLine -NotePropertyValue @{ type = 'command'; command = $command } -Force
$json = $existing | ConvertTo-Json -Depth 10
$json = $json -replace '\\/', '/'  # unescape forward slashes
[System.IO.File]::WriteAllText($settingsPath, $json, (New-Object System.Text.UTF8Encoding $false))
```

**macOS/Linux — use Node.js for JSON merge:**

```bash
node -e "
const fs = require('fs');
const path = require('path');
const p = path.join(process.env.CLAUDE_CONFIG_DIR || require('os').homedir() + '/.claude', 'settings.json');
let s = {};
try { s = JSON.parse(fs.readFileSync(p, 'utf8')); } catch {}
s.statusLine = { type: 'command', command: process.argv[1] };
fs.writeFileSync(p, JSON.stringify(s, null, 2));
" "<COMMAND_STRING>"
```

**Verify** — read settings.json and confirm `statusLine.command` is set:

```bash
cat ~/.claude/settings.json | grep -A2 statusLine
```

Tell the user:

> Setup complete! Restart Claude Code (exit and re-enter) to see the status line. If it doesn't appear, run `/cc-statusline:setup` again to verify.
