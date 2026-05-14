---
name: config-sync
description: |
  Two-way sync of terminal config files between local environment and ccNovaTerm project.
  Use this when the user wants to sync config changes between their local machine and the
  ccNovaTerm repo templates. Trigger phrases:
  - "同步到项目" / "sync to project" / "push configs to ccNovaTerm"
  - "同步到本地" / "sync to local" / "pull configs from ccNovaTerm"
  - "更新项目模板" / "update project templates"
  - "apply config from project"
  Also use when the user mentions syncing WezTerm, Nushell, Starship, or Claude Code
  config between their environment and the ccNovaTerm repository.
compatibility: Windows only (PowerShell 5.1+), requires ccNovaTerm project in working directory
---

# Config Sync — 终端配置双向同步

在本地环境（`~/`）和 ccNovaTerm 项目（`config/`）之间同步配置文件。两方向都支持，总是先备份后写入。

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

## 工作流程

### 方向 1：本地 → 项目（local → ccNovaTerm）

用户说"同步到项目"时触发。将本地环境的配置更新推送到 ccNovaTerm 项目模板。

1. **读取本地文件** — 从用户目录读取 6 个配置文件的实际内容
2. **检测用户特定值** — 自动识别当前环境的：
   - nu.exe 路径（检查 `Get-Command nu.exe`、`~\AppData\Local\Programs\nu\bin\nu.exe`、`${env:ProgramFiles}\nu\bin\nu.exe`）
   - Git usr/bin 路径（从 `git.exe` 位置推断，或检查 `C:\Program Files\Git\usr\bin`）
   - 用户名（`$env:USERNAME`）
   - 代理端口（`env.nu` 中的 `load-env` 行）
3. **生成模板** — 将用户特定值替换为占位符：
   - nu.exe 完整路径 → `__NU_PATH__`
   - Git usr/bin 路径 → `__GIT_USR_BIN__`
   - 用户名 → `__USERNAME__`
   - `load-env { http_proxy: ... }` → 注释掉 `# load-env { http_proxy: "http://127.0.0.1:7890", https_proxy: "http://127.0.0.1:7890" }`
   - `.wezterm.lua` 中 `config.default_prog` 改为带 OS 检测的占位符形式（如模板已有则保持）
4. **写入项目** — 写入 `ccNovaTerm/config/` 目录，覆盖现有模板。**必须使用 UTF-8 编码写入**（`Set-Content -Encoding UTF8` 或 `.NET UTF8`），绝对不能用系统默认编码
5. **额外注意** — `settings.json` 只取 `statusLine` 字段，不写入完整配置（避免泄露 API key）
6. **提示文档更新** — 如果改动涉及新功能或修复，提醒用户是否需要更新 `README.md`、`README_CN.md`、`project-lifecycle.md`

### 方向 2：项目 → 本地（ccNovaTerm → local）

用户说"同步到本地"时触发。将 ccNovaTerm 模板应用到本地环境。

1. **读取项目模板** — 从 `ccNovaTerm/config/` 读取 6 个模板文件
2. **检测系统值** — 自动查找当前系统对应的实际路径：
   - nu.exe 完整路径（按优先级查找）
   - Git usr/bin 路径
   - 当前用户名
3. **备份本地配置** — 将现有配置文件备份到 `~\ccNovaTerm-backup\yyyyMMdd_HHmmss\`
4. **替换占位符** — 将模板中的占位符替换为实际值
5. **settings.json 合并** — 只添加/更新 `statusLine` 字段，保留用户已有的 API key、模型设置、权限等
6. **写入本地** — 写入本地配置路径，自动创建所需目录。**必须使用 UTF-8 编码**，`starship.toml` 尤其敏感
7. **运行验证** — 执行语法、Unicode 完整性和文件大小检查
8. **报告结果** — 列出写入的文件、备份位置、下一步操作（重启 WezTerm 等）

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

## 实现参考

读取参考文件了解完整细节：
- `references/paths.md` — 所有本地和项目路径的详细说明
- `references/placeholders.md` — 占位符替换规则的完整参考

同步逻辑应直接嵌入主流程。不依赖外部脚本——用 PowerShell 内联实现所有检测和替换。
