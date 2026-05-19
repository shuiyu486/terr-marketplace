# Paths Reference

## Local Environment Paths (Windows)

| Config | Absolute Path |
|--------|--------------|
| WezTerm | `$env:USERPROFILE\.wezterm.lua` |
| Nushell config | `$env:APPDATA\nushell\config.nu` (i.e., `~\AppData\Roaming\nushell\config.nu`) |
| Nushell env | `$env:APPDATA\nushell\env.nu` |
| Starship | `$env:USERPROFILE\.config\starship.toml` |
| CLAUDE.local.md | `Join-Path $PWD.Path "CLAUDE.local.md"`（当前工作目录，文件不存在则跳过） |

CLAUDE.local.md 是唯一不位于用户 home 目录的文件，其本地路径由 `$PWD` 决定。如果当前目录下没有该文件，此文件不会参与同步。

## ccNovaTerm Project Template Paths

All under `<repo-root>/config/`:

| Template | File |
|----------|------|
| WezTerm | `config/.wezterm.lua` |
| Nushell config | `config/config.nu` |
| Nushell env | `config/env.nu` |
| Starship | `config/starship.toml` |
| CLAUDE.local.md | `config/CLAUDE.local.md` |

## Template Source

**模板源仅从远程获取。本地项目不参与同步操作。**

1. **Remote fetch** — 从 GitHub raw 获取到临时缓存（Step 0b），对所有操作类型生效
2. **Ask user** — 远程获取失败时，由用户提供路径或手动 clone

临时 clone 仅用于方向 1（push）的写入和 git push。

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

If both fail, the remote repo may use a different branch name — ask the user or fall back to manual path entry.

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

这是所有操作（对比、同步到本地、同步到项目）的**主模板源**。每次操作从远程 GitHub raw 获取并缓存到此目录。Session 级别，下次获取或系统 temp 清理时清除。

## Temporary Clone Directory (push operations)

`$env:TEMP\ccNovaTerm-push-<yyyyMMddHHmmss>\`

所有 push 操作均通过临时 clone 执行：
- 浅克隆（`git clone --depth 1`）创建于此
- 模板文件写入、提交、推送
- 推送成功后**自动删除**
- 推送失败时保留目录，告知用户路径以便手动处理

## Backup Directory

`$env:USERPROFILE\ccNovaTerm-backup\<yyyyMMdd_HHmmss>\`
