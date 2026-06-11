---
description: Set up cc-statusline in Claude Code settings (find path, write statusLine config, optionally authorize current Codex probe host)
allowed-tools: ["Bash", "PowerShell", "Read", "Edit", "Write", "AskUserQuestion"]
---

# cc-statusline Setup

Configure Claude Code's status line to use cc-statusline. After finding the plugin path, verify the build exists and build if needed, migrate cc-statusline config, optionally authorize the current remote Codex probe host, then write the status line command.

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

Check if `dist/index.js` and `dist/configCli.js` exist in the plugin path. If not, build the plugin:

**Windows (PowerShell):**

```powershell
$distFile = Join-Path $pluginPath 'dist\index.js'
$configCli = Join-Path $pluginPath 'dist\configCli.js'
if ((-not (Test-Path $distFile)) -or (-not (Test-Path $configCli))) {
    Write-Output "Build not found. Running npm install && npm run build..."
    Push-Location $pluginPath
    npm install 2>&1
    if ($LASTEXITCODE -ne 0) {
        Pop-Location
        Write-Output "ERROR: npm install failed. Check Node.js and network."
        exit 1
    }
    npm run build 2>&1
    $buildCode = $LASTEXITCODE
    Pop-Location
    if ($buildCode -ne 0) {
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
CONFIG_CLI="$PLUGIN_PATH/dist/configCli.js"
if [ ! -f "$PLUGIN_PATH/dist/index.js" ] || [ ! -f "$CONFIG_CLI" ]; then
    echo "Build not found. Running npm install && npm run build..."
    cd "$PLUGIN_PATH"
    npm install && npm run build || { echo "ERROR: build failed. Check Node.js and network."; exit 1; }
    echo "BUILD_OK"
else
    echo "Build already exists."
fi
```

## Step 3: Migrate cc-statusline Config

Use the shared config CLI to create, repair, or backfill `${CLAUDE_CONFIG_DIR:-~/.claude}/cc-statusline.json`.

**Windows (PowerShell):**

```powershell
$configCli = Join-Path $pluginPath 'dist\configCli.js'
node $configCli migrate
if ($LASTEXITCODE -ne 0) {
    Write-Output "ERROR: config migration failed"
    exit 1
}
```

**macOS / Linux:**

```bash
node "$CONFIG_CLI" migrate || { echo "ERROR: config migration failed"; exit 1; }
```

## Step 4: Optionally Authorize Current Codex Probe Host

cc-statusline only sends Codex header fallback probes to built-in local hosts (`localhost`, `127.0.0.1`, `::1`) or hosts explicitly listed in `codexProbeAllowedHosts`.

Use the shared config CLI to inspect the current effective `ANTHROPIC_BASE_URL`. It follows runtime precedence: `settings.json.env` first, then current process environment overrides it.

**Windows (PowerShell):**

```powershell
$probeSuggestionJson = node $configCli suggest-probe-host
if ($LASTEXITCODE -ne 0) {
    Write-Output "WARN: could not inspect ANTHROPIC_BASE_URL for Codex probe authorization"
    $probeSuggestion = $null
} else {
    $probeSuggestion = $probeSuggestionJson | ConvertFrom-Json
    Write-Output $probeSuggestionJson
}
```

**macOS / Linux:**

```bash
PROBE_SUGGESTION_JSON=$(node "$CONFIG_CLI" suggest-probe-host) || PROBE_SUGGESTION_JSON=''
[ -n "$PROBE_SUGGESTION_JSON" ] && echo "$PROBE_SUGGESTION_JSON"
```

If the result has `shouldAsk: true`, use AskUserQuestion:

Question: `Allow cc-statusline to probe Codex usage headers from <HOST>?`

Options:
1. label: `Allow`, description: `Add <HOST> to codexProbeAllowedHosts. cc-statusline may send a minimal /v1/messages probe to this host when Claude Code stdin lacks rate_limits.`
2. label: `Skip`, description: `Do not authorize this remote host. Setup continues, but Codex usage fallback will remain hidden for this host unless Claude Code provides rate_limits.`

If the user chooses `Allow`, run:

**Windows (PowerShell):**

```powershell
node $configCli allow-probe-host $probeSuggestion.host
if ($LASTEXITCODE -ne 0) {
    Write-Output "ERROR: failed to authorize Codex probe host"
    exit 1
}
```

**macOS / Linux:**

```bash
HOST=$(node -e "const s=JSON.parse(process.argv[1]); process.stdout.write(s.host || '')" "$PROBE_SUGGESTION_JSON")
node "$CONFIG_CLI" allow-probe-host "$HOST" || { echo "ERROR: failed to authorize Codex probe host"; exit 1; }
```

If `shouldAsk` is false:
- `status: "builtin"` means the host is local and already allowed by default.
- `status: "already_allowed"` means it is already listed in `codexProbeAllowedHosts`.
- `status: "no_base_url"` or `status: "invalid_base_url"` means there is no remote host to authorize; continue setup.

## Step 5: Write Status Line Configuration

Merge the `statusLine` field into `~/.claude/settings.json`, preserving all existing settings.

The command string uses forward slashes (Claude Code handles this correctly on all platforms):

```text
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
$pluginPathForCommand = $pluginPath -replace '\\','/'
$command = 'node "' + $pluginPathForCommand + '/dist/index.js"'
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
[System.IO.File]::WriteAllText($settingsPath, $json + "`n", (New-Object System.Text.UTF8Encoding $false))
```

**macOS/Linux — use Node.js for JSON merge:**

```bash
COMMAND_STRING="node \"${PLUGIN_PATH%/}/dist/index.js\""
node -e "
const fs = require('fs');
const path = require('path');
const p = path.join(process.env.CLAUDE_CONFIG_DIR || require('os').homedir() + '/.claude', 'settings.json');
let s = {};
try { s = JSON.parse(fs.readFileSync(p, 'utf8')); } catch {}
s.statusLine = { type: 'command', command: process.argv[1] };
fs.writeFileSync(p, JSON.stringify(s, null, 2) + '\n');
" "$COMMAND_STRING"
```

**Verify** — read settings.json and confirm `statusLine.command` is set:

```bash
cat ~/.claude/settings.json | grep -A2 statusLine
```

Tell the user:

> Setup complete! Restart Claude Code (exit and re-enter) to see the status line. If you authorized a remote Codex probe host, usage fallback takes effect after restart. If it doesn't appear, run `/cc-statusline:setup` again to verify.
