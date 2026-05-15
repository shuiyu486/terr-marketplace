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
  Use proactively when users ask about config differences between their local environment
  and ccNovaTerm, or mention WezTerm / Nushell / Starship / Claude Code configs in the
  context of the project — comparison is as important as syncing.
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

**这是最容易出错的步骤——跳过会导致盲目假设。** 所有三种操作（对比、项目→本地、本地→项目）都优先远程获取，**完全不需要用户手动克隆项目**。本地 clone 和临时 clone 都是自动处理的实现细节。

### 0a. 确定操作类型并获取远程仓库 URL

首先判断用户意图，并从插件元数据中读取远程仓库 URL：

| 操作 | 触发词 | 最终需要 push？ |
|------|--------|---------------|
| 对比差异 | "对比"、"diff"、"compare"、"有什么不同" | 否 |
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

**所有三种操作类型都适用。** 从 GitHub raw 获取模板文件作为基准。

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

**逐个获取 6 个模板文件**，使用 `WebClient.DownloadData` 获取原始字节（避免 PowerShell 的文本编码干扰）：

```powershell
$cacheDir = "$env:TEMP\ccNovaTerm-remote-config"
New-Item -ItemType Directory -Force $cacheDir | Out-Null

$wc = New-Object System.Net.WebClient
$files = @(".wezterm.lua", "config.nu", "env.nu", "starship.toml", "statusline.ps1", "settings.json")
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

**占位符规则**：
- `__NU_PATH__` — Windows 用 nu.exe 完整路径（双反斜杠），macOS 用 `'nu'`
- `__GIT_USR_BIN__` — Git 安装目录下的 `usr\bin` 路径（双反斜杠）
- `__USERNAME__` — Windows 用户名，出现在 `settings.json` 的 statusLine command 路径中

## 双重排除机制：内置保护 + 用户配置（`~/.configsyncignore`）

config-sync 有两层排除规则。**内置规则自动生效，无需用户配置**；`.configsyncignore` 让用户按需扩展额外排除项。

### 第一层：内置保护规则（自动生效，无需配置）

以下规则硬编码在技能中，对所有用户无条件启用：

| 文件 | 匹配模式 | 保护内容 |
|------|---------|---------|
| `env.nu` | 包含 `load-env` 的行 | 代理服务器地址（`127.0.0.1:7890` 等） |

**为什么内置？** 代理设置是典型的"个人环境配置"——每个人的代理地址和端口不同，不应进入共享模板。这不是可选项，每个用户都需要这个保护。用户无需写任何配置文件即可获得此保护。

**内置规则在三个方向中的行为**：

| 方向 | 行为 |
|------|------|
| 方向 1（本地→项目） | 模板化时，`load-env { http_proxy: ... }` → 注释为 `# load-env { http_proxy: ... }` |
| 方向 2（项目→本地） | 模板中注释的 `# load-env` 行**不覆盖**本地已激活的 `load-env` 行（保留本地版本） |
| 方向 3（对比差异） | 模板 `# load-env { ... }` 与本地 `load-env { ... }` 视为一致，不标差异 |

### 第二层：用户排除规则（`~/.configsyncignore`）

在内置规则基础上，用户可定义**额外**排除项——如跳过整个文件、保护自定义字段。

#### 文件格式

每行一条规则，`#` 开头为注释。**注意：env.nu 的代理行已由内置规则自动保护，无需在此重复配置。**

```
# === 文件级排除：跳过整个文件 ===
# 方向 1（→项目）：不读取、不推送该文件
# 方向 2（→本地）：不覆盖该本地文件
# 方向 3（对比）：标注"已排除"，不比较内容
# env.nu         ← 如需排除整个 env.nu（而非仅代理行），取消此行注释

# === 行/字段级排除：只跳过含指定关键字的行 ===
# 格式：文件名::关键字
# 方向 1（→项目）：模板化时保留原样
# 方向 2（→本地）：保留本地版本的行
# 方向 3（对比）：匹配行不标差异
# starship.toml::time_format   ← 示例：保护自定义时间格式
```

#### 规则行为矩阵

| 规则类型 | 方向 1（→项目） | 方向 2（→本地） | 方向 3（对比） |
|---------|----------------|----------------|---------------|
| 文件级 `文件名` | 跳过，不包含在 commit 中 | 跳过，保留本地文件原样 | 标注"⏭️ 已排除" |
| 字段级 `文件名::关键字` | 该行保留原样推送 | 保留本地版本的行 | 该行不标差异 |
| 无规则 | 正常同步 | 正常同步 | 正常对比 |

### 合并解析（内置 + 用户）

在每次操作开始时（第零步之后），先加载内置规则，再合并用户规则。内置规则和用户规则中的 `*` 哨兵（全文件排除）会覆盖该文件的行级规则：

```powershell
# === 内置保护规则（硬编码，所有用户自动生效） ===
$builtinRules = @{
    "env.nu" = @("load-env")  # 代理行保护：匹配含 load-env 的行
}

# === 读取用户规则（~/.configsyncignore） ===
$userRules = @{}
$ignoreFile = "$env:USERPROFILE\.configsyncignore"
if (Test-Path $ignoreFile) {
    $lines = [System.Text.Encoding]::UTF8.GetString([System.IO.File]::ReadAllBytes($ignoreFile)) -split "`n"
    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        if (-not $trimmed -or $trimmed.StartsWith('#')) { continue }
        if ($trimmed -match '^(.+?)::(.+)$') {
            $fname = $Matches[1].Trim()
            $pattern = $Matches[2].Trim()
            if (-not $userRules.ContainsKey($fname)) { $userRules[$fname] = @() }
            if ($userRules[$fname][0] -ne "*") { $userRules[$fname] += $pattern }
        } else {
            $userRules[$trimmed] = @("*")  # * 哨兵 = 全文件排除
        }
    }
}

# === 合并：内置规则优先，用户规则追加 ===
$excludeRules = @{}
# 先加载内置规则
foreach ($key in $builtinRules.Keys) {
    $excludeRules[$key] = [System.Collections.ArrayList]::new()
    foreach ($v in $builtinRules[$key]) { [void]$excludeRules[$key].Add($v) }
}
# 再合并用户规则
foreach ($key in $userRules.Keys) {
    if ($userRules[$key][0] -eq "*") {
        # 用户文件级排除覆盖所有（包括内置行级规则）
        $excludeRules[$key] = @("*")
    } elseif ($excludeRules.ContainsKey($key) -and $excludeRules[$key][0] -ne "*") {
        # 追加行级模式（去重）
        foreach ($p in $userRules[$key]) {
            if ($p -notin $excludeRules[$key]) { $excludeRules[$key] += $p }
        }
    } else {
        $excludeRules[$key] = $userRules[$key]
    }
}
# 示例结果（无用户配置时）：
# $excludeRules = @{ "env.nu" = @("load-env") }
# 示例结果（用户添加了文件级排除 starship.toml 时）：
# $excludeRules = @{ "env.nu" = @("load-env"); "starship.toml" = @("*") }
```

### isExcludedFile / isExcludedLine 判断

后续各方向中通过以下逻辑判断（同时覆盖内置和用户规则）：

```powershell
# 是否全文件排除？
function Test-FileExcluded([string]$Filename) {
    return ($excludeRules.ContainsKey($Filename) -and $excludeRules[$Filename][0] -eq "*")
}

# 某行是否匹配排除规则（含内置和用户规则）？
function Test-LineExcluded([string]$Filename, [string]$LineContent) {
    if (-not $excludeRules.ContainsKey($Filename)) { return $false }
    $patterns = $excludeRules[$Filename]
    foreach ($p in $patterns) {
        if ($LineContent.Contains($p)) { return $true }
    }
    return $false
}
```

无 `~/.configsyncignore` 时仅内置规则生效——代理保护始终在线，向后兼容。

## 工作流程

### 方向 1：本地 → 项目（local → ccNovaTerm）

用户说"同步到项目"、"push"、"更新模板"时触发。将本地配置变更推送到 ccNovaTerm 仓库。

**完全无需用户手动克隆项目。** 如果本地没有 clone，自动在临时目录 clone、提交、推送后清理。

#### 第一步：准备模板化的本地配置

1. **读取排除规则** — 解析 `~/.configsyncignore`（如存在），构建 `$excludeRules`
2. **读取本地文件** — 用 UTF-8 编码读取配置文件。**跳过文件级排除的文件**（`Test-FileExcluded` 返回 `$true` 的文件不参与后续步骤）
3. **检测系统特定值** — 自动识别：
   - nu.exe 路径（`Get-Command nu.exe` → `~\AppData\Local\Programs\nu\bin\nu.exe` → `${env:ProgramFiles}\nu\bin\nu.exe`）
   - Git usr/bin 路径（从 `git.exe` 推断 → `C:\Program Files\Git\usr\bin`）
   - 用户名（`$env:USERNAME`）
3. **生成模板** — 将系统值替换为占位符：
   - nu.exe 完整路径 → `__NU_PATH__`
   - Git usr/bin 路径 → `__GIT_USR_BIN__`
   - 用户名 → `__USERNAME__`
   - `load-env { http_proxy: ... }` → 注释掉（如 `# load-env { http_proxy: "http://127.0.0.1:7890", https_proxy: "http://127.0.0.1:7890" }`）
   - `settings.json`：只取 `statusLine` 字段，不包含 API key 等敏感信息
   - `.wezterm.lua`：`config.default_prog` 用操作系统检测包裹（如模板已有则保持）

#### 第二步：展示差异并确认

1. **获取远程基准** — 如第零步 0b 无本地项目，执行 0c 远程获取模板到缓存
2. **对比差异** — 将模板化后的本地内容与远程基准逐文件对比（settings.json 只比较 statusLine 字段）。**不包含文件级排除的文件**
3. **无变更则终止** — 如果所有文件与远程一致，告知用户"本地配置与项目模板完全一致，无需推送"，不执行任何写入操作
4. **展示变更清单** — 列出哪些文件有变更、变更内容概要。**单独列出被排除规则跳过的文件**
5. **请求确认** — 向用户展示变更摘要并询问是否继续推送。**必须获得用户明确同意才能执行推送**（涉及远程仓库写入）

#### 第三步：推送变更

推送前检查 git 是否可用：

```powershell
$gitOk = $true
try { $null = Get-Command git.exe -ErrorAction Stop } catch {
    Write-Output "未检测到 git。请安装 Git for Windows 后再执行同步到项目。"
    $gitOk = $false
}
```

根据第零步结果选择路径：

**路径 A：本地项目存在（0b 成功）**

直接在本地项目上操作：

```powershell
# 1. 写入模板化后的文件到 $configDir（UTF-8 无 BOM）
foreach ($f in $changedFiles) {
    [System.IO.File]::WriteAllText("$configDir\$f", $templatedContent, [System.Text.Encoding]::UTF8)
}

# 2. 提交并推送
git -C $repoRoot add config/
git -C $repoRoot commit -m "<生成的提交信息>"
git -C $repoRoot push
```

**路径 B：无本地项目（通过临时 clone）**

```powershell
$tmpDir = "$env:TEMP\ccNovaTerm-push-$((Get-Date -Format 'yyyyMMddHHmmss'))"

# 1. 浅克隆（节省时间，只取最新提交）
git clone --depth 1 $repoUrl $tmpDir

# 2. 写入模板化后的文件（UTF-8 无 BOM）
foreach ($f in $changedFiles) {
    [System.IO.File]::WriteAllText("$tmpDir\config\$f", $templatedContent, [System.Text.Encoding]::UTF8)
}

# 3. 提交
git -C $tmpDir add config/
git -C $tmpDir commit -m "<生成的提交信息>"

# 4. 推送（需用户已配置 git 凭据）
git -C $tmpDir push

# 5. 清理临时目录
Remove-Item -Recurse -Force $tmpDir
```

**提交信息格式** — 简洁描述变更内容：
```
sync: update <文件1>, <文件2> from local environment

- .wezterm.lua: update default_prog path
- starship.toml: adjust <具体变更>
```

**git push 失败处理** — 如果 push 失败（凭据未配置、无权限等）：
- 临时目录保留不删除，告知用户路径
- 提示用户可以手动进入目录执行 `git push`
- 或提供 `gh auth login` / SSH key 配置指引

#### 第四步：报告结果

- 列出成功推送的文件
- 列出被排除规则跳过的文件
- 临时 clone 是否已清理（路径 B）
- 如果是本地项目，提醒可能需要更新 README 等文档

### 方向 2：项目 → 本地（ccNovaTerm → local）

用户说"同步到本地"时触发。将 ccNovaTerm 模板应用到本地环境。**本地 clone 或远程获取均可。**

1. **读取排除规则** — 解析 `~/.configsyncignore`（如存在），构建 `$excludeRules`
2. **读取项目模板** — 从 `$configDir`（本地项目或远程缓存）读取模板文件。**跳过文件级排除的文件**
3. **检测系统值** — 自动查找当前系统对应的实际路径：
   - nu.exe 完整路径（按优先级查找）
   - Git usr/bin 路径
   - 当前用户名
4. **备份本地配置** — 将现有配置文件备份到 `~\ccNovaTerm-backup\yyyyMMdd_HHmmss\`
5. **替换占位符** — 将模板中的占位符替换为实际值。**内置保护规则**：env.nu 代理行自动保留本地版本。**用户排除规则**：对于字段级排除，替换占位符后从备份中恢复被排除的行
6. **settings.json 合并** — 只添加/更新 `statusLine` 字段，保留用户已有的 API key、模型设置、权限等
7. **写入本地** — 写入本地配置路径，自动创建所需目录。**必须使用 UTF-8 编码**，`starship.toml` 尤其敏感。**跳过文件级排除的文件**（不覆盖）
8. **运行验证** — 执行语法、Unicode 完整性和文件大小检查
9. **报告结果** — 列出写入的文件、跳过的文件（含排除原因）、备份位置、下一步操作（重启 WezTerm 等）。如果模板来自远程缓存，注明来源

**字段级排除的行级合并**：当某文件有字段级排除规则时，在写入模板内容前：
```powershell
# 对于有字段级排除的文件，逐行处理
if ($excludeRules.ContainsKey($fname) -and $excludeRules[$fname][0] -ne "*") {
    $tplLines = $templatedContent -split "`n"
    $localLines = $localContent -split "`n"
    $mergedLines = @()
    for ($i = 0; $i -lt $tplLines.Count; $i++) {
        $excluded = $false
        foreach ($pattern in $excludeRules[$fname]) {
            if ($tplLines[$i].Contains($pattern)) { $excluded = $true; break }
        }
        if ($excluded -and $i -lt $localLines.Count) {
            $mergedLines += $localLines[$i]  # 保留本地行
        } else {
            $mergedLines += $tplLines[$i]     # 使用模板行
        }
    }
    $templatedContent = $mergedLines -join "`n"
}
```

### 方向 3：对比差异（Compare / Diff）

用户说"对比"、"看看有什么不同"、"check differences"时触发。只读不写，报告本地和项目模板之间的差异。**本地 clone 或远程获取均可。**

1. **获取模板源** — 执行第零步的完整流程（0a → 0b → 0c 或 0d）
2. **读取排除规则** — 解析 `~/.configsyncignore`（如存在），构建 `$excludeRules`
3. **成对读取** — 对 6 个文件，同时读取本地版本和模板版本（均用 UTF-8 编码）。**跳过文件级排除的文件**。**settings.json 特殊处理**：本地只提取 `statusLine` 字段参与对比，忽略 `env`、`permissions`、`model` 等包含敏感信息的字段（避免 API key 泄露到 diff 输出）。如果模板只有 `statusLine` 而本地有其他字段，标注"本地有额外设置"即可，不输出具体值。
4. **占位符感知对比** — 比较时将模板中的占位符替换为当前系统实际值后再 diff，这样差异反映的是真实的配置变化，而非路径不同：
   - `__NU_PATH__` → 当前系统 nu.exe 路径
   - `__GIT_USR_BIN__` → 当前系统 Git usr/bin 路径
   - `__USERNAME__` → 当前用户名
   - **内置保护规则**：`# load-env { http_proxy: ... }` 视为与本地 `load-env` 行一致（不标差异）
   - **用户排除规则**：对于匹配用户排除关键字的行，视为一致（不标差异）
   - 对于 `settings.json`：本地和模板都只取 `statusLine` 字段对比，其余字段只报告"存在差异"但不输出内容
5. **输出差异报告** — 对每个文件报告：
   - ✅ 一致：内容相同（占位符展开后）
   - ⚠️ 仅本地有不同：列出差异行
   - ❌ 模板不存在：文件仅在本地
   - ➖ 本地不存在：文件仅在模板中
   - ⏭️ 已排除：文件在 `.configsyncignore` 中，不比较
6. **总结建议** — 如果所有文件一致，告知用户。如果有差异，建议同步方向（本地→项目 还是 项目→本地），让用户决定。如果模板来自远程缓存，注明来源。**说明排除规则影响的文件数**

## 编码要求（关键！）

**所有配置文件的读写必须使用 UTF-8 编码，读取和写入都要显式指定。** 在中文 Windows 上，PowerShell 5.1 的 `Get-Content` 和 `Set-Content` 默认使用 GBK 编码。用 GBK 读取 UTF-8 文件会将 Nerd Font PUA 字符（3 字节 UTF-8）错误解释为 CJK 字符，之后再写入时永久损坏。

`starship.toml` 包含 Nerd Font 私有区（PUA）Unicode 字符（如 `` U+E0B6、`` U+E0B0、`󰈙` U+F0219 等）。这些字符在 GBK 编码下无对应映射，会被拆成 2-3 个 CJK 字符（`顐` `禲` `癩` 等）。

**必须使用以下 API（避开 PowerShell 默认编码陷阱）：**

读取文件：
```powershell
# 方法 1（推荐）— .NET UTF8，无 BOM 问题
$bytes = [System.IO.File]::ReadAllBytes($path)
$content = [System.Text.Encoding]::UTF8.GetString($bytes)

# 方法 2 — PowerShell，但必须显式指定 UTF8
$content = Get-Content $path -Raw -Encoding UTF8
```

写入文件：
```powershell
# 唯一推荐方法 — .NET UTF8，不写 BOM（关键！）
[System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)

# 定义 helper 以便复用：
function Write-FileUtf8NoBom([string]$Path, [string]$Content) {
    $dir = Split-Path -Parent $Path
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force $dir | Out-Null }
    [System.IO.File]::WriteAllText($Path, $Content, [System.Text.Encoding]::UTF8)
}
```

**绝对禁止 `Set-Content -Encoding UTF8`** —— PS5.1 会在文件头添加 BOM（字节 EF BB BF）。`config.nu` 开头的 BOM 字符 `﻿` 会被拼接到第一个语句前，导致 Nushell 静默跳过整个文件的 alias 解析（`scope aliases` 返回空列表，`cc` 别名失效）。`starship.toml` 的 BOM 虽不致命但也不规范。

**禁止使用**：任何不带 `-Encoding UTF8` 的 `Get-Content` / `Set-Content`（默认 GBK）、`Out-File`、`>` 重定向（默认 UTF-16 LE 或 GBK）、`Set-Content -Encoding UTF8`（BOM 隐患）。

**远程获取的特殊注意**：`Invoke-WebRequest` 返回的 `.Content` 属性已经过 PowerShell 的文本解码，可能引入编码问题。用 `.RawContentStream` 或直接使用 `[System.Net.WebClient]` 获取原始字节更安全：

```powershell
$wc = New-Object System.Net.WebClient
$bytes = $wc.DownloadData($url)
[System.IO.File]::WriteAllBytes("$cacheDir\$f", $bytes)
```

**Starship.toml 特殊保护**：同步前后用以下方法快速检查：
```powershell
$t = [System.Text.Encoding]::UTF8.GetString([System.IO.File]::ReadAllBytes($path))
if ($t.Contains('顐') -or $t.Contains('禲') -or $t.Contains('癩')) {
    # 编码已损坏！从备份恢复并用 .NET UTF8 重写
}
```

## 验证步骤

每次同步后执行这些检查：

1. **PowerShell 语法** — 用 `[System.Management.Automation.Language.Parser]::ParseFile()` 检查 `statusline.ps1`
2. **JSON 语法** — 用 `ConvertFrom-Json` 检查 `settings.json`
3. **文件大小** — 确认所有写入文件 > 10 字节
4. **Unicode 完整性** — 检查 `starship.toml` 是否含有预期的 Nerd Font 字符（如 `` ``）。如果文件中出现 `顐` `禲` `癩` 等 CJK 替代字符，说明编码已损坏
5. **WezTerm 状态** — 运行 `wezterm cli list` 确认 WezTerm 在运行
6. **Lua 基本检查** — 不要求独立 lua 解释器，但检查 `.wezterm.lua` 有 `return config` 结尾

如果验证失败，不要继续写入——先修复问题。

## 开始工作前必须读取

**在处理任何同步或对比请求之前，先读取以下两个参考文件。** 它们包含的细节不能靠记忆猜测：

1. `references/paths.md` — 本地路径、项目路径、备份路径、远程 URL 推导、缓存路径的完整说明
2. `references/placeholders.md` — 每个占位符的检测方法、替换规则、特殊处理（如代理注释、跨平台 default_prog）

读完后再继续。路径解析失败是最高频的错误——严格按照 paths.md 的流程执行。

同步和对比逻辑应直接嵌入主流程。不依赖外部脚本——用 PowerShell 内联实现所有检测和替换。
