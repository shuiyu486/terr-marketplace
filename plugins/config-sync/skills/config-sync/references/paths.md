# Paths Reference

## Local Environment Paths (Windows)

| Config | Absolute Path |
|--------|--------------|
| WezTerm | `$env:USERPROFILE\.wezterm.lua` |
| Nushell config | `$env:APPDATA\nushell\config.nu` (i.e., `~\AppData\Roaming\nushell\config.nu`) |
| Nushell env | `$env:APPDATA\nushell\env.nu` |
| Starship | `$env:USERPROFILE\.config\starship.toml` |
| Claude statusline | `$env:USERPROFILE\.claude\statusline.ps1` |
| Claude settings | `$env:USERPROFILE\.claude\settings.json` |
| CLAUDE.local.md | `$repoRoot\CLAUDE.local.md`（项目根目录，由 Step 0 的 `$repoRoot` 确定） |

## ccNovaTerm Project Template Paths

All under `<repo-root>/config/`:

| Template | File |
|----------|------|
| WezTerm | `config/.wezterm.lua` |
| Nushell config | `config/config.nu` |
| Nushell env | `config/env.nu` |
| Starship | `config/starship.toml` |
| Claude statusline | `config/statusline.ps1` |
| Claude settings | `config/settings.json` |
| CLAUDE.local.md | `config/CLAUDE.local.md` |

## Finding ccNovaTerm Repo Root (优先顺序)

1. **Current working directory** — if it contains `config/.wezterm.lua`
2. **Default local path** — `$env:USERPROFILE\ccNovaTerm\`
3. **Remote fetch** (contrast & pull only) — fetch from GitHub raw, cache to temp
4. **Ask user** — if all above fail (or push operation with no local clone)

## Remote Repository URL

Repository metadata is stored in the plugin directory at:
`$env:USERPROFILE\.claude\plugins\cache\terr-marketplace\config-sync\<version>\.claude-plugin\plugin.json`

**Use a version-agnostic path** to survive plugin upgrades:

```powershell
$pluginBase = "$env:USERPROFILE\.claude\plugins\cache\terr-marketplace\config-sync"
$versions = Get-ChildItem $pluginBase -Directory -ErrorAction SilentlyContinue | Sort-Object Name -Descending
if ($versions) {
    $pluginJson = Get-Content "$($versions[0].FullName)\.claude-plugin\plugin.json" -Raw -Encoding UTF8 | ConvertFrom-Json
    $repoUrl = $pluginJson.repository
} else {
    $repoUrl = "https://github.com/shuiyu486/ccNovaTerm"
}
# Example result: https://github.com/shuiyu486/ccNovaTerm
```

### Deriving raw file URLs

Convert GitHub URL to raw content URL:

```powershell
# https://github.com/shuiyu486/ccNovaTerm
# → https://raw.githubusercontent.com/shuiyu486/ccNovaTerm
$rawBase = $repoUrl -replace 'https://github.com/', 'https://raw.githubusercontent.com/' -replace '\.git$', ''

# Raw file URL: $rawBase/$branch/config/<filename>
# Example: https://raw.githubusercontent.com/shuiyu486/ccNovaTerm/main/config/.wezterm.lua
```

### Default branch detection

Try `main` first, fall back to `master` if 404:

```powershell
$branch = "main"
$testUrl = "$rawBase/$branch/config/.wezterm.lua"
try {
    $null = Invoke-WebRequest -Uri $testUrl -UseBasicParsing -TimeoutSec 5
} catch {
    $branch = "master"
}
```

If both fail, the remote repo may use a different branch name — ask the user or fall back to step 4 (ask user for path).

### Fetching files safely (preserving UTF-8 bytes)

Use `System.Net.WebClient` to download raw bytes — avoids PowerShell's text encoding interference:

```powershell
$wc = New-Object System.Net.WebClient
foreach ($f in $files) {
    $url = "$rawBase/$branch/config/$f"
    try {
        $bytes = $wc.DownloadData($url)
        [System.IO.File]::WriteAllBytes("$cacheDir\$f", $bytes)
    } catch {
        Write-Output "Remote fetch failed for $f"
    }
}
```

**Do NOT use** `Invoke-WebRequest` + `.Content` — PowerShell decodes `.Content` as text using system encoding, which corrupts Nerd Font PUA characters in `starship.toml`. `Invoke-WebRequest` `.RawContentStream` is fine but `WebClient.DownloadData` is simpler.

## Remote Cache Directory

`$env:TEMP\ccNovaTerm-remote-config\`

This directory stores config templates fetched from the remote repository for **read-only** operations (对比 and 项目→本地). It is:
- **Session-scoped** — cleared on next fetch or system temp cleanup
- **Read-only** — never write back to this directory

## Temporary Clone Directory (push operations)

`$env:TEMP\ccNovaTerm-push-<yyyyMMddHHmmss>\`

When pushing configs to the remote repository without a local clone (方向 1 路径 B):
- A shallow clone (`git clone --depth 1`) is created here
- Template files are written, committed, and pushed
- The directory is **automatically deleted** after successful push
- If push fails: directory is preserved, user is told the path so they can manually resolve

## Backup Directory

`$env:USERPROFILE\ccNovaTerm-backup\<yyyyMMdd_HHmmss>\`

## Cache Directory (statusline runtime)

`$env:TEMP\ccNovaTerm-statusline-cache\ses-{PID}.txt`
