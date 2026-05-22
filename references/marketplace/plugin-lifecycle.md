# Plugin lifecycle

用于实际添加/更新插件、同步版本，以及编辑 `.claude-plugin/marketplace.json` 条目。

## 读取条件

只在准备执行以下修改时读取本文件：

- 新增 `plugins/<name>` 或把 skill 转成 marketplace plugin。
- 修改已有插件并准备发布或 bump version。
- 编辑 `plugins/<name>/.claude-plugin/plugin.json`。
- 编辑根 `.claude-plugin/marketplace.json` 的插件条目。

不要在以下场景读取本文件：

- 只是讨论同步方案、目录设计或是否可行。
- 只是查看 marketplace 当前有哪些插件。
- 只是解释某个插件代码，不涉及发布或版本。

## 添加插件

适用场景：新增 `plugins/<name>`、将 skill 转成 marketplace plugin、注册新插件。

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

## 更新插件

适用场景：修改已有插件功能、`src/`、`commands/`、`skills/`、`references/` 或其他用户可见行为。

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

## 版本同步

常见需要同步的文件：

```text
plugins/<name>/package.json
plugins/<name>/package-lock.json
plugins/<name>/.claude-plugin/plugin.json
.claude-plugin/marketplace.json
```

| 变更类型 | bump |
|---|---|
| bugfix | patch |
| 新功能 | minor |
| 破坏性变更 | major |
| 仅内部重构且不影响用户 | 通常不 bump |
| references / commands 改变用户使用方式 | 需要 bump |

## marketplace.json 条目

文件：`.claude-plugin/marketplace.json`。

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

检查点：

- 新插件条目必须放在 `plugins` 数组内。
- 前一个条目后需要逗号，最后一个条目后不能有逗号。
- `version` 要与插件元数据同步。
- `path` 必须指向真实插件目录。
