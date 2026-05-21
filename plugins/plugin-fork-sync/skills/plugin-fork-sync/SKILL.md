---
name: plugin-fork-sync
description: |
  Manage Claude Code marketplace plugins that are forked, copied, or locally customized from an upstream plugin. Use this skill whenever the user wants to check whether an original Claude plugin has updated, compare an official upstream plugin with their own modified plugin, sync forked marketplace plugins, port upstream changes without overwriting local edits, audit plugin lineage, or prepare a safe merge plan for repos such as terr-marketplace. Trigger on Chinese or English phrases like “插件原身更新了吗”, “同步官方插件”, “魔改插件”, “forked plugin”, “upstream plugin update”, “marketplace plugin sync”, “别覆盖我的修改”, or mentions of comparing `anthropics/claude-plugins-official` with a custom marketplace.
compatibility: Claude Code on Windows or Unix; prefers git/gh when available; never pushes or overwrites plugin files without explicit user approval.
---

# Plugin Fork Sync — 魔改插件上游同步

帮助用户管理 Claude Code marketplace 中“从官方或其他上游插件复制后改造”的插件：检查上游是否有更新，识别本地魔改内容，并生成可审阅的同步方案。

## 核心原则

- 保护本地魔改优先于追新。不要用上游目录直接覆盖目标插件。
- 默认只读分析；只有用户明确要求“应用补丁/修改本地文件”时才写入目标插件。
- 优先做三方对比：上次同步基线、上游最新版、本地魔改版。
- 如果找不到基线，不要声称能安全自动合并；降级为“人工审阅模式”。
- 所有 push、PR、删除、reset、clean、强制 checkout 等共享或破坏性操作都必须先问用户。

## 需要识别的输入

从用户提示或本地文件中提取：

1. **上游插件来源**：仓库 URL、分支或 commit、插件子目录。
   - 示例：`https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator`
2. **本地魔改插件**：本地目录、远程仓库 URL、插件子目录。
   - 示例：`~/.claude/plugins/marketplaces/terr-marketplace/plugins/hookify`
3. **marketplace 仓库**：本地仓库和远程仓库。
   - 示例：`~/.claude/plugins/marketplaces/terr-marketplace`
4. **同步意图**：只检查、生成补丁、实际应用补丁、创建提交/PR。

如果缺少上游来源或本地目标路径，先问用户。不要猜测非用户提供的 URL。

## 推荐的同步账本：PLUGIN_FORK_SYNC.md

目标插件根目录的 `PLUGIN_FORK_SYNC.md` 是首选同步账本。它是每个魔改插件专有的维护文件，用来记录上游来源、上次同步基线、自身插件仓库和本地魔改范围，避免把同步元数据塞进 `CLAUDE.local.md`。

建议结构：

```markdown
# Plugin Fork Sync

## Upstream
- repo: https://github.com/anthropics/claude-plugins-official
- path: plugins/skill-creator
- branch: main
- lastSyncedCommit: <last-synced-upstream-commit>

## Local plugin
- repo: https://github.com/shuiyu486/terr-marketplace
- path: plugins/hookify
- pushRemote: origin
- pushBranch: main

## Local modifications
- .claude-plugin/plugin.json — renamed/re-described plugin metadata
- README.md — local marketplace documentation
- hooks/pretooluse.py — Windows UTF-8 behavior change

## Sync policy
- compareStrategy: hash-first
- autoApply: low-risk-only
- pushAfterSync: ask
```

字段含义：

- `Upstream.repo/path/branch/lastSyncedCommit` 决定 `base` 与 `upstream` 的精确来源。
- `Local plugin.repo/path` 决定魔改插件所在 git 仓库和插件子目录。
- `Local modifications` 是本地魔改文件清单；通常只有一两个文件，应优先保护并重点审阅。
- `compareStrategy: hash-first` 表示先用文件 hash 找出真正变化的文件，再只读取必要文件内容，节约 token。
- `pushAfterSync` 可为 `ask`、`never`、`allowed-after-clean-check`。即使配置允许，也要遵守用户当前指令和仓库安全状态。

如果没有 `PLUGIN_FORK_SYNC.md`：

- 检查 `.claude-plugin/plugin.json`、README、提交记录中是否有 `repository`、`Forked`、`upstream`、`baseRef` 等线索。
- 如果仍找不到 `lastSyncedCommit`，询问用户是否知道上次同步的 upstream commit/tag。
- 用户不知道时，可以继续做二方比较，但报告中明确标注“无基线，不能安全自动合并”。
- 可以建议创建 `PLUGIN_FORK_SYNC.md`，但不要擅自写入，除非用户明确要求。

## 标准工作流

### 1. 建立安全工作区

- 在临时目录或只读检查环境中 clone/fetch 上游仓库和目标 marketplace。
- 不要在目标插件目录中直接运行会修改文件的 merge、checkout、reset、clean。
- Windows 环境优先使用 PowerShell 工具；读取/编辑文件优先使用 Read/Edit/Write。

### 2. 读取 PLUGIN_FORK_SYNC.md 并定位三个版本

先读取目标插件根目录的 `PLUGIN_FORK_SYNC.md`，提取：

- 上游仓库、插件路径、分支、上次同步 commit。
- 自身插件 git 仓库、插件路径、push remote、push branch。
- 本地魔改文件清单和同步策略。

然后准备这三份目录快照：

| 快照 | 含义 | 用途 |
| --- | --- | --- |
| `base` | 目标插件上次同步时的上游版本 | 判断哪些变化来自上游，哪些是本地魔改 |
| `upstream` | 当前上游最新版 | 需要考虑移植的新变化 |
| `local` | 当前本地魔改插件 | 必须保护的用户修改 |

如果 `base` 不存在，只准备 `upstream` 和 `local`，并进入审阅模式。

### 3. 用 hash-first 策略判断上游是否更新

先比较文件列表和 hash，再读取内容：

1. 对 `base`、`upstream`、`local` 生成相对路径到 hash 的清单。
2. 如果某文件在 `base` 与 `upstream` hash 相同，说明上游未改，不需要读取内容。
3. 如果某文件在 `base` 与 `local` hash 相同，说明本地未魔改，可作为低风险移植候选。
4. 对 `PLUGIN_FORK_SYNC.md` 的 `Local modifications` 列表中的文件，即使 hash 看似可自动处理，也要重点列出供用户确认。

比较 `base` 与 `upstream`：

- 如果没有差异：报告“上游相对基线无更新”，可附带当前 upstream commit。
- 如果有差异：列出新增、修改、删除、重命名文件，并总结影响范围。
- 特别关注 `.claude-plugin/plugin.json`、`SKILL.md`、`commands/`、`hooks/`、`agents/`、`scripts/`、`references/`。
- `PLUGIN_FORK_SYNC.md` 是本地维护账本，不来自上游；除非用户要求更新账本，否则不要把它纳入上游同步补丁。

### 4. 识别本地魔改

比较 `base` 与 `local`：

- 列出本地新增/修改/删除文件。
- 区分明显的品牌/命名改动、Windows 兼容修复、行为改造、文档改造、技能描述优化。
- 对 `localKeepPatterns` 中的文件默认不自动替换，只在报告中建议人工确认。

### 5. 冲突分类

按文件给出同步建议：

| 类型 | 判断 | 默认处理 |
| --- | --- | --- |
| 仅上游变更 | `base→upstream` 有变，`base→local` 无变 | 可自动移植到补丁 |
| 仅本地变更 | `base→local` 有变，`base→upstream` 无变 | 保留本地 |
| 双方同文件变更 | 两边都改同一文件 | 标为冲突，人工审阅 |
| 上游删除、本地修改 | 上游删除但本地仍改 | 标为高风险冲突 |
| 本地新增 | 只存在 local | 保留 |
| 上游新增 | 只存在 upstream | 可建议新增 |

### 6. 生成报告

默认输出中文报告，结构如下：

```markdown
## 结论
- 上游是否有更新：是/否/无法确定
- 是否能安全自动移植：是/部分/否
- 建议下一步：只审阅/生成补丁/应用补丁/补充基线信息

## 输入与基线
- 上游：repo、path、ref
- 本地：repo/path
- 基线：ref 或“未找到”

## 上游变化摘要
- 新增：...
- 修改：...
- 删除：...

## 本地魔改摘要
- 保留项：...
- 可能与上游冲突：...

## 文件级同步计划
| 文件 | 上游变化 | 本地变化 | 风险 | 建议 |
| --- | --- | --- | --- | --- |

## 待用户确认
- [ ] 是否创建或更新 `PLUGIN_FORK_SYNC.md` 同步账本
- [ ] 是否生成补丁文件
- [ ] 是否应用低风险变更
- [ ] 是否提交/推送/创建 PR
```

### 7. 生成补丁时的规则

只有用户要求生成补丁时才执行：

- 优先把补丁写到临时文件或 workspace，例如 `plugin-fork-sync-workspace/<plugin>/update.patch`。
- 补丁只包含低风险变更：仅上游变更、上游新增文件、无本地改动的文件。
- 冲突文件不要自动写入目标插件；给出文件级说明和建议合并片段。
- 应用补丁前展示将修改的文件列表并等待确认。

### 8. 应用更新后的收尾

如果用户批准应用更新：

- 修改完成后运行可用的静态检查或最小验证，例如读取 plugin.json、确认 SKILL.md frontmatter 有 `name` 和 `description`。
- 更新 `PLUGIN_FORK_SYNC.md` 的 `lastSyncedCommit` 为已同步的 upstream commit，并同步更新 `Local modifications` 清单。
- 报告修改文件和仍需人工处理的冲突。
- 如果 `PLUGIN_FORK_SYNC.md` 记录了自身插件 git 仓库、push remote 和 push branch，可准备提交与 push。

### 9. 自主提交与 push 条件

只有同时满足以下条件，才可以执行 commit/push：

- 用户当前请求明确包含“提交”“push”“推送”“自主 push”或同等含义，或 `PLUGIN_FORK_SYNC.md` 的 `pushAfterSync` 明确允许且当前任务就是同步落库。
- 工作区检查显示只包含本次同步相关改动，没有不明来源的未提交文件。
- 已展示将提交的文件列表、提交信息和目标 remote/branch。
- 没有未解决冲突或高风险文件被自动改写。

推荐提交信息：

```text
Sync <local-plugin> with upstream <upstream-plugin>
```

push 后报告 commit hash、remote/branch，以及是否还需要用户创建或查看 PR。

## 针对当前用户默认示例

当用户没有给更多参数但提到当前测试场景时，使用这些默认值：

- 上游插件：`https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator`
- 本地魔改插件：`~/.claude/plugins/marketplaces/terr-marketplace/plugins/hookify`
- 本地 marketplace：`~/.claude/plugins/marketplaces/terr-marketplace`
- 本地 marketplace 远程：`https://github.com/shuiyu486/terr-marketplace`

仍然要先确认是否只是检查，还是要生成/应用补丁。

## 常见触发示例

- “看看官方 skill-creator 更新了没，如果有，把 hookify 也同步一下，但别覆盖我的改动。”
- “对比 terr-marketplace 里的 hookify 和它的原身插件，给我一个同步计划。”
- “帮我给这个魔改插件补一个 upstream 基线文件。”
- “官方插件更新了，帮我把安全的变更移植过来，冲突的地方列出来。”
