# CLAUDE.local.md — terr-marketplace

Claude Code 插件集合，通过 `git-subdir` 格式从 GitHub 分发。仓库：`shuiyu486/terr-marketplace`。

## 关键约束

- **marketplace.json 中所有 source 必须用 `git-subdir`**，不能写相对路径 `./plugins/xxx`
- **修改 plugin 版本时**，三文件 version 必须同步：`package.json` + `plugin.json` + `marketplace.json`
- **任何影响用户功能的变更**（src/、commands/、references/）都必须 bump 版本号，否则 `cc-statusline:update` 无法识别更新
- **每次修改 marketplace.json 后**必须跑 `claude plugin validate .`
- **skill-creator 的输出**通过 skills2ccPlugin 转换为 marketplace 插件后发布

## PowerShell 陷阱

- 写文件用 `[System.IO.File]::WriteAllText($p, $c, (New-Object System.Text.UTF8Encoding $false))`
- **禁止** `Set-Content -Encoding UTF8`（带 BOM）和裸 `Set-Content`/`Get-Content`（默认 GBK）
- **禁止** 用 `ConvertTo-Json` 生成 plugin.json（撇号转义、Depth 截断）

## 添加插件

```shell
# 1. 创建 plugins/<name>/.claude-plugin/plugin.json（手工 JSON，不用 ConvertTo-Json）
# 2. 复制 skill 到 plugins/<name>/skills/<name>/
# 3. 追加 git-subdir 条目到 .claude-plugin/marketplace.json 的 plugins 数组
claude plugin validate .
git add plugins/<name>/ .claude-plugin/marketplace.json
git commit -m "Add <name> plugin v<version>"
git push
```

## 更新插件

```shell
# 1. 改代码/commands/references + 改 package.json version + 改 plugin.json version + 改 marketplace.json version
#    任何影响用户功能的变更都必须 bump（不只是 src/）
#    bugfix → patch, feature → minor
claude plugin validate .
git add plugins/<name>/ .claude-plugin/marketplace.json
git commit -m "Update <name> to v<new-version>"
git push
```

## plugin.json 模板

```json
{
  "name": "<name>",
  "version": "1.0.0",
  "description": "<描述>",
  "author": { "name": "<作者>" },
  "repository": "https://github.com/<owner>/<repo>",
  "license": "MIT",
  "keywords": ["<kw>"]
}
```

## marketplace.json 条目模板（git-subdir）

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

## validate 失败排查

- JSON 中有 `'` → PS 5.1 `ConvertTo-Json` 过度转义，重写 JSON
- 逗号错位 → 确认新条目在 `plugins` 数组内、前有逗号、最后无逗号
- 用 `Get-Content <file> | ConvertFrom-Json` 单独测每个 JSON
