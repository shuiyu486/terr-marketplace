---
description: One-click update cc-statusline — pull latest, migrate config, rebuild, relink settings.json, and restart statusline
allowed-tools: ["Bash", "PowerShell", "Read", "Edit", "Write"]
---

# cc-statusline Update

One-click repair-style update for already-installed users. Pulls the latest plugin into Claude Code's installed marketplace clone, rebuilds the runtime cache even when the version is unchanged, migrates `cc-statusline.json`, updates `settings.json`, updates the plugin registry, and restarts the status line.

Existing config values are preserved when valid. Missing config files are created with complete defaults; corrupt config JSON is backed up before defaults are written.

No git push/commit and no maintainer working tree changes — this is a user-side update, not a maintainer publish.

## Step 1: Git Pull Installed Marketplace Clone

Pull the latest plugin code in Claude Code's installed marketplace clone:

**Windows (PowerShell):**

```powershell
$claudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$marketplaceDir = Join-Path $claudeDir 'plugins\marketplaces\terr-marketplace'
Set-Location $marketplaceDir
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
$currentVersion = 'unknown'
if (Test-Path $settingsPath) {
    $currentVersion = node -e "const fs = require('fs'); try { const s = JSON.parse(fs.readFileSync(process.argv[1], 'utf8')); const m = String(s.statusLine?.command ?? '').match(/cc-statusline[/\\]([\d.]+)[/\\]/); process.stdout.write(m?.[1] ?? 'unknown'); } catch { process.stdout.write('unknown'); }" $settingsPath
}
Write-Output "CURRENT_VERSION=$currentVersion"
```

**macOS / Linux:**

```bash
SETTINGS="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"
if [ -f "$SETTINGS" ]; then
  CURRENT_VERSION=$(node -e "try{process.stdout.write(require('$SETTINGS').statusLine?.command?.match(/cc-statusline[/\\]([\d.]+)[/\\]/)?.[1]||'unknown')}catch(e){process.stdout.write('unknown')}")
else
  CURRENT_VERSION="unknown"
fi
echo "CURRENT_VERSION=$CURRENT_VERSION"
```

## Step 4: Decide Update Mode

Always continue. Version equality does not skip copy/build/relink/restart because the installed marketplace clone may have changed after `git pull`, or cache/runtime may still contain an older build.

**Windows (PowerShell):**

```powershell
if ($currentVersion -eq $latestVersion) {
    Write-Output "SAME_VERSION_REFRESH=$latestVersion"
} elseif ($currentVersion -eq 'unknown') {
    Write-Output "CURRENT_VERSION_UNKNOWN_REFRESH"
} else {
    Write-Output "VERSION_UPDATE=$currentVersion->$latestVersion"
}
```

**macOS / Linux:**

```bash
if [ "$CURRENT_VERSION" = "$LATEST_VERSION" ]; then
  echo "SAME_VERSION_REFRESH=$LATEST_VERSION"
elif [ "$CURRENT_VERSION" = "unknown" ]; then
  echo "CURRENT_VERSION_UNKNOWN_REFRESH"
else
  echo "VERSION_UPDATE=$CURRENT_VERSION->$LATEST_VERSION"
fi
```

## Step 5: Copy to Temporary Cache

Copy the plugin source from the installed marketplace clone to a temporary cache directory, excluding build artifacts. The final cache directory is replaced only after the build succeeds.

**Windows (PowerShell):**

```powershell
$cacheRoot = Join-Path $claudeDir 'plugins\cache\terr-marketplace\cc-statusline'
$cacheDir = Join-Path $cacheRoot $latestVersion
$tempCacheDir = Join-Path $cacheRoot "$latestVersion.tmp-update"
if (Test-Path $tempCacheDir) { Remove-Item -Recurse -Force $tempCacheDir }
New-Item -ItemType Directory -Force $tempCacheDir | Out-Null
Get-ChildItem -LiteralPath $sourceDir -Force | Where-Object {
    $_.Name -notin @('node_modules', 'dist', '.git')
} | Copy-Item -Destination $tempCacheDir -Recurse -Force
Write-Output "CACHE_COPIED=$tempCacheDir"
```

**macOS / Linux:**

```bash
CACHE_ROOT="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins/cache/terr-marketplace/cc-statusline"
CACHE_DIR="$CACHE_ROOT/$LATEST_VERSION"
TEMP_CACHE_DIR="$CACHE_ROOT/$LATEST_VERSION.tmp-update"
rm -rf "$TEMP_CACHE_DIR"
mkdir -p "$TEMP_CACHE_DIR"
rsync -a --exclude='node_modules' --exclude='dist' --exclude='.git' "$SOURCE_DIR/" "$TEMP_CACHE_DIR/"
echo "CACHE_COPIED=$TEMP_CACHE_DIR"
```

## Step 6: Build Temporary Cache

Run `npm install && npm run build` in the temporary cache directory:

**Windows (PowerShell):**

```powershell
Set-Location $tempCacheDir
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
cd "$TEMP_CACHE_DIR"
npm install && npm run build || { echo "ERROR: build failed"; exit 1; }
echo "BUILD_OK"
```

## Step 7: Stop Running Statusline and Promote Cache

Stop existing cc-statusline Node processes, then replace the versioned cache directory with the freshly built temporary cache.

**Windows (PowerShell):**

```powershell
$cacheRootForMatch = $cacheRoot -replace '\\','/'
$escapedRoot = [regex]::Escape($cacheRootForMatch)
$pattern = "$escapedRoot/.+/dist/index\.js"
$stopped = 0
Get-CimInstance Win32_Process | Where-Object {
    $_.Name -eq 'node.exe' -and (($_.CommandLine -replace '\\','/') -match $pattern)
} | ForEach-Object {
    Stop-Process -Id $_.ProcessId -Force -Confirm:$false
    $stopped++
}
if (Test-Path $cacheDir) { Remove-Item -Recurse -Force $cacheDir }
Move-Item -Path $tempCacheDir -Destination $cacheDir
Write-Output "STATUSLINE_RESTARTED=$stopped"
Write-Output "CACHE_PROMOTED=$cacheDir"
```

**macOS / Linux:**

```bash
STOPPED=0
while IFS= read -r pid; do
    kill "$pid" 2>/dev/null && STOPPED=$((STOPPED + 1))
done < <(ps -eo pid=,args= | awk -v root="$CACHE_ROOT" '$0 ~ /node/ && index($0, root) && $0 ~ /\/dist\/index\.js/ { print $1 }')
rm -rf "$CACHE_DIR"
mv "$TEMP_CACHE_DIR" "$CACHE_DIR"
echo "STATUSLINE_RESTARTED=$STOPPED"
echo "CACHE_PROMOTED=$CACHE_DIR"
```

## Step 8: Migrate cc-statusline.json

Use the freshly built shared config module to create, repair, or backfill the user config file.

**Windows (PowerShell):**

```powershell
node (Join-Path $cacheDir 'dist\configCli.js') migrate
if ($LASTEXITCODE -ne 0) {
    Write-Output "ERROR: config migration failed"
    exit 1
}
```

**macOS / Linux:**

```bash
node "$CACHE_DIR/dist/configCli.js" migrate || { echo "ERROR: config migration failed"; exit 1; }
```

## Step 9: Update settings.json

Point `statusLine.command` to the new cached build. Uses forward slashes (Claude Code handles this correctly on all platforms):

```text
node "<CACHE_DIR>/dist/index.js"
```

**Windows PowerShell — UTF-8 without BOM:**

```powershell
node -e "const fs = require('fs'); const p = process.argv[1]; const cacheDir = process.argv[2].replace(/\\/g, '/'); const quote = String.fromCharCode(34); let s = {}; try { s = JSON.parse(fs.readFileSync(p, 'utf8')); } catch {} s.statusLine = s.statusLine || {}; s.statusLine.type = 'command'; s.statusLine.command = 'node ' + quote + cacheDir + '/dist/index.js' + quote; fs.writeFileSync(p, JSON.stringify(s, null, 2) + '\n', 'utf8');" $settingsPath $cacheDir
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
const p = process.argv[1];
const cacheDir = process.argv[2];
let s = {};
try { s = JSON.parse(fs.readFileSync(p, 'utf8')); } catch {}
s.statusLine = s.statusLine || {};
s.statusLine.type = 'command';
s.statusLine.command = 'node \"' + cacheDir + '/dist/index.js\"';
fs.writeFileSync(p, JSON.stringify(s, null, 2) + '\n', 'utf8');
" "$SETTINGS" "$CACHE_DIR" || { echo "ERROR: settings.json update failed"; exit 1; }
echo "PATH_UPDATED"
```

## Step 10: Update Plugin Registry

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

## Step 11: Clean Old Versions

Remove outdated cached versions, keeping only the current one:

**Windows (PowerShell):**

```powershell
Get-ChildItem $cacheRoot -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -ne $latestVersion } | Remove-Item -Recurse -Force
Write-Output "OLD_CLEANED"
```

**macOS / Linux:**

```bash
for d in "$CACHE_ROOT"/*/; do
    dir_name=$(basename "$d")
    if [ "$dir_name" != "$LATEST_VERSION" ]; then
        rm -rf "$d"
    fi
done
echo "OLD_CLEANED"
```

## Step 12: Verify

Read `settings.json`, `installed_plugins.json`, and `cc-statusline.json` to confirm the runtime, slash-command registry, and user config were refreshed:

**Windows (PowerShell):**

```powershell
Get-Content (Join-Path $claudeDir 'settings.json') | Select-String -Pattern 'statusLine' -Context 0,2
Get-Content (Join-Path $claudeDir 'plugins\installed_plugins.json') | Select-String -Pattern 'cc-statusline@terr-marketplace' -Context 0,8
Get-Content (Join-Path $claudeDir 'cc-statusline.json')
```

**macOS / Linux:**

```bash
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
grep -A2 'statusLine' "$CLAUDE_DIR/settings.json"
grep -A8 'cc-statusline@terr-marketplace' "$CLAUDE_DIR/plugins/installed_plugins.json"
cat "$CLAUDE_DIR/cc-statusline.json"
```

Tell the user:

> **Updated/refreshed to v{LATEST_VERSION}!** The status line now runs from the freshly rebuilt cache. `cc-statusline.json` has been created, repaired, or backfilled as needed, and existing cc-statusline processes were stopped so Claude Code will start the updated status line on the next refresh.
>
> Previous version was v{CURRENT_VERSION}. Old cached versions have been cleaned up. Run `/reload-plugins` to refresh slash command registration in the current Claude Code session.
