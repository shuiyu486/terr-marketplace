---
description: Set up cc-statusline in Claude Code settings (find path, write statusLine config)
allowed-tools: ["Bash", "Read", "Edit", "Write", "AskUserQuestion"]
---

# cc-statusline Setup

Configure Claude Code's status line to use cc-statusline. After finding the plugin path, verify the build exists and build if needed, then write the config.

## Step 1: Find Plugin Path

Find the plugin cache directory — the plugin is installed under `~/.claude/plugins/cache/`:

**macOS / Linux:**

```bash
PLUGIN_PATH=$(ls -d "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins/cache/*/cc-statusline/*/ 2>/dev/null | sort -V | tail -1)
echo "$PLUGIN_PATH"
```

**Windows (PowerShell):**

```powershell
$claudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$pluginPath = (Get-ChildItem (Join-Path $claudeDir 'plugins\cache\*\cc-statusline\*') -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '^\d+(\.\d+)+$' } | Sort-Object { [version]$_.Name } -Descending | Select-Object -First 1).FullName
Write-Output $pluginPath
```

If no path is found, tell the user to install the plugin first: `/plugin install cc-statusline`.

If a path is found, set the variable for later steps:

- **Windows:** `$pluginPath` (already set by the PowerShell command above)
- **macOS/Linux:** `$PLUGIN_PATH` (already set by the bash command above)

## Step 2: Ensure Build Exists

Check if `dist/index.js` exists in the plugin path. If not, build the plugin:

**Windows (PowerShell):**

```powershell
$distFile = Join-Path $pluginPath 'dist\index.js'
if (-not (Test-Path $distFile)) {
    Write-Output "Build not found. Running npm install && npm run build..."
    cd $pluginPath
    npm install 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Output "ERROR: npm install failed. Check Node.js and network."
        exit 1
    }
    npm run build 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Output "ERROR: npm run build failed."
        exit 1
    }
    Write-Output "BUILD_OK"
} else {
    Write-Output "Build already exists."
}
```

**macOS / Linux:**

```bash
if [ ! -f "$PLUGIN_PATH/dist/index.js" ]; then
    echo "Build not found. Running npm install && npm run build..."
    cd "$PLUGIN_PATH"
    npm install && npm run build || { echo "ERROR: build failed. Check Node.js and network."; exit 1; }
    echo "BUILD_OK"
else
    echo "Build already exists."
fi
```

## Step 3: Write Configuration

Merge the `statusLine` field into `~/.claude/settings.json`, preserving all existing settings.

The command string uses forward slashes (Claude Code handles this correctly on all platforms):

```
node "<PLUGIN_PATH>/dist/index.js"
```

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

> Setup complete! Restart Claude Code (exit and re-enter) to see the status line. If the build was missing, it has been built automatically. If it doesn't appear, run `/cc-statusline:setup` again to verify.