---
description: One-click update cc-statusline — pull latest from remote, build, and relink settings.json
allowed-tools: ["Bash", "Read", "Edit", "Write"]
---

# cc-statusline Update

One-click update for already-installed users. Pulls the latest plugin from the remote marketplace, builds it, and updates `settings.json` to point to the new version. Preserves your existing `cc-statusline.json` config.

No git push/commit — this is a user-side update, not a maintainer publish.

## Step 1: Git Pull Marketplace

Pull the latest plugin code from the remote marketplace repo:

**Windows (PowerShell):**

```powershell
$claudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$marketplaceDir = Join-Path $claudeDir 'plugins\marketplaces\terr-marketplace'
cd $marketplaceDir
git pull 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Output "ERROR: git pull failed. Check network or run /plugin install cc-statusline manually."
    exit 1
}
Write-Output "MARKETPLACE_UPDATED"
```

**macOS / Linux:**

```bash
MARKETPLACE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/marketplaces/terr-marketplace"
cd "$MARKETPLACE_DIR"
git pull || { echo "ERROR: git pull failed. Check network or run /plugin install cc-statusline manually."; exit 1; }
echo "MARKETPLACE_UPDATED"
```

## Step 2: Read Latest Version from Marketplace

Read the version from the plugin's `plugin.json`:

**Windows (PowerShell):**

```powershell
$sourceDir = Join-Path $marketplaceDir 'plugins\cc-statusline'
$pluginJson = Get-Content (Join-Path $sourceDir '.claude-plugin\plugin.json') -Raw | ConvertFrom-Json
$latestVersion = $pluginJson.version
Write-Output "LATEST_VERSION=$latestVersion"
```

**macOS / Linux:**

```bash
SOURCE_DIR="$MARKETPLACE_DIR/plugins/cc-statusline"
LATEST_VERSION=$(node -e "console.log(require('$SOURCE_DIR/.claude-plugin/plugin.json').version)")
echo "LATEST_VERSION=$LATEST_VERSION"
```

## Step 3: Read Current Version from settings.json

**Windows (PowerShell):**

```powershell
$settingsPath = Join-Path $claudeDir 'settings.json'
if (-not (Test-Path $settingsPath)) {
    Write-Output "ERROR: settings.json not found. Run /cc-statusline:setup first."
    exit 1
}
$settings = Get-Content $settingsPath -Raw | ConvertFrom-Json
$currentCmd = $settings.statusLine.command
$currentVersion = "unknown"
if ($currentCmd -match 'cc-statusline[/\\]([\d.]+)[/\\]') {
    $currentVersion = $matches[1]
}
Write-Output "CURRENT_VERSION=$currentVersion"
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

## Step 4: Compare Versions

Compare `LATEST_VERSION` with `CURRENT_VERSION`:

- If `LATEST_VERSION == CURRENT_VERSION`: check if the build exists (see below). If build is intact, tell the user **"Already up to date (v{version})."** and stop. If build is missing, proceed to Step 6 (repair mode — skip copy, just rebuild).
- If `LATEST_VERSION > CURRENT_VERSION`: proceed to Step 5.
- If `CURRENT_VERSION` is "unknown" or comparison fails: proceed to Step 5 (full update — do not skip copy).

**Build existence check (when versions match):**

**Windows (PowerShell):**

```powershell
$cacheDir = Join-Path $claudeDir "plugins\cache\terr-marketplace\cc-statusline\$currentVersion"
$distFile = Join-Path $cacheDir 'dist\index.js'
if (Test-Path $distFile) {
    Write-Output "BUILD_INTACT"
} else {
    Write-Output "BUILD_MISSING"
}
```

**macOS / Linux:**

```bash
CACHE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache/terr-marketplace/cc-statusline/$CURRENT_VERSION"
if [ -f "$CACHE_DIR/dist/index.js" ]; then
    echo "BUILD_INTACT"
else
    echo "BUILD_MISSING"
fi
```

## Step 5: Copy to Cache

Copy the plugin source from marketplace to the cache directory, excluding build artifacts.

**⚠️ Skip this entire step in repair mode** (version unchanged but build missing) — the source files already exist in cache, only the build is missing. Jump directly to Step 6.

**Windows (PowerShell):**

```powershell
$cacheDir = Join-Path $claudeDir "plugins\cache\terr-marketplace\cc-statusline\$latestVersion"
# Remove existing stale copy if any
if (Test-Path $cacheDir) { Remove-Item -Recurse -Force $cacheDir }
New-Item -ItemType Directory -Force $cacheDir | Out-Null
# Copy all except node_modules and dist (will rebuild)
Copy-Item -Path "$sourceDir\*" -Destination $cacheDir -Recurse -Force
# Remove stale node_modules and dist from cache copy
Remove-Item -Recurse -Force (Join-Path $cacheDir 'node_modules') -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force (Join-Path $cacheDir 'dist') -ErrorAction SilentlyContinue
Write-Output "CACHE_COPIED=$cacheDir"
```

**macOS / Linux:**

```bash
CACHE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache/terr-marketplace/cc-statusline/$LATEST_VERSION"
rm -rf "$CACHE_DIR"
mkdir -p "$CACHE_DIR"
# Copy all except node_modules and dist
rsync -a --exclude='node_modules' --exclude='dist' --exclude='.git' "$SOURCE_DIR/" "$CACHE_DIR/"
echo "CACHE_COPIED=$CACHE_DIR"
```

## Step 6: Build

Run `npm install && npm run build` in the cache directory:

**Windows (PowerShell):**

```powershell
cd $cacheDir
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
cd "$CACHE_DIR"
npm install && npm run build || { echo "ERROR: build failed"; exit 1; }
echo "BUILD_OK"
```

## Step 7: Update settings.json

Point `statusLine.command` to the new cached build. Uses forward slashes (Claude Code handles this correctly on all platforms):

```
node "<CACHE_DIR>/dist/index.js"
```

**Windows PowerShell — UTF-8 without BOM:**

```powershell
$newCmd = "node `"$($cacheDir -replace '\\','/')/dist/index.js`""
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
s.statusLine.command = 'node \"$CACHE_DIR/dist/index.js\"';
fs.writeFileSync('$SETTINGS', JSON.stringify(s, null, 2));
"
```

## Step 8: Clean Old Versions

Remove outdated cached versions, keeping only the current one:

**Windows (PowerShell):**

```powershell
$cacheRoot = Join-Path $claudeDir 'plugins\cache\terr-marketplace\cc-statusline'
Get-ChildItem $cacheRoot -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -ne $latestVersion } | Remove-Item -Recurse -Force
Write-Output "OLD_CLEANED"
```

**macOS / Linux:**

```bash
CACHE_ROOT="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache/terr-marketplace/cc-statusline"
for d in "$CACHE_ROOT"/*/; do
    dir_name=$(basename "$d")
    if [ "$dir_name" != "$LATEST_VERSION" ]; then
        rm -rf "$d"
    fi
done
echo "OLD_CLEANED"
```

## Step 9: Verify

Read `settings.json` and confirm the path points to the new version:

```bash
cat ~/.claude/settings.json | grep -A2 statusLine
```

Tell the user:

> **Updated to v{LATEST_VERSION}!** The status line now runs from the latest build. If it was already running, the new version takes effect on the next status line refresh (~300ms). No restart needed.
> 
> Previous version was v{CURRENT_VERSION}. Old cached versions have been cleaned up.
