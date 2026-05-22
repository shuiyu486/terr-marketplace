# marketplace-manager.md — terr-marketplace 维护手册

本文件是 `shuiyu486/terr-marketplace` 的详细维护规则。不要默认整篇读取；从 `CLAUDE.local.md` 的路由表进入对应 section。

---

## 仓库定位与工作目录

`terr-marketplace` 是 Claude Code 插件 marketplace 仓库。

本地仓库通常位于：

- Windows: `~\.claude\plugins\marketplaces\terr-marketplace`
- macOS/Linux: `~/.claude/plugins/marketplaces/terr-marketplace`

维护规则：

- 当前工作目录不一定是 marketplace 仓库。
- 修改 marketplace、插件、commands、skills、references 前，先确认实际仓库路径。
- 不要在管理入口目录 clone `terr-marketplace`，除非用户明确要求。
- 涉及 git commit、push、PR 时，必须在真正的 marketplace git 仓库内执行。

---

## 添加插件流程

适用场景：

- 新增 `plugins/<name>`。
- 将 skill 转成 marketplace plugin。
- 注册新插件到 `.claude-plugin/marketplace.json`。

流程：

```bash
# 1. 创建插件目录
plugins/<name>/

# 2. 创建插件元数据
plugins/<name>/.claude-plugin/plugin.json

# 3. 添加 skill / command / references / src 等内容
plugins/<name>/...

# 4. 注册 marketplace 条目
.claude-plugin/marketplace.json

# 5. 验证
claude plugin validate .
```

要求：

- `marketplace.json` 中的 `source.source` 必须是 `git-subdir`。
- `source.url` 使用远程仓库地址。
- `source.path` 指向 `plugins/<name>`。
- 不要使用相对路径 source，例如 `./plugins/<name>`。

新增插件后通常需要检查：

```bash
claude plugin validate .
git status
```

---

## 更新插件流程

适用场景：

- 修改已有插件功能。
- 修改 `src/`。
- 修改 `commands/`。
- 修改 `skills/`。
- 修改 `references/`。
- 修改用户可见行为。

流程：

```bash
# 1. 修改插件内容
plugins/<name>/...

# 2. 按语义化版本规则 bump version
# bugfix -> patch
# feature -> minor
# breaking change -> major

# 3. 同步所有 version 声明
# 4. 运行验证
claude plugin validate .
```

重要规则：

- 任何影响用户功能的变更都必须 bump version。
- 不 bump version 会导致已安装用户无法通过 update 识别更新。
- 文档、references、commands 如果影响用户使用，也视为用户功能变更。

---

## 版本同步规则

插件版本声明必须保持一致。

常见需要同步的文件：

```text
plugins/<name>/package.json
plugins/<name>/package-lock.json
plugins/<name>/.claude-plugin/plugin.json
.claude-plugin/marketplace.json
```

其中：

- `package.json`：Node 插件或有 npm 构建时存在。
- `package-lock.json`：如果存在，必须同步。
- `.claude-plugin/plugin.json`：插件自身元数据。
- 根 `.claude-plugin/marketplace.json`：marketplace 分发入口。

版本策略：

| 变更类型 | bump |
|---|---|
| bugfix | patch |
| 新功能 | minor |
| 破坏性变更 | major |
| 仅内部重构且不影响用户 | 通常不 bump |
| references / commands 改变用户使用方式 | 需要 bump |

检查建议：

```bash
claude plugin validate .
```

---

## marketplace.json 规则

文件：

```text
.claude-plugin/marketplace.json
```

每个插件条目必须使用 `git-subdir`：

```json
{
  "name": "<name>",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/shuiyu486/terr-marketplace.git",
    "path": "plugins/<name>"
  },
  "description": "<描述>",
  "version": "1.0.0",
  "author": { "name": "<作者>" },
  "license": "MIT",
  "keywords": ["<kw>"]
}
```

禁止：

```json
"source": "./plugins/<name>"
```

常见检查点：

- 新插件条目必须放在 `plugins` 数组内。
- 前一个条目后需要逗号。
- 最后一个条目后不能有逗号。
- `version` 要与插件元数据同步。
- `path` 必须指向真实插件目录。

---

## PowerShell 与 JSON 陷阱

Windows / PowerShell 下维护 JSON 时注意：

- 避免用 `ConvertTo-Json` 生成 `plugin.json` 或 `marketplace.json`。
- 避免裸 `Set-Content` / `Get-Content` 造成编码问题。
- 避免 `Set-Content -Encoding UTF8` 在旧 PowerShell 中写出 BOM。

推荐无 BOM UTF-8 写入方式：

```powershell
[System.IO.File]::WriteAllText($path, $content, (New-Object System.Text.UTF8Encoding $false))
```

JSON 建议：

- 小文件优先手写或用编辑工具精确修改。
- 修改后用 JSON parser 验证。
- 不要依赖 PowerShell 默认编码。

---

## validate 失败排查

验证命令：

```bash
claude plugin validate .
```

常见问题：

| 现象 | 可能原因 | 处理 |
|---|---|---|
| JSON parse error | 逗号、引号、尾逗号错误 | 检查对应 JSON |
| source invalid | 未使用 `git-subdir` | 改为 git-subdir 结构 |
| path not found | `source.path` 指错 | 确认 `plugins/<name>` 存在 |
| version mismatch | 多个 version 未同步 | 按版本同步规则检查 |
| metadata missing | plugin.json 字段不完整 | 补齐 name/version/description 等 |

单独测试 JSON 可使用：

```powershell
Get-Content <file> -Raw | ConvertFrom-Json
```

如果怀疑编码问题，重写为无 BOM UTF-8。

---

## 发布前检查清单

提交或发布前检查：

```bash
claude plugin validate .
git status
```

检查项：

- `.claude-plugin/marketplace.json` 已更新。
- 插件目录下 `.claude-plugin/plugin.json` 已更新。
- 如存在 `package.json` / `package-lock.json`，version 已同步。
- 用户可见变更已 bump version。
- 没有把本机路径、临时文件、私有配置写进远程文件。
- 没有把插件级历史 bug 塞进根入口文件。
- PowerShell 写出的 JSON 没有 BOM / 转义异常。

提交信息建议：

```text
Add <plugin-name> plugin v<x.y.z>
Update <plugin-name> to v<x.y.z>
Fix <plugin-name> <short issue>
```
