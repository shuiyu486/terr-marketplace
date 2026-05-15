# 方向 4：快速兼容检查（Quick Check）

用户说"快速检查"、"兼容吗"、"检查兼容性"、"quick check"时触发。**轻量模式——跳过远程获取，仅用本地 ccNovaTerm clone 做 hash 级对比。** 修改配置后快速验证是否与模板兼容，token 消耗远低于完整对比（方向 3）。

**设计理念**：完整对比每次都要远程获取 → 占位符展开 → 逐文件内容 diff，即使文件完全一致也消耗大量 token。快速检查翻转流程：**先用 SHA256 hash 判断有无变化，只有 hash 不同时才展开占位符做内容对比。** 大多数时候用户只改了 1-2 个文件，其余文件 hash 一致直接跳过。

**排除规则说明**：快速检查为保持轻量，跳过 `~/.configsyncignore` 用户排除规则，仅使用内联保护（env.nu 代理行 + settings.json 字段过滤）。如需完整双层排除系统，使用方向 3（完整对比）。

## 4a. 定位本地 ccNovaTerm 项目（不执行远程获取）

```powershell
$repoRoot = $null
$candidates = @(
    $PWD.Path,
    "$($PWD.Path)\ccNovaTerm",
    "$env:USERPROFILE\ccNovaTerm"
)
foreach ($c in $candidates) {
    if (Test-Path "$c\config\.wezterm.lua") { $repoRoot = $c; break }
}
if (-not $repoRoot) {
    Write-Output "未找到本地 ccNovaTerm 项目。快速检查需要本地 clone，请执行："
    Write-Output "  git clone https://github.com/shuiyu486/ccNovaTerm ~/ccNovaTerm"
    Write-Output "或使用完整对比模式——自动从远程获取模板。"
    exit 1
}
$configDir = "$repoRoot\config"
Write-Output "项目路径: $repoRoot"
```

## 4b. 检测本地 clone 是否过期

```powershell
$repoIsStale = $false
$behindCount = 0
git -C $repoRoot fetch --quiet 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Output "(无法连接远程仓库，跳过新鲜度检测)"
} else {
    $currentBranch = (git -C $repoRoot rev-parse --abbrev-ref HEAD 2>$null).Trim()
    if ($currentBranch) {
        $behindCount = [int](git -C $repoRoot rev-list --count "HEAD..origin/$currentBranch" 2>$null)
    }
}
if ($behindCount -gt 0) {
    Write-Output "WARNING: 本地项目落后远程 $behindCount 个提交，检查结果可能不是最新的。"
    Write-Output "建议先更新：git -C $repoRoot pull"
    Write-Output "或使用完整对比模式——自动从远程获取最新模板。"
    $repoIsStale = $true
}
```

检测失败（无网络等）不阻塞检查——静默跳过，继续使用本地版本。

## 4c. Hash 级快速对比

对 7 个文件计算 SHA256。**hash 一致直接跳过，只有 hash 不同的文件才展开占位符做内容 diff：**

```powershell
# 路径映射
$fileMap = @{
    ".wezterm.lua"     = "$env:USERPROFILE\.wezterm.lua"
    "config.nu"        = "$env:APPDATA\nushell\config.nu"
    "env.nu"           = "$env:APPDATA\nushell\env.nu"
    "starship.toml"    = "$env:USERPROFILE\.config\starship.toml"
    "statusline.ps1"   = "$env:USERPROFILE\.claude\statusline.ps1"
    "settings.json"    = "$env:USERPROFILE\.claude\settings.json"
    "CLAUDE.local.md"  = "$repoRoot\CLAUDE.local.md"
}

# 检测占位符替换值（只需检测一次）
$nuPath = $null
try { $nuPath = (Get-Command nu.exe -ErrorAction Stop).Source } catch {
    $nuPath = "$env:LOCALAPPDATA\Programs\nu\bin\nu.exe"
}
$gitUsrBin = "$env:ProgramFiles\Git\usr\bin"
if (-not (Test-Path $gitUsrBin)) { $gitUsrBin = "C:\Program Files\Git\usr\bin" }
$username = Split-Path -Leaf $env:USERPROFILE

$results = @()
foreach ($fname in $fileMap.Keys) {
    $tplPath = "$configDir\$fname"
    $localPath = $fileMap[$fname]

    if (-not (Test-Path $tplPath)) {
        $results += [PSCustomObject]@{ File=$fname; Status="⚠️ 模板缺失"; Detail="" }
        continue
    }
    if (-not (Test-Path $localPath)) {
        $results += [PSCustomObject]@{ File=$fname; Status="➖ 仅模板有"; Detail="本地文件不存在" }
        continue
    }

    # Hash 对比 —— 大多数文件在这一步就跳过了
    $tplHash = (Get-FileHash $tplPath -Algorithm SHA256).Hash
    $localHash = (Get-FileHash $localPath -Algorithm SHA256).Hash

    if ($tplHash -eq $localHash) {
        $results += [PSCustomObject]@{ File=$fname; Status="✅ 一致"; Detail="" }
        continue
    }

    # Hash 不同 → 展开占位符做内容对比
    $tplContent = [System.Text.Encoding]::UTF8.GetString([System.IO.File]::ReadAllBytes($tplPath))
    $localContent = [System.Text.Encoding]::UTF8.GetString([System.IO.File]::ReadAllBytes($localPath))

    # 展开占位符（双反斜杠用于 Lua/Nushell 转义）
    $expanded = $tplContent
    $expanded = $expanded -replace '__NU_PATH__', ($nuPath -replace '\\', '\\')
    $expanded = $expanded -replace '__GIT_USR_BIN__', ($gitUsrBin -replace '\\', '\\')
    $expanded = $expanded -replace '__USERNAME__', $username

    # settings.json 特殊处理：只对比 statusLine 字段
    if ($fname -eq "settings.json") {
        $tplJson = $expanded | ConvertFrom-Json
        $localJson = $localContent | ConvertFrom-Json
        $tplSL = ($tplJson.statusLine | ConvertTo-Json -Compress)
        $localSL = if ($localJson.statusLine) { ($localJson.statusLine | ConvertTo-Json -Compress) } else { "" }
        if ($tplSL -eq $localSL) {
            $results += [PSCustomObject]@{ File=$fname; Status="✅ 一致"; Detail="statusLine 相同（本地有其他字段）" }
        } else {
            $results += [PSCustomObject]@{ File=$fname; Status="⚠️ 有差异"; Detail="statusLine 不同" }
        }
        continue
    }

    # env.nu 代理行保护：模板中注释的 load-env 与本地激活的 load-env 视为一致
    if ($fname -eq "env.nu") {
        $normalizedLocal = ($localContent -split "`n" | ForEach-Object {
            if ($_ -match '^\s*load-env') { "# $_" } else { $_ }
        }) -join "`n"
        if ($expanded.Trim() -eq $normalizedLocal.Trim()) {
            $results += [PSCustomObject]@{ File=$fname; Status="✅ 一致"; Detail="（代理行差异自动忽略）" }
            continue
        }
    }

    # 内容对比：展开后相同？
    if ($expanded.Trim() -eq $localContent.Trim()) {
        $results += [PSCustomObject]@{ File=$fname; Status="✅ 一致"; Detail="" }
        continue
    }

    # 有差异 → 提取前几处差异行
    $diffLines = @()
    $tplLines = $expanded -split "`n"
    $localLines = $localContent -split "`n"
    $maxLen = [Math]::Max($tplLines.Count, $localLines.Count)
    for ($i = 0; $i -lt $maxLen; $i++) {
        $tplLine = if ($i -lt $tplLines.Count) { $tplLines[$i].Trim() } else { "<EOF>" }
        $localLine = if ($i -lt $localLines.Count) { $localLines[$i].Trim() } else { "<EOF>" }
        if ($tplLine -ne $localLine) {
            $diffLines += "  L$($i+1): 模板='$tplLine' → 本地='$localLine'"
            if ($diffLines.Count -ge 5) { $diffLines += "  ... (仅显示前 5 处差异)"; break }
        }
    }
    $results += [PSCustomObject]@{ File=$fname; Status="⚠️ 有差异"; Detail=($diffLines -join "`n") }
}
```

## 4d. 输出精简报告

```
=== ccNovaTerm 兼容性快速检查 ===
项目路径: <repoRoot>
本地项目状态: <最新/落后 N 个提交/未检测>
检查时间: <当前时间>

.wezterm.lua     ✅ 一致
config.nu        ✅ 一致
env.nu           ✅ 一致（代理行差异自动忽略）
starship.toml    ⚠️ 有差异
  L12: 模板='format = "$all"' → 本地='format = "$directory$git_branch"'
statusline.ps1   ✅ 一致
settings.json    ✅ 一致（本地有其他字段）
CLAUDE.local.md ✅ 一致

结果: 6/7 兼容, 1 个文件有差异
建议: starship.toml 需要同步 → "同步到项目" 或 "同步到本地"
```

如果本地项目过期（`$repoIsStale -eq $true`），在"本地项目状态"行显示落后提交数，并在建议区追加：`⚠️ 本地项目落后远程，建议先 git pull 再检查。`

## 与完整对比（方向 3）的区别

| 特性 | 快速检查（方向 4） | 完整对比（方向 3） |
|------|-------------------|-------------------|
| 远程获取 | 跳过 | 执行 |
| 新鲜度检测 | `git fetch` + 比较 HEAD | 直接从远程获取最新 |
| 对比方式 | Hash 优先，仅变化时内容对比 | 全量占位符展开 + 逐文件内容 diff |
| Token 消耗 | **极低**（无变更文件 hash 一致即跳过） | 较高 |
| 适用场景 | 修改配置后快速验证 | 首次对比、无本地 clone 时、需要完整 diff |
| 依赖本地 clone | **必须** | 自动远程获取 |
| 排除规则 | 复用内置代理保护 + settings.json 字段过滤 | 完整双层排除系统 |
