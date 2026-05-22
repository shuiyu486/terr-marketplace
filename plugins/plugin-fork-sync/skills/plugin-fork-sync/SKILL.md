---
name: plugin-fork-sync
description: Command-only helper for `/plugin-fork-sync`.
compatibility: Claude Code on Windows or Unix; uses bundled references for first-run and update-run workflows; never overwrites plugin files without explicit user approval; after the user confirms a sync/apply action, commit and push the sync changes automatically when the repository state is safe.
---

# Plugin Fork Sync — 手动魔改插件同步

本 skill 只作为 `/plugin-fork-sync` slash command 的执行引擎。它帮助维护从官方或其他上游插件魔改而来的 Claude Code marketplace 插件。

## 手动触发规则

- 只在用户显式运行 `/plugin-fork-sync` 时执行。
- 普通对话中出现“插件同步”“上游更新”“魔改插件”等词时，不要主动触发本 skill。
- 如果不是 slash command 入口，请只提示用户使用 `/plugin-fork-sync ...`。

## 两种模式

先确定目标本地插件根目录，然后检查是否存在：

```text
PLUGIN_FORK_SYNC.md
```

- 不存在：读取 `references/first-run.md`，执行首次同步流程，并帮助生成 `PLUGIN_FORK_SYNC.md`。
- 存在：读取 `references/update-run.md`，按账本执行已有账本更新流程。

## 输入识别

从 `/plugin-fork-sync` 的参数和用户补充中识别：

1. 本地魔改插件目录。
2. 上游插件仓库 URL、分支/commit、插件子路径。
3. 本地 marketplace 仓库 URL 和插件子路径。
4. 用户意图：只计划、生成账本、应用低风险更新；用户确认执行同步/应用后，commit 和 push 默认自动进行。

缺少本地目录或上游来源时，先询问用户。不要猜测未提供的 URL。

## 共同安全原则

- 保护本地魔改优先于追新；不要用上游目录直接覆盖目标插件。
- 默认只读分析；只有用户明确要求应用补丁、修改本地文件或确认执行同步时才写入。
- 优先使用 hash-first：先比较文件列表和 hash，再读取必要文件内容。
- 用户确认执行同步/应用后，commit 和 push 视为已授权；执行前仍要检查工作区只包含本次同步相关改动，并展示目标 remote/branch。删除、reset、clean、强制 checkout 等破坏性操作仍必须单独确认。
- `PLUGIN_FORK_SYNC.md` 是本地维护账本，不来自上游；除非用户要求更新账本，否则不要把它纳入上游同步补丁。它不是提交历史记录，不要记录已完成同步的叙事原因；这类历史原因应放进 commit message。
- 生成或更新 `PLUGIN_FORK_SYNC.md` 时，把它作为目标插件仓库中的受版本控制文件处理，并纳入本次同步提交，便于在其它电脑继续管理和迭代。
- 账本和报告中的路径优先使用 repo-relative 或 plugin-relative 形式，例如 `plugins/<plugin-name>`、`hooks/pretooluse.py`；避免写入本机绝对路径。只有在用户输入歧义、需要定位当前机器文件，或报告临时工作目录时才展示绝对路径。

## 默认报告语言与排版

默认使用中文报告和中文 `PLUGIN_FORK_SYNC.md`。报告要方便快速扫读，不要输出成一整段文字：

- 先给出 3-5 行“重点结论”，用 `🚨 高风险`、`⚠️ 需确认`、`✅ 可自动同步`、`ℹ️ 信息` 这类醒目标记区分严重程度。
- 用表格呈现文件级差异；每行必须包含“文件 / 差异类型 / 风险 / 建议 / 原因”。
- 把“必须用户确认的问题”和“已可执行的低风险步骤”分成两个小节。
- 对长列表做分组和截断摘要，必要时说明“仅展示重点差异，完整 diff 已通过工具检查”。

## commit message 要求

当用户确认同步并允许提交时，commit message 不只写“同步了什么”，还要说明为什么同步或为什么回归上游：

- 如果某个本地差异被回归为上游，说明回归原因，例如“上游已修复同类问题”“该差异不再是本地长期维护项”“用户确认该差异应跟随上游”。
- 如果原因来自上游提交，优先引用或概括相关 upstream commit message；无法获取时，明确写“未能获取上游提交信息，依据文件 diff/用户确认判断”。
- 如果保留本地魔改，说明保留原因，例如“Windows UTF-8 hook 输入修复仍未进入上游”。
- 提交正文使用中文或英文均可，但原因必须清楚，避免只有 `sync upstream` 这类空泛描述。

## 固定默认值

如果用户只提供需要同步的本地插件名和上游插件 URL，可使用这些默认值推导路径：

- 本地 marketplace：`~/.claude/plugins/marketplaces/terr-marketplace`
- 本地 marketplace 远程：`https://github.com/shuiyu486/terr-marketplace`

本地插件名可解析为 `~/.claude/plugins/marketplaces/terr-marketplace/plugins/<plugin-name>`。仍然要确认用户是只检查、生成账本，还是应用更新；一旦用户确认应用同步，后续 commit/push 按默认自动流程执行。
