---
name: plugin-publisher
description: >-
  将 skill 发布到 terr-marketplace。将 skill-creator 生成的 skill 目录转换为 marketplace 插件格式，
  自动创建 plugin.json、组织 skills/ 目录结构、注册到 marketplace.json（git-subdir 格式）并验证。
  Trigger phrases (EN): publish skill to marketplace, convert skill to plugin, register skill in marketplace,
  add skill to terr-marketplace, 发布 skill 到 marketplace, 将 skill 转换为插件, 注册 skill 到 marketplace
---

# Plugin Publisher

将 skill-creator 生成的 skill 目录转换为 terr-marketplace 中可通过 `/plugin install` 安装的插件。

## 输入来源

支持以下两种输入方式：

1. **本地目录路径** — skill-creator 生成的 `skills/<name>/` 目录
2. **直接在对话中** — 用户描述了 skill 的内容，skill-creator 刚在对话中生成了 SKILL.md

## 关键路径

| 用途 | 路径 |
|------|------|
| marketplace 仓库根目录 | `C:\AI\m_projects\m_agents\terr-marketplace` |
| 插件存放目录 | `<repo>/plugins/<plugin-name>/` |
| marketplace 注册表 | `<repo>/.claude-plugin/marketplace.json` |
| plugin 清单 | `<repo>/plugins/<name>/.claude-plugin/plugin.json` |
| skill 文件 | `<repo>/plugins/<name>/skills/<name>/SKILL.md` |

## 发布流程

### 第一步：收集信息

从用户提供的 skill 目录中读取 `SKILL.md` 的 YAML frontmatter，提取 `name` 和 `description`。

向用户确认或询问以下元数据（如 SKILL.md 中已有则作为默认值）：

- **name**: skill 的唯一标识符（与 SKILL.md frontmatter 中的 name 一致）
- **version**: 版本号，默认 `1.0.0`
- **description**: 从 SKILL.md frontmatter 提取
- **author.name**: 作者名
- **license**: 许可证，默认 `MIT`
- **keywords**: 关键词数组
- **repository**: 关联仓库 URL（可选）
- **homepage**: 项目主页 URL（可选）

### 第二步：创建 plugin.json

在 `<repo>/plugins/<name>/.claude-plugin/plugin.json` 创建文件，格式如下：

```json
{
  "name": "<name>",
  "version": "<version>",
  "description": "<description>",
  "author": { "name": "<author>" },
  "repository": "<optional-repo-url>",
  "license": "<license>",
  "keywords": ["<kw1>", "<kw2>"]
}
```

参考 `C:\AI\m_projects\m_agents\terr-marketplace\plugins\config-sync\.claude-plugin\plugin.json` 作为模板。

### 第三步：组织插件目录结构

确保文件按以下结构放置：

```
plugins/<name>/
├── .claude-plugin/
│   └── plugin.json          ← 第二步创建
└── skills/
    └── <name>/
        ├── SKILL.md          ← 从源 skill 复制
        ├── references/       ← 如有，从源 skill 复制
        │   └── *.md
        └── scripts/          ← 如有，从源 skill 复制
            └── *
```

注意：`skills/<name>/` 子目录名必须与 plugin name 一致。

### 第四步：注册到 marketplace.json

读取 `<repo>/.claude-plugin/marketplace.json`，在 `plugins` 数组中追加新条目。

**固定使用 git-subdir 格式**（不需要 `--sparse` 参数）：

```json
{
  "name": "<name>",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/shuiyu486/terr-marketplace.git",
    "path": "plugins/<name>"
  },
  "description": "<description>",
  "version": "<version>",
  "author": { "name": "<author>" },
  "license": "<license>",
  "keywords": [<keywords>]
}
```

确保 `marketplace.json` 仍是合法的 JSON（注意逗号、括号匹配）。

### 第五步：验证

运行验证命令：

```shell
claude plugin validate C:\AI\m_projects\m_agents\terr-marketplace
```

如验证失败，检查并修复错误后重新验证。

### 第六步：提交

验证通过后，提示用户提交并推送：

```shell
cd C:\AI\m_projects\m_agents\terr-marketplace
git add plugins/<name>/ .claude-plugin/marketplace.json
git commit -m "Add <name> plugin v<version>"
git push
```

## 注意事项

- **不要**修改 `marketplace.json` 中已有的其他插件条目
- plugin name 必须与 skill name 一致，且在整个 marketplace 中唯一
- 所有 source 固定使用 `git-subdir` 格式的 GitHub URL
- 验证步骤不可跳过，必须在提交前通过验证
- 如果目标 `plugins/<name>/` 已存在，询问用户是否覆盖
