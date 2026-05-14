---
name: skills2ccPlugin
description: >-
  将 skill 转换为 terr-marketplace 可安装插件。当用户想把 skill 发布到 marketplace，
  将 skill-creator 的输出打包为插件，或提到"发布 skill"、"打包插件"、"注册到 marketplace"、
  "让 skill 能通过 /plugin install 安装"时使用。即使措辞不同（"上线"、"分享"、"分发"），
  只要意图是将 skill 变成 marketplace 中的可安装单元，就应该触发。
---

# skills2ccPlugin

将一个 skill 目录转换为 terr-marketplace 插件。读取 SKILL.md 元数据，
生成 plugin.json，组织目录结构，注册 marketplace.json（git-subdir），验证。

## 重要前提

- marketplace 仓库在 `C:\AI\m_projects\m_agents\terr-marketplace`
- 所有插件使用 **git-subdir** source 格式，否则用户安装时需 `--sparse` 参数
- 插件目录固定为 `plugins/<name>/`，skill 内容放在 `plugins/<name>/skills/<name>/`

## 目标目录结构

源 skill（由 skill-creator 生成）通常是：
```
skills/<name>/
├── SKILL.md
├── references/  (可选)
└── scripts/     (可选)
```

转换为 marketplace 插件后：
```
plugins/<name>/
├── .claude-plugin/
│   └── plugin.json           ← 新建
└── skills/
    └── <name>/
        ├── SKILL.md           ← 从源 skill 复制
        ├── references/        ← 从源 skill 复制
        └── scripts/           ← 从源 skill 复制
```

## 操作流程

### 1. 提取元数据

读取源 skill 的 `SKILL.md` YAML frontmatter，提取 `name` 和 `description`。
向用户确认 version（默认 1.0.0）、author、license（默认 MIT）、keywords。

### 2. 创建 plugin.json

```json
{
  "name": "<name>",
  "version": "1.0.0",
  "description": "<description>",
  "author": { "name": "<author>" },
  "license": "MIT",
  "keywords": ["<kw1>", "<kw2>"]
}
```

### 3. 组织文件

按上述目标结构复制文件。`skills/<name>/` 子目录名必须与 plugin name 完全一致。

### 4. 注册 marketplace.json

在 `.claude-plugin/marketplace.json` 的 `plugins` 数组末尾追加。
**必须用 git-subdir 格式**——它让每个插件独立从 GitHub 稀疏克隆子目录，
用户添加 marketplace 时无需 `--sparse` 参数：

```json
{
  "name": "<name>",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/shuiyu486/terr-marketplace.git",
    "path": "plugins/<name>"
  },
  "description": "<description>",
  "version": "1.0.0",
  "author": { "name": "<author>" },
  "license": "MIT",
  "keywords": ["<kw1>", "<kw2>"]
}
```

**关键**：不要修改已有条目。确保插入后的 JSON 仍合法（逗号位置、括号闭合）。

### 5. 验证

```shell
claude plugin validate C:\AI\m_projects\m_agents\terr-marketplace
```

验证失败则修复后重试，不要跳过。

### 6. 提交推送

```shell
cd C:\AI\m_projects\m_agents\terr-marketplace
git add plugins/<name>/ .claude-plugin/marketplace.json
git commit -m "Add <name> plugin v<version>"
git push
```

## 边界情况

- 若 `plugins/<name>/` 已存在，询问用户是覆盖还是跳过
- 若源 skill 无 references/ 或 scripts/ 目录，跳过即可
- plugin name 在整个 marketplace 中必须唯一
- 不要修改 marketplace.json 中已有的其他 `plugins` 条目
