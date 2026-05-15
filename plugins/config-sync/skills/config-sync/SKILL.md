---
name: config-sync
description: |
  Two-way sync and comparison of terminal config files between local environment and
  ccNovaTerm project. Can fetch templates directly from remote git repository when local
  project is not available. Auto-protects local proxy settings (env.nu load-env) without
  configuration; supports ~/.configsyncignore for custom exclusions. Use this whenever the
  user wants to sync, compare, diff, or check config changes between their local machine
  and the ccNovaTerm repo templates — even if they don't say "sync" explicitly. Trigger phrases:
  - "同步到项目" / "sync to project" / "push configs to ccNovaTerm"
  - "同步到本地" / "sync to local" / "pull configs from ccNovaTerm"
  - "对比" / "compare" / "diff" / "check differences" / "有什么不同" / "看看区别"
  - "更新项目模板" / "update project templates"
  - "apply config from project"
  - "快速检查" / "quick check" / "兼容吗" / "兼容性检查" / "check compatibility" — lightweight hash-based check using local clone only
  Use proactively when users ask about config differences between their local environment
  and ccNovaTerm, or mention WezTerm / Nushell / Starship / Claude Code configs in the
  context of the project — comparison is as important as syncing. After editing any managed
  config file, suggest a quick check to verify compatibility.
compatibility: Windows (PowerShell 5.1+), supports local project and remote GitHub fetch
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

## 第零步：获取配置模板源（所有操作之前强制执行！）

**这是最容易出错的步骤——跳过会导致盲目假设。** 所有操作都优先远程获取，**完全不需要用户手动克隆项目**。本地 clone 和临时 clone 都是自动处理的实现细节。

### 0a. 确定操作类型并获取远程仓库 URL

| 操作 | 触发词 | 最终需要 push？ |
|------|--------|---------------|
| 对比差异 | "对比"、"diff"、"compare"、"有什么不同" | 否 |
| 项目→本地 | "同步到本地"、"pull"、"apply" | 否 |
| 本地→项目 | "同步到项目"、"push"、"更新模板" | 是（通过临时 clone） |
| 快速检查 | "快速检查"、"兼容吗"、"兼容性检查"、"quick check"、"check compatibility" | 否 |

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

### 0b. 尝试本地项目（优先——所有操作类型都支持）

```powershell
$repoRoot = $null
$candidates = @($PWD.Path, "$env:USERPROFILE\ccNovaTerm")
foreach ($c in $candidates) {
    if (Test-Path "$c\config\.wezterm.lua") { $repoRoot = $c; break }
}
```

如果找到本地项目：设定 `$configDir = "$repoRoot\config"`。对于"本地→项目"操作，可以直接在本地项目上 commit/push（不需要临时 clone）。

### 0c. 远程获取（本地项目不存在时的默认路径）

**除快速检查外所有操作类型都适用。** 从 GitHub raw 获取模板文件作为基准。

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

**逐个获取 7 个模板文件**，使用 `WebClient.DownloadData` 获取原始字节（避免 PowerShell 的文本编码干扰）：

```powershell
$cacheDir = "$env:TEMP\ccNovaTerm-remote-config"
New-Item -ItemType Directory -Force $cacheDir | Out-Null

$wc = New-Object System.Net.WebClient
$files = @(".wezterm.lua", "config.nu", "env.nu", "starship.toml", "statusline.ps1", "settings.json", "CLAUDE.local.md")
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
$wc.Dispose()
```

- **全部获取成功**：设定 `$configDir = $cacheDir`，进入操作步骤。
- **部分或全部失败**：进入 0d。

### 0d. 远程获取失败时的处理

询问用户：

> 无法从远程仓库获取配置模板（网络不可达或仓库结构有变）。你可以：
> - 手动克隆仓库：`git clone $repoUrl ~/ccNovaTerm`
> - 或提供已有 ccNovaTerm 项目的本地路径

设定 `$configDir` 后继续。详细信息见 `references/paths.md`。

## 文件映射

| 本地路径 | 项目模板 | 占位符 |
|---------|---------|--------|
| `~/.wezterm.lua` | `config/.wezterm.lua` | `__NU_PATH__` → nu.exe 完整路径 |
| `~\AppData\Roaming\nushell\config.nu` | `config/config.nu` | 无 |
| `~\AppData\Roaming\nushell\env.nu` | `config/env.nu` | `__GIT_USR_BIN__` → Git usr/bin 目录 |
| `~/.config/starship.toml` | `config/starship.toml` | 无 |
| `~/.claude/statusline.ps1` | `config/statusline.ps1` | 无 |
| `~/.claude/settings.json` | `config/settings.json` | `__USERNAME__` → 当前用户名（仅 statusLine 字段） |
| `<项目根>/CLAUDE.local.md` | `config/CLAUDE.local.md` | 无 |

**占位符规则**：
- `__NU_PATH__` — Windows 用 nu.exe 完整路径（双反斜杠），macOS 用 `'nu'`
- `__GIT_USR_BIN__` — Git 安装目录下的 `usr\bin` 路径（双反斜杠）
- `__USERNAME__` — Windows 用户名，出现在 `settings.json` 的 statusLine command 路径中

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
| 对比 / diff / 有什么不同 | 方向 3: 完整对比 | `references/diff.md` |
| 快速检查 / 兼容吗 / 兼容性检查 | 方向 4: 快速检查（轻量，无远程获取） | `references/quick-check.md` |

**执行流程**：第零步（获取模板源） → 选择方向 → 读取对应方向 reference。方向 1-3 额外读取 `references/exclusions.md`（排除规则）；方向 4 使用内联保护规则（不读 exclusions.md）。→ 执行操作 → 验证

## 编码要求（关键！）

所有配置文件读写必须使用 UTF-8 无 BOM。PowerShell 5.1 的 `Get-Content`/`Set-Content` 默认 GBK 会损坏 Nerd Font PUA 字符（`` `` `󰈙` → `顐` `禲` `癩`）。

**必须使用**：
- 读取: `[System.IO.File]::ReadAllBytes()` + `[System.Text.Encoding]::UTF8.GetString()`
- 写入: `[System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)`

**绝对禁止**：`Set-Content -Encoding UTF8`（BOM 破坏 Nushell alias 解析）、不带 `-Encoding UTF8` 的 `Get-Content`/`Set-Content`（默认 GBK）、`Invoke-WebRequest` 的 `.Content` 属性。

详见 `references/encoding.md`，包含 starship.toml 编码损坏检测、远程获取安全方法、BOM 危害说明。

## 验证步骤

每次同步后执行这些检查：

1. **PowerShell 语法** — 用 `[System.Management.Automation.Language.Parser]::ParseFile()` 检查 `statusline.ps1`
2. **JSON 语法** — 用 `ConvertFrom-Json` 检查 `settings.json`
3. **文件大小** — 确认所有写入文件 > 10 字节
4. **Unicode 完整性** — 检查 `starship.toml` 是否含有预期的 Nerd Font 字符。如果文件中出现 `顐` `禲` `癩` 等 CJK 替代字符，说明编码已损坏
5. **WezTerm 状态** — 运行 `wezterm cli list` 确认 WezTerm 在运行
6. **Lua 基本检查** — 检查 `.wezterm.lua` 有 `return config` 结尾

如果验证失败，不要继续写入——先修复问题。

## 开始工作前必须读取

**在选择方向之前**先读取以下基础文件：

1. `references/paths.md` — 本地路径、项目路径、备份路径、远程 URL 推导、缓存路径（含 CLAUDE.local.md 项目根路径说明）
2. `references/placeholders.md` — 每个占位符的检测方法、替换规则、双反斜杠规则

**确定方向后**读取对应流程文件，方向 1-3 同时读取排除规则：

3. `references/exclusions.md` — 排除规则（方向 1-3 需要；方向 4 跳过，使用内联保护）
4. `references/sync-push.md` — 方向 1 完整流程
5. `references/sync-pull.md` — 方向 2 完整流程（含 settings.json 合并代码）
6. `references/diff.md` — 方向 3 完整流程
7. `references/quick-check.md` — 方向 4 完整流程（含 git 新鲜度检测）

**遇到编码问题时**读取：

8. `references/encoding.md` — 编码安全细节、starship.toml 保护、远程获取安全

读完后再继续。路径解析失败是最高频的错误——严格按照 paths.md 的流程执行。
