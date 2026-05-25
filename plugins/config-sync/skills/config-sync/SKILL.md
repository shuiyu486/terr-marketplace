---
name: config-sync
description: Two-way sync, diff, and quick compatibility check of terminal configs between local environment and ccNovaTerm.
disable-model-invocation: true
compatibility: Windows (PowerShell 5.1+), primary template source is remote GitHub fetch (no local project auto-discovery)
---

# Config Sync — 终端配置双向同步与对比

在本地环境（`~/`）和 ccNovaTerm 项目（`config/`）之间同步或对比配置文件。同步前总是先备份后写入。

## 执行策略（必读！）

**所有多行 PowerShell 代码必须使用 Claude Code 原生的 `PowerShell` 工具执行，严禁使用 `Bash` 工具包装 PowerShell 命令。**

原因：`Bash` 工具通过 bash 传递命令，bash 会将 PowerShell here-string 语法 `@'...'@` 中的单引号当作自己的字符串定界符，导致命令在到达 PowerShell 之前就被破坏，引发 `ParserError: UnrecognizedToken`。

具体规则：
- **多行 PowerShell（3 行及以上）**：必须用 `PowerShell` 工具，将代码块直接作为 `command` 参数
- **单行 PowerShell（1-2 行）**：优先用 `PowerShell` 工具，短命令也可用 `Bash(powershell -NoProfile -Command "...")`（双引号，不能有内嵌双引号）
- **绝对禁止**：`Bash(powershell -NoProfile -Command @'...'@)` — 这里的 `@'...'@` here-string 在 bash 中必然失败
- 如需在 Bash 工具中运行 PowerShell，使用 `-EncodedCommand` 配合 Base64 编码，或将脚本写入临时 `.ps1` 文件后通过 `-File` 执行
- `PowerShell` 工具是 Windows PowerShell 5.1，与本插件兼容；语法注意事项（无三元运算符、无双引号插值等）已在下文代码中适配

## 第零步：获取远程配置模板源（所有操作之前强制执行！）

**这是最容易出错的步骤——跳过会导致盲目假设。** 所有操作从远程 GitHub 仓库获取模板基准，**不需要也不使用本地项目 clone**。本地 ccNovaTerm 项目仅用于编辑技能和文档，不参与同步操作。临时 clone 是 push 操作的自动实现细节。

### 0a. 确定操作类型并获取远程仓库 URL

| 操作 | 触发词 | 最终需要 push？ |
|------|--------|---------------|
| 对比差异 | "对比"、"diff"、"compare"、"有什么不同"、"快速检查"、"兼容吗"、"quick check"、"check compatibility" | 否 |
| 项目→本地 | "同步到本地"、"pull"、"apply" | 否 |
| 本地→项目 | "同步到项目"、"push"、"更新模板" | 是（通过临时 clone） |

```powershell
# 尝试从插件元数据读取仓库 URL（版本号用通配符，适应升级）
$pluginBase = "$env:USERPROFILE\.claude\plugins\cache\terr-marketplace\config-sync"
$versions = Get-ChildItem $pluginBase -Directory -ErrorAction SilentlyContinue | Sort-Object Name -Descending
if ($versions -and (Test-Path "$($versions[0].FullName)\.claude-plugin\plugin.json")) {
    $pluginJson = Get-Content "$($versions[0].FullName)\.claude-plugin\plugin.json" -Raw -Encoding UTF8 | ConvertFrom-Json
    $repoUrl = $pluginJson.repository
} else {
    # Fallback: 硬编码仓库地址（插件元数据不可用时的最后手段）
    $repoUrl = "https://github.com/shuiyu486/ccNovaTerm"
}
$rawBase = $repoUrl -replace 'https://github.com/', 'https://raw.githubusercontent.com/' -replace '\.git$', ''
```

### 0b. 远程获取（唯一模板源）

从 GitHub raw 获取模板文件作为基准。

**默认分支检测**——先试 `main`，如 404 则回退到 `master`：

```powershell
$branch = "main"
$testUrl = "$rawBase/$branch/config/.wezterm.lua"
try {
    $null = Invoke-WebRequest -Uri $testUrl -UseBasicParsing -TimeoutSec 5
} catch {
    $branch = "master"
}
```

**逐个获取 5 个模板文件**，使用 `WebClient.DownloadData` 获取原始字节（避免 PowerShell 的文本编码干扰）：

```powershell
$cacheDir = "$env:TEMP\ccNovaTerm-remote-config"
New-Item -ItemType Directory -Force $cacheDir | Out-Null

$wc = New-Object System.Net.WebClient
$files = @(".wezterm.lua", "config.nu", "env.nu", "starship.toml", "CLAUDE.local.md")
$docFiles = @("config-sync-workflow.md", "compatibility-constraints.md")
$remoteOk = $true
foreach ($f in $files) {
    $url = "$rawBase/$branch/config/$f"
    try {
        $bytes = $wc.DownloadData($url)
        [System.IO.File]::WriteAllBytes("$cacheDir\$f", $bytes)
    } catch {
        Write-Output "无法从远程获取 $f （$_）"
        $remoteOk = $false
    }
}
foreach ($f in $docFiles) {
    $url = "$rawBase/$branch/docs/$f"
    try {
        $bytes = $wc.DownloadData($url)
        New-Item -ItemType Directory -Force "$cacheDir\docs" | Out-Null
        [System.IO.File]::WriteAllBytes("$cacheDir\docs\$f", $bytes)
    } catch {
        Write-Output "无法从远程获取 docs/$f （$_）"
    }
}
$wc.Dispose()
```

- **全部获取成功**：设定 `$configDir = $cacheDir`，进入操作步骤。
- **部分或全部失败**：进入 0c。

### 0c. 远程获取失败时的处理

询问用户：

> 无法从远程仓库获取配置模板（网络不可达或仓库结构有变）。config-sync 以远程仓库为准，不自动 fallback 到本地项目。你可以：
> - 检查网络连接后重试
> - 手动提供一个包含 config/ 目录的路径作为模板源

设定 `$configDir` 后继续。详细信息见 `references/paths.md`。

## 文件映射

| 本地路径 | 项目模板 | 占位符 |
|---------|---------|--------|
| `~/.wezterm.lua` | `config/.wezterm.lua` | `__NU_PATH__` → nu.exe 完整路径 |
| `~\AppData\Roaming\nushell\config.nu` | `config/config.nu` | 无 |
| `~\AppData\Roaming\nushell\env.nu` | `config/env.nu` | `__GIT_USR_BIN__` → Git usr/bin 目录 |
| `~/.config/starship.toml` | `config/starship.toml` | 无 |
| `${PWD}/CLAUDE.local.md` | `config/CLAUDE.local.md` | 无（文件不存在则跳过） |
| `${PWD}/docs/config-sync-workflow.md` | `docs/config-sync-workflow.md` | 无（纯参考文档） |
| `${PWD}/docs/compatibility-constraints.md` | `docs/compatibility-constraints.md` | 无（纯参考文档） |

**占位符规则**：
- `__NU_PATH__` — Windows 用 nu.exe 完整路径（双反斜杠），macOS 用 `'nu'`
- `__GIT_USR_BIN__` — Git 安装目录下的 `usr\bin` 路径（双反斜杠）

## 双重排除机制

config-sync 有两层排除规则：
1. **内置保护**（自动生效）：`env.nu` 的 `load-env` 代理行始终保护，无需用户配置
2. **用户配置**（`~/.configsyncignore`）：可选，定义额外排除项（文件级或行/字段级）

在每次操作开始时合并两层规则。完整规则定义、解析逻辑和合并策略见 `references/exclusions.md`。

## 工作流程

根据用户意图选择对应方向。**先执行第零步，再读取对应方向的 reference 文件获取完整指令。**

| 用户意图 | 方向 | 详细指令 |
|---------|------|---------|
| 同步到项目 / push / 更新模板 | 方向 1: 本地 → 项目 | `references/sync-push.md` |
| 同步到本地 / pull / apply | 方向 2: 项目 → 本地 | `references/sync-pull.md` |
| 对比 / diff / 快速检查 / 兼容吗 | 方向 3: 对比（含 hash 预检） | `references/diff.md` |

**执行流程**：第零步（获取远程模板源） → 选择方向 → 读取对应方向 reference → 执行操作 → 验证

## 编码要求（关键！）

所有配置文件读写必须使用 UTF-8 无 BOM。PowerShell 5.1 的 `Get-Content`/`Set-Content` 默认 GBK 会损坏 Nerd Font PUA 字符（`` `` `󰈙` → `顐` `禲` `癩`）。

**必须使用**：
- 读取: `[System.IO.File]::ReadAllBytes()` + `[System.Text.Encoding]::UTF8.GetString()`
- 写入: `$utf8NoBom = New-Object System.Text.UTF8Encoding $false; [System.IO.File]::WriteAllText($path, $content, $utf8NoBom)`

**绝对禁止**：`Set-Content -Encoding UTF8`（BOM 破坏 Nushell alias 解析）、不带 `-Encoding UTF8` 的 `Get-Content`/`Set-Content`（默认 GBK）、`Invoke-WebRequest` 的 `.Content` 属性。**注意：`[System.Text.Encoding]::UTF8` 作为写入参数在 .NET Framework 中带有 BOM——必须用 `New-Object System.Text.UTF8Encoding $false`。**

详见 `references/encoding.md`，包含 starship.toml 编码损坏检测、远程获取安全方法、BOM 危害说明。

## 验证步骤

每次同步后执行这些检查：

1. **PowerShell 语法** — 用 `[System.Management.Automation.Language.Parser]::ParseFile()` 检查 `.wezterm.lua`（基本结构）
2. **TOML 格式** — 检查 `starship.toml` 含 schema reference
3. **文件大小** — 确认所有写入文件 > 10 字节
4. **Unicode 完整性** — 检查 `starship.toml` 是否含有预期的 Nerd Font 字符。如果文件中出现 `顐` `禲` `癩` 等 CJK 替代字符，说明编码已损坏
5. **文档完整性** — 检查 `docs/` 下的 `.md` 文件是否存在且 > 10 字节
6. **WezTerm 状态** — 运行 `wezterm cli list` 确认 WezTerm 在运行
6. **Lua 基本检查** — 检查 `.wezterm.lua` 有 `return config` 结尾

如果验证失败，不要继续写入——先修复问题。

## 开始工作前必须读取

**在选择方向之前**先读取以下基础文件：

1. `references/paths.md` — 本地路径、项目路径、备份路径、远程 URL 推导、缓存路径（含 CLAUDE.local.md 由 $PWD 确定的说明）
2. `references/placeholders.md` — 每个占位符的检测方法、替换规则、双反斜杠规则

**确定方向后**读取对应流程文件，同时读取排除规则：

3. `references/exclusions.md` — 排除规则（方向 3 轻量模式跳过用户规则，使用内联保护）
4. `references/sync-push.md` — 方向 1 完整流程
5. `references/sync-pull.md` — 方向 2 完整流程
6. `references/diff.md` — 方向 3 完整流程（含 hash 预检，合并原快速检查）

**遇到编码问题时**读取：

7. `references/encoding.md` — 编码安全细节、starship.toml 保护、远程获取安全

读完后再继续。路径解析失败是最高频的错误——严格按照 paths.md 的流程执行。
