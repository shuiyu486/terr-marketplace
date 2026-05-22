---
description: Manually sync a customized Claude Code marketplace plugin with its upstream plugin
argument-hint: "<local-plugin-path> [upstream-url] [--init|--update|--plan-only]"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "AskUserQuestion", "PowerShell", "Bash", "Skill"]
---

# Plugin Fork Sync

手动维护从官方或其他上游插件魔改而来的 Claude Code marketplace 插件。

## 入口规则

只在用户显式运行 `/plugin-fork-sync` 时执行本命令。不要因为普通对话里出现“插件同步”“上游更新”等词而自动开始。

## 执行步骤

1. 使用 Skill 工具加载 `plugin-fork-sync:plugin-fork-sync`。
2. 将 `$ARGUMENTS` 作为用户的同步请求传给该 skill。
3. 由 skill 判断目标插件根目录是否存在 `PLUGIN_FORK_SYNC.md`：
   - 不存在：按首次同步流程执行，并帮助生成账本。
   - 存在：按已有账本更新流程执行。
4. 默认先输出计划；用户确认执行同步/应用更新后，自动提交并 push 本次同步相关改动，不再单独追问 commit/push。若工作区不干净、remote/branch 不明确或存在冲突，则停止并说明需要用户处理。

## 参数示例

```text
/plugin-fork-sync C:\Users\terrapin\.claude\plugins\marketplaces\terr-marketplace\plugins\hookify https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator --init
```

```text
/plugin-fork-sync C:\Users\terrapin\.claude\plugins\marketplaces\terr-marketplace\plugins\hookify --update
```
