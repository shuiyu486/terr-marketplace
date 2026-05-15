# CLAUDE.local.md — terr-marketplace 维护指南

terr-marketplace 是 Terr 的 Claude Code 插件集合，通过 GitHub 分发。使用 `git-subdir` 格式，用户无需 `--sparse` 参数即可安装。

## 仓库信息

- **GitHub**: `https://github.com/shuiyu486/terr-marketplace`
- **本仓库**：即当前目录 — 克隆后 Claude Code 自动加载本文件
- **工作副本**：维护者可在任意目录维护个人工作副本，修改后同步到本仓库根目录随 git 分发

## 快速上手（新维护者）

```shell
git clone https://github.com/shuiyu486/terr-marketplace.git
cd terr-marketplace
claude plugin validate .
```

## 目录结构

```
terr-marketplace/
├── .claude-plugin/
│   └── marketplace.json           ← 市场注册表（所有插件在此注册）
├── .gitignore
├── README.md                      ← marketplace 级说明（面向用户）
├── CLAUDE.local.md                ← 维护指南（面向开发者，本文件）
└── plugins/                       ← 所有插件
    ├── config-sync/               ← 终端配置双向同步
    ├── dm-api/                    ← 大漠插件 API 文档
    ├── hookify/                   ← 钩子规则创建
    ├── skill-creator/             ← Skill 全生命周期管理
    └── skills2ccPlugin/           ← Skill → 插件发布工具
```

插件详情见 `.claude-plugin/marketplace.json`。

## 添加新插件流程

1. **准备 skill 目录**（由 skill-creator 生成或手写）
2. **使用 skills2ccPlugin**（推荐）或手动：
   - 创建 `plugins/<name>/.claude-plugin/plugin.json`
   - 复制 skill 内容到 `plugins/<name>/skills/<name>/`
   - 编写 `plugins/<name>/README.md`
3. **注册到 marketplace.json** — 在 `plugins` 数组末尾追加 git-subdir 条目
4. **验证**: `claude plugin validate .`
5. **提交推送**:
   ```shell
   git add plugins/<name>/ .claude-plugin/marketplace.json
   git commit -m "Add <name> plugin v1.0.0"
   git push
   ```

## 更新已有插件流程

1. 修改 `plugins/<name>/` 下的文件
2. 更新 `plugins/<name>/.claude-plugin/plugin.json` 中的 `version`
3. 同步更新 `.claude-plugin/marketplace.json` 中对应条目的 `version`
4. 按添加流程验证、提交、推送：

```shell
claude plugin validate .
git add plugins/<name>/ .claude-plugin/marketplace.json
git commit -m "Update <name> to v<new-version>"
git push
```

## 关键技术约定

### git-subdir 格式（必须遵守）

所有插件在 `marketplace.json` 中必须使用 `git-subdir` source：

```json
"source": {
  "source": "git-subdir",
  "url": "https://github.com/shuiyu486/terr-marketplace.git",
  "path": "plugins/<name>"
}
```

### PowerShell 编码（Windows 关键）

- 所有配置文件读写使用 UTF-8 无 BOM
- **绝对禁止** `Set-Content -Encoding UTF8`（带 BOM）和不带 `-Encoding` 的读写（默认 GBK）
- 正确写入：`[System.IO.File]::WriteAllText($path, $content, (New-Object System.Text.UTF8Encoding $false))`
- `ConvertTo-Json` 在 PS 5.1 中有多个坑：撇号过度转义、默认 -Depth 2 截断、缩进非标准。生成 plugin.json 时用手工构造 JSON 字符串

### plugin.json 规范

```json
{
  "name": "<name>",
  "version": "1.0.0",
  "description": "<简短描述>",
  "author": { "name": "<作者>" },
  "repository": "https://github.com/<owner>/<repo>",
  "license": "MIT",
  "keywords": ["<kw1>", "<kw2>"]
}
```

## 插件间依赖关系

- **skill-creator** → **skills2ccPlugin**：skill-creator 创建的 skill 通过 skills2ccPlugin 发布到 marketplace
- **config-sync** 管理自己的 `CLAUDE.local.md`，与 marketplace 维护相关
- **hookify**、**dm-api** 独立，无相互依赖

## 常见问题

### `claude plugin validate .` 失败

- **JSON 解析错误**：检查 `plugin.json` 或 `marketplace.json` 中是否有 `'` 等转义问题（PS 5.1 `ConvertTo-Json` 常见）
- **缺失字段**：对照本文件的 `plugin.json 规范` 逐字段检查
- **marketplace.json 逗号错位**：确认新增条目在 `plugins` 数组内，前一条目后有逗号，最后一条目后无逗号
- 用 `Get-Content <file> | ConvertFrom-Json` 单独测试每个 JSON 文件

### 用户安装不到最新插件

用户需要主动更新 marketplace：
```shell
/plugin marketplace update terr-marketplace
```
