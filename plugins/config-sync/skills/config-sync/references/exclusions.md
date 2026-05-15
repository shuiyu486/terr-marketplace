# 双重排除机制：内置保护 + 用户配置（`~/.configsyncignore`）

config-sync 有两层排除规则。**内置规则自动生效，无需用户配置**；`.configsyncignore` 让用户按需扩展额外排除项。

## 第一层：内置保护规则（自动生效，无需配置）

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

## 第二层：用户排除规则（`~/.configsyncignore`）

在内置规则基础上，用户可定义**额外**排除项——如跳过整个文件、保护自定义字段。

### 文件格式

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

### 规则行为矩阵

| 规则类型 | 方向 1（→项目） | 方向 2（→本地） | 方向 3（对比） |
|---------|----------------|----------------|---------------|
| 文件级 `文件名` | 跳过，不包含在 commit 中 | 跳过，保留本地文件原样 | 标注"⏭️ 已排除" |
| 字段级 `文件名::关键字` | 该行保留原样推送 | 保留本地版本的行 | 该行不标差异 |
| 无规则 | 正常同步 | 正常同步 | 正常对比 |

## 合并解析（内置 + 用户）

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

## isExcludedFile / isExcludedLine 判断

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
