---
description: Update cc-statusline to the latest installed version (build + relink settings.json path)
allowed-tools: ["Bash", "Read", "Edit", "Write"]
---

# cc-statusline Update

One-click update: find the latest installed version, build it, and update settings.json to point to the new path. Preserves your existing cc-statusline.json config.

## Step 0: Pull Latest (if needed)

If you haven't pulled the latest plugin version yet, run this first:

```
/plugin install cc-statusline
```

Then re-run `/cc-statusline:update`.

## Step 1: Find Latest Version Directory

Scan for all installed versions of cc-statusline and pick the latest:

**Windows (PowerShell):**

```powershell
$claudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$latest = (Get-ChildItem (Join-Path $claudeDir 'plugins\cache\*\cc-statusline\*') -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -match '^\d+(\.\d+)+$' } | Sort-Object { [version]$_.Name } -Descending | Select-Object -First 1)
if (-not $latest) {
    Write-Output "ERROR: cc-statusline not found. Install first: /plugin install cc-statusline"
    exit 1
}
$latestVersion = $latest.Name
$latestPath = $latest.FullName
Write-Output "LATEST_VERSION=$latestVersion"
Write-Output "LATEST_PATH=$latestPath"
```

**macOS / Linux:**

```bash
LATEST=$(ls -d "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"/plugins/cache/*/cc-statusline/*/ 2>/dev/null | sort -V | tail -1)
if [ -z "$LATEST" ]; then
    echo "ERROR: cc-statusline not found. Install first: /plugin install cc-statusline"
    exit 1
fi
LATEST_VERSION=$(basename "$LATEST")
echo "LATEST_VERSION=$LATEST_VERSION"
echo "LATEST_PATH=$LATEST"
```

## Step 2: Read Current Version from settings.json

Read `settings.json` and extract the version from `statusLine.command`:

**Windows (PowerShell):**

```powershell
$claudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$settingsPath = Join-Path $claudeDir 'settings.json'
if (-not (Test-Path $settingsPath)) {
    Write-Output "ERROR: settings.json not found. Run /cc-statusline:setup first."
    exit 1
}
$settings = Get-Content $settingsPath -Raw | ConvertFrom-Json
$currentCmd = $settings.statusLine.command
# Extract version from path like .../cc-statusline/1.0.0/dist/index.js
$currentVersion = "unknown"
if ($currentCmd -match 'cc-statusline[/\\]([\d.]+)[/\\]') {
    $currentVersion = $matches[1]
}
Write-Output "CURRENT_VERSION=$currentVersion"
Write-Output "CURRENT_CMD=$currentCmd"
```

**macOS / Linux:**

```bash
SETTINGS="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"
if [ ! -f "$SETTINGS" ]; then
    echo "ERROR: settings.json not found. Run /cc-statusline:setup first."
    exit 1
fi
CURRENT_VERSION=$(node -e "try{process.stdout.write(require('$SETTINGS').statusLine.command.match(/cc-statusline[/\\\\]([\\d.]+)[/\\\\]/)?.[1]||'unknown')}catch(e){console.log('unknown')}")
echo "CURRENT_VERSION=$CURRENT_VERSION"
```

## Step 3: Compare Versions

Compare `LATEST_VERSION` with `CURRENT_VERSION`:

- If `LATEST_VERSION == CURRENT_VERSION`: tell the user **"Already up to date (v{version})."** and stop.
- If `LATEST_VERSION > CURRENT_VERSION`: proceed to Step 4.
- If comparison fails (unknown current version): proceed to Step 4 (repair mode).

## Step 4: Build Latest Version

Run `npm install && npm run build` in the latest version directory:

**Windows (PowerShell):**

```powershell
cd $latestPath
npm install 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Output "ERROR: npm install failed"
    exit 1
}
npm run build 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Output "ERROR: build failed"
    exit 1
}
Write-Output "BUILD_OK"
```

**macOS / Linux:**

```bash
cd "$LATEST_PATH"
npm install && npm run build
if [ $? -ne 0 ]; then
    echo "ERROR: build failed"
    exit 1
fi
echo "BUILD_OK"
```

## Step 5: Update settings.json

Replace the `statusLine.command` path with the latest version path:

The new command uses forward slashes (Claude Code handles this correctly on all platforms):

```
node "<LATEST_PATH>/dist/index.js"
```

**Windows PowerShell — UTF-8 without BOM:**

```powershell
$newCmd = "node `"$($latestPath -replace '\\','/')/dist/index.js`""
$settings = Get-Content $settingsPath -Raw | ConvertFrom-Json
$settings.statusLine.command = $newCmd
$json = $settings | ConvertTo-Json -Depth 10
$json = $json -replace '\\/', '/'  # unescape forward slashes
[System.IO.File]::WriteAllText($settingsPath, $json, (New-Object System.Text.UTF8Encoding $false))
Write-Output "PATH_UPDATED"
```

**macOS/Linux — use Node.js for JSON merge:**

```bash
node -e "
const fs = require('fs');
const s = JSON.parse(fs.readFileSync('$SETTINGS', 'utf8'));
s.statusLine.command = 'node \"$LATEST_PATH/dist/index.js\"';
fs.writeFileSync('$SETTINGS', JSON.stringify(s, null, 2));
"
```

## Step 6: Verify

Read `settings.json` and confirm the path points to the new version:

```bash
cat ~/.claude/settings.json | grep -A2 statusLine
```

Tell the user:

> **Updated to v{LATEST_VERSION}!** The status line now runs from the latest build. If it was already running, the new version takes effect on the next status line refresh (~300ms). No restart needed.
