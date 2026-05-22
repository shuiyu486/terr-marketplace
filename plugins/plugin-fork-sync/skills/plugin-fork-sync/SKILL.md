---
name: plugin-fork-sync
description: Command-only helper for `/plugin-fork-sync`.
compatibility: Claude Code on Windows or Unix; uses bundled references for first-run and update-run workflows; never pushes or overwrites plugin files without explicit user approval.
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
4. 用户意图：只计划、生成账本、应用低风险更新、提交、push。

缺少本地目录或上游来源时，先询问用户。不要猜测未提供的 URL。

## 共同安全原则

- 保护本地魔改优先于追新；不要用上游目录直接覆盖目标插件。
- 默认只读分析；只有用户明确要求应用补丁或修改本地文件时才写入。
- 优先使用 hash-first：先比较文件列表和 hash，再读取必要文件内容。
- 所有 push、PR、删除、reset、clean、强制 checkout 等共享或破坏性操作都必须先确认。
- `PLUGIN_FORK_SYNC.md` 是本地维护账本，不来自上游；除非用户要求更新账本，否则不要把它纳入上游同步补丁。

## 默认报告语言

默认使用中文报告，包含：结论、输入与基线、差异摘要、文件级同步计划、待用户确认事项。

## 固定默认值

如果用户只提供需要同步的本地插件名和上游插件 URL，可使用这些默认值推导路径：

- 本地 marketplace：`~/.claude/plugins/marketplaces/terr-marketplace`
- 本地 marketplace 远程：`https://github.com/shuiyu486/terr-marketplace`

本地插件名可解析为 `~/.claude/plugins/marketplaces/terr-marketplace/plugins/<plugin-name>`。仍然要确认用户是只检查、生成账本、应用更新，还是提交/push。
