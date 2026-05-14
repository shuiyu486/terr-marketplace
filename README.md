# terr-marketplace

Terr 的 Claude Code 插件集合。通过 GitHub 分发，使用 `git-subdir` 格式，无需 `--sparse` 参数。

## 安装与使用

### 添加 marketplace

```shell
/plugin marketplace add shuiyu486/terr-marketplace
```

或 CLI 方式：

```shell
claude plugin marketplace add shuiyu486/terr-marketplace
```

### 安装插件

```shell
# 列出可选插件
/plugin marketplace list

# 安装
/plugin install <plugin-name>@terr-marketplace
```

例如：

```shell
/plugin install config-sync@terr-marketplace
/plugin install plugin-publisher@terr-marketplace
```

### 更新 marketplace

```shell
/plugin marketplace update terr-marketplace
```

## 可用插件

| 插件 | 版本 | 说明 |
|------|------|------|
| `config-sync` | 1.0.0 | 双向同步终端配置文件（WezTerm, Nushell, Starship 等） |
| `plugin-publisher` | 1.0.0 | 将 skill-creator 生成的 skill 发布到 terr-marketplace |

## 目录结构

```
terr-marketplace/
├── .claude-plugin/
│   └── marketplace.json       ← 市场注册表
├── .gitignore
├── README.md                  ← 本文档
└── plugins/                   ← 所有插件存放目录
    ├── config-sync/
    │   ├── .claude-plugin/
    │   │   └── plugin.json
    │   └── skills/
    │       └── config-sync/
    │           ├── SKILL.md
    │           ├── references/
    │           └── scripts/
    └── plugin-publisher/
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            └── plugin-publisher/
                ├── SKILL.md
                └── references/
```

## 添加新插件

### 方式一：使用 plugin-publisher skill（推荐）

在 Claude Code 中对话式操作：

```
使用 plugin-publisher 发布 <skill 路径>
```

plugin-publisher 会自动完成：创建 plugin.json → 组织目录 → 注册 marketplace.json → 验证 → 提示提交。

### 方式二：手动操作

1. **创建插件目录和清单**

```
plugins/<plugin-name>/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── <plugin-name>/
        ├── SKILL.md
        ├── references/
        └── scripts/
```

2. **编写 plugin.json**

```json
{
  "name": "<plugin-name>",
  "version": "1.0.0",
  "description": "<描述>",
  "author": { "name": "<作者>" },
  "license": "MIT",
  "keywords": ["<关键词>"]
}
```

3. **注册到 marketplace.json**

在 `plugins` 数组中追加：

```json
{
  "name": "<plugin-name>",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/shuiyu486/terr-marketplace.git",
    "path": "plugins/<plugin-name>"
  },
  "description": "<描述>",
  "version": "1.0.0",
  "author": { "name": "<作者>" },
  "license": "MIT",
  "keywords": ["<关键词>"]
}
```

4. **验证、提交、推送**

```shell
# 验证
claude plugin validate .
# or: /plugin validate .

# 提交推送
git add plugins/<plugin-name>/ .claude-plugin/marketplace.json
git commit -m "Add <plugin-name> plugin v1.0.0"
git push
```

## 更新已有插件

1. 修改 `plugins/<name>/` 下的文件
2. 更新 `plugins/<name>/.claude-plugin/plugin.json` 中的 `version`
3. 同步更新 `marketplace.json` 中对应条目的 `version`
4. 验证 → 提交 → 推送

```shell
claude plugin validate .
git add plugins/<name>/ .claude-plugin/marketplace.json
git commit -m "Update <name> to v<new-version>"
git push
```

用户执行 `/plugin marketplace update terr-marketplace` 后即可获取更新。

## 技术说明

### 为什么使用 git-subdir？

Claude Code 克隆第三方 marketplace 时默认只 checkout `.claude-plugin/` 根目录。传统相对路径 source（如 `./plugins/xxx`）会因找不到 `plugins/` 子目录而失败，需要 `--sparse` 参数。

`git-subdir` source 类型让**每个插件独立执行稀疏克隆**，从 GitHub 只拉取自己的子目录，彻底解决此问题。

### 添加 marketplace 时的对比

| 方式 | 命令 |
|------|------|
| 传统相对路径（需 --sparse） | `/plugin marketplace add owner/repo --sparse .claude-plugin plugins` |
| git-subdir（本仓库采用） | `/plugin marketplace add owner/repo` |
