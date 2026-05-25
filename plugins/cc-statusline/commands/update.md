---
description: One-click update cc-statusline — pull latest from remote, build, relink settings.json, and restart statusline
allowed-tools: ["Bash", "PowerShell", "Read", "Edit", "Write"]
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
$currentVersion = node -e "const fs = require('fs'); try { const s = JSON.parse(fs.readFileSync(process.argv[1], 'utf8')); const m = String(s.statusLine?.command ?? '').match(/cc-statusline[/\\\\]([\\d.]+)[/\\\\]/); process.stdout.write(m?.[1] ?? 'unknown'); } catch { process.stdout.write('unknown'); }" $settingsPath
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
node -e "const fs = require('fs'); const p = process.argv[1]; const cacheDir = process.argv[2].replace(/\\\\/g, '/'); const quote = String.fromCharCode(34); const s = JSON.parse(fs.readFileSync(p, 'utf8')); s.statusLine = s.statusLine || { type: 'command' }; s.statusLine.type = 'command'; s.statusLine.command = 'node ' + quote + cacheDir + '/dist/index.js' + quote; fs.writeFileSync(p, JSON.stringify(s, null, 2) + '\n', 'utf8');" $settingsPath $cacheDir
if ($LASTEXITCODE -ne 0) {
    Write-Output "ERROR: settings.json update failed"
    exit 1
}
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

## Step 8: Update Plugin Registry

Update Claude Code's plugin registry so slash commands are registered from the same cached version as the status line runtime.

**Windows PowerShell — use Node.js to preserve JSON encoding:**

```powershell
node -e "
const fs = require('fs');
const p = process.argv[1];
const installPath = process.argv[2];
const version = process.argv[3];
const gitCommitSha = process.argv[4];
const data = JSON.parse(fs.readFileSync(p, 'utf8'));
const key = 'cc-statusline@terr-marketplace';
const entries = data.installedPlugins?.[key] ?? data.plugins?.[key] ?? data[key];
if (!Array.isArray(entries) || entries.length === 0) throw new Error('cc-statusline plugin registry entry not found');
for (const entry of entries) {
  if (entry.scope === 'user' || entries.length === 1) {
    entry.installPath = installPath;
    entry.version = version;
    entry.lastUpdated = new Date().toISOString();
    if (gitCommitSha) entry.gitCommitSha = gitCommitSha;
  }
}
fs.writeFileSync(p, JSON.stringify(data, null, 2) + '\n', 'utf8');
" (Join-Path $claudeDir 'plugins\installed_plugins.json') $cacheDir $latestVersion (git -C $marketplaceDir rev-parse HEAD)
if ($LASTEXITCODE -ne 0) {
    Write-Output "ERROR: plugin registry update failed"
    exit 1
}
Write-Output "PLUGIN_REGISTRY_UPDATED"
```

**macOS/Linux:**

```bash
node -e "
const fs = require('fs');
const p = process.argv[1];
const installPath = process.argv[2];
const version = process.argv[3];
const gitCommitSha = process.argv[4];
const data = JSON.parse(fs.readFileSync(p, 'utf8'));
const key = 'cc-statusline@terr-marketplace';
const entries = data.installedPlugins?.[key] ?? data.plugins?.[key] ?? data[key];
if (!Array.isArray(entries) || entries.length === 0) throw new Error('cc-statusline plugin registry entry not found');
for (const entry of entries) {
  if (entry.scope === 'user' || entries.length === 1) {
    entry.installPath = installPath;
    entry.version = version;
    entry.lastUpdated = new Date().toISOString();
    if (gitCommitSha) entry.gitCommitSha = gitCommitSha;
  }
}
fs.writeFileSync(p, JSON.stringify(data, null, 2) + '\n', 'utf8');
" "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/installed_plugins.json" "$CACHE_DIR" "$LATEST_VERSION" "$(git -C "$MARKETPLACE_DIR" rev-parse HEAD)" || { echo "ERROR: plugin registry update failed"; exit 1; }
echo "PLUGIN_REGISTRY_UPDATED"
```

## Step 9: Restart Running Statusline

Stop existing cc-statusline Node processes so the next Claude Code status-line refresh loads the updated build. Match only Node processes whose command line points at `plugins/cache/terr-marketplace/cc-statusline/*/dist/index.js`.

**Windows (PowerShell):**

```powershell
$cacheRootForMatch = (Join-Path $claudeDir 'plugins\cache\terr-marketplace\cc-statusline') -replace '\\','/'
$escapedRoot = [regex]::Escape($cacheRootForMatch)
$pattern = "$escapedRoot/.+/dist/index\.js"
$stopped = 0
Get-CimInstance Win32_Process | Where-Object {
    $_.Name -eq 'node.exe' -and (($_.CommandLine -replace '\\','/') -match $pattern)
} | ForEach-Object {
    Stop-Process -Id $_.ProcessId -Force -Confirm:$false
    $stopped++
}
Write-Output "STATUSLINE_RESTARTED=$stopped"
```

**macOS / Linux:**

```bash
CACHE_ROOT="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache/terr-marketplace/cc-statusline"
STOPPED=0
while IFS= read -r pid; do
    kill "$pid" 2>/dev/null && STOPPED=$((STOPPED + 1))
done < <(ps -eo pid=,args= | awk -v root="$CACHE_ROOT" '$0 ~ /node/ && index($0, root) && $0 ~ /\/dist\/index\.js/ { print $1 }')
echo "STATUSLINE_RESTARTED=$STOPPED"
```

## Step 10: Clean Old Versions

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

## Step 11: Verify

Read `settings.json` and `installed_plugins.json` to confirm both the status-line runtime and slash-command registry point to the new version:

```bash
cat ~/.claude/settings.json | grep -A2 statusLine
cat ~/.claude/plugins/installed_plugins.json | grep -A8 'cc-statusline@terr-marketplace'
```

Tell the user:

> **Updated to v{LATEST_VERSION}!** The status line now runs from the latest build. Existing cc-statusline processes were stopped, so Claude Code will start the updated status line on the next refresh.
> 
> Previous version was v{CURRENT_VERSION}. Old cached versions have been cleaned up. Run `/reload-plugins` to refresh slash command registration in the current Claude Code session.
