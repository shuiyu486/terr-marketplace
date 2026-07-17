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
/plugin install skills2ccPlugin@terr-marketplace
```

### 更新 marketplace

```shell
/plugin marketplace update terr-marketplace
```

## 可用插件

| 插件 | 版本 | 说明 |
|------|------|------|
| `cc-statusline` | 1.0.0 | Claude Code 状态栏（模型、effort、上下文、token 统计、会话 API 消耗） |
| `config-sync` | 1.3.0 | 终端配置双向同步+快速兼容检查（WezTerm, Nushell, Starship，5 个文件） |
| `dm-api` | 1.0.0 | 大漠插件 API 文档查询（465 个函数，17 个分类） |
| `hookify` | 1.0.1 | 从对话模式创建钩子规则，防止不期望的行为 |
| `hook-terr` | 1.4.6 | 可扩展 Claude Code hook runtime，支持 Stop 通知、API error 自动恢复和显式 notify 规则 |
| `skill-creator` | 1.0.0 | Skill 全生命周期管理（创建、修改、评估、优化触发） |
| `skills2ccPlugin` | 1.0.1 | 将 skill 转换为 terr-marketplace 可安装插件并发布 |

## 目录结构

```
terr-marketplace/
├── .claude-plugin/
│   └── marketplace.json       ← 市场注册表
├── .gitignore
├── README.md                  ← 本文档
└── plugins/                   ← 所有插件存放目录
    ├── cc-statusline/        ← Claude Code 状态栏
    ├── config-sync/           ← 终端配置双向同步
    ├── dm-api/                ← 大漠插件 API 文档
    ├── hookify/               ← 钩子规则创建
    ├── hook-terr/             ← 可扩展 hook runtime 与 Stop 通知
    ├── skill-creator/         ← Skill 全生命周期管理
    └── skills2ccPlugin/       ← Skill → 插件发布工具
```

## 添加新插件

### 方式一：使用 skills2ccPlugin skill（推荐）

在 Claude Code 中对话式操作：

```
使用 skills2ccPlugin 发布 <skill 路径>
```

skills2ccPlugin 会自动完成：创建 plugin.json → 组织目录 → 注册 marketplace.json → 验证 → 提示提交。

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
