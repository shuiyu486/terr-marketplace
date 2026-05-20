# 方向 3：对比差异（Diff / 快速检查）

覆盖 "对比"、"diff"、"有什么不同"、"快速检查"、"兼容吗"、"quick check"、"check compatibility" 等所有比较类操作。只读不写，报告本地和远程模板之间的差异。

**优化策略**：先计算 SHA256 hash，hash 一致的文件跳过全文对比。只有 hash 不同的文件才展开占位符做内容 diff。大多数时候用户只改了 1-2 个文件，其余文件 hash 一致直接跳过，配合远程获取达到与旧版"快速检查"同等甚至更低的 token 消耗。

## 第一步：获取远程模板

执行第零步（始终远程获取），得到 `$configDir`（远程缓存目录，由 Step 0b 设置）。

## 第二步：读取排除规则

解析 `~/.configsyncignore`（如存在），合并内置保护规则（env.nu 代理行）。构建 `$excludeRules`。

**轻量场景**：用户说"快速检查"/"兼容吗"时，跳过 `~/.configsyncignore` 用户排除规则，仅使用内置代理保护。用户说"对比"/"diff"时，使用完整双层排除系统。

## 第三步：Hash 级预检

对 5 个配置文件 + 2 个参考文档计算本地和模板的 SHA256 hash。hash 一致直接跳过，只有 hash 不同的文件才展开占位符做内容对比：

```powershell
# 路径映射（CLAUDE.local.md 由 $PWD 确定）
$fileMap = @{
    ".wezterm.lua"     = "$env:USERPROFILE\.wezterm.lua"
    "config.nu"        = "$env:APPDATA\nushell\config.nu"
    "env.nu"           = "$env:APPDATA\nushell\env.nu"
    "starship.toml"    = "$env:USERPROFILE\.config\starship.toml"
    "CLAUDE.local.md"  = (Join-Path $PWD.Path "CLAUDE.local.md")
}

# 检测占位符替换值（只检测一次）
$nuPath = $null
try { $nuPath = (Get-Command nu.exe -ErrorAction Stop).Source } catch {
    $nuPath = "$env:LOCALAPPDATA\Programs\nu\bin\nu.exe"
}
$gitUsrBin = "$env:ProgramFiles\Git\usr\bin"
if (-not (Test-Path $gitUsrBin)) { $gitUsrBin = "C:\Program Files\Git\usr\bin" }

$results = @()
foreach ($fname in $fileMap.Keys) {
    $tplPath = "$configDir\$fname"
    $localPath = $fileMap[$fname]

    # 文件级排除检查
    if (Test-FileExcluded $fname) {
        $results += [PSCustomObject]@{ File=$fname; Status="⏭️ 已排除"; Detail="" }
        continue
    }

    if (-not (Test-Path $tplPath)) {
        $results += [PSCustomObject]@{ File=$fname; Status="❌ 模板缺失"; Detail="" }
        continue
    }
    if (-not (Test-Path $localPath)) {
        $results += [PSCustomObject]@{ File=$fname; Status="➖ 仅模板有"; Detail="本地文件不存在" }
        continue
    }

    # Hash 对比 — 大多数文件在这一步就跳过了
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

    # 展开后相同？（env.nu 使用归一化后的本地内容，排除代理行干扰）
    $compareLocal = if ($fname -eq "env.nu") { $normalizedLocal } else { $localContent }
    if ($expanded.Trim() -eq $compareLocal.Trim()) {
        $results += [PSCustomObject]@{ File=$fname; Status="✅ 一致"; Detail="" }
        continue
    }

    # 有差异 → 提取前几处差异行
    $diffLines = @()
    $tplLines = $expanded -split "`n"
    $localLines = $compareLocal -split "`n"
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

# 参考文档对比（docs/ 下的 .md 文件，直接内容对比，无占位符展开）
$docFiles = @("config-sync-workflow.md", "compatibility-constraints.md")
$localDocsDir = Join-Path $PWD.Path "docs"
foreach ($df in $docFiles) {
    $tplDocPath = Join-Path $configDir "docs\$df"
    $localDocPath = Join-Path $localDocsDir $df

    if (-not (Test-Path $tplDocPath)) {
        $results += [PSCustomObject]@{ File="docs/$df"; Status="❌ 模板缺失"; Detail="" }
        continue
    }
    if (-not (Test-Path $localDocPath)) {
        $results += [PSCustomObject]@{ File="docs/$df"; Status="➖ 仅模板有"; Detail="本地文件不存在" }
        continue
    }

    $tplDocHash = (Get-FileHash $tplDocPath -Algorithm SHA256).Hash
    $localDocHash = (Get-FileHash $localDocPath -Algorithm SHA256).Hash

    if ($tplDocHash -eq $localDocHash) {
        $results += [PSCustomObject]@{ File="docs/$df"; Status="✅ 一致"; Detail="" }
    } else {
        $results += [PSCustomObject]@{ File="docs/$df"; Status="⚠️ 有差异"; Detail="" }
    }
}
```

## 第四步：输出差异报告

```
=== ccNovaTerm 配置对比 ===
检查时间: <当前时间>
模板源: 远程仓库（$branch 分支）

.wezterm.lua     ✅ 一致
config.nu        ✅ 一致
env.nu           ✅ 一致（代理行差异自动忽略）
starship.toml    ⚠️ 有差异
  L12: 模板='format = "$all"' → 本地='format = "$directory$git_branch"'
CLAUDE.local.md ✅ 一致

结果: 4/5 一致, 1 个文件有差异
建议: starship.toml 需要同步 → "同步到项目" 或 "同步到本地"
```

## 第五步：总结建议

- 如果所有文件一致 → 告知用户"本地配置与远程模板完全一致"
- 如果有差异 → 建议同步方向（本地→项目 或 项目→本地），让用户决定
- 如果 CLAUDE.local.md 在本地不存在 → 显示"仅模板有"，不阻塞其他文件检查
- 排除规则影响的文件单独说明

## 与旧版的变化

旧版有方向 3（完整对比）和方向 4（快速检查）两个独立方向。方向 4 存在的原因是"跳过远程获取以节省时间/网络"。新架构下远程获取是唯一的模板源，方向 4 的价值消失。合并后的方向 3 用 hash 预检实现同等轻量效果，统一为一个流程。

| 特性 | 旧方向 3 | 旧方向 4 | 新方向 3 |
|------|---------|---------|---------|
| 模板源 | 本地优先，远程备选 | 仅本地 clone | 始终远程 |
| 对比方式 | 全量占位符展开 + diff | Hash 优先 | Hash 优先 + 按需展开 |
| Token 消耗 | 较高 | 极低 | 极低（多数文件 hash 一致即跳过） |
| 依赖本地 clone | 否 | **必须** | 否 |
| 排除规则 | 完整双层 | 仅内置保护 | 完整（diff）/ 仅内置（快速检查） |
