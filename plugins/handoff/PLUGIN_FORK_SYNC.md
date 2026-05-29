# handoff fork 同步账本

## 上游来源

- 仓库：https://github.com/mattpocock/skills
- 路径：skills/productivity/handoff
- 分支：main
- 最近同步基线：e3b90b5238f38cdea5996e16861dcae28ef52eda

## 本地插件

- 仓库：https://github.com/shuiyu486/terr-marketplace
- 路径：plugins/handoff
- 推送 remote：origin
- 推送分支：main

## 需要保留的本地魔改

- `.claude-plugin/plugin.json` — terr-marketplace 插件包装元数据，不来自上游 skill 目录。
- `commands/handoff.md` — 将上游 skill 改包为仅 slash command 触发的本地入口，避免 description 自动触发。
- `PLUGIN_FORK_SYNC.md` — 本地 fork 同步账本，不来自上游。
- `.claude-plugin/marketplace.json` 中的 `handoff` 条目 — marketplace 注册信息，由 terr-marketplace 维护。

## 跟随上游的内容

- `commands/handoff.md` 的核心 handoff 规则默认跟随上游 `skills/productivity/handoff/SKILL.md` 的语义，但入口形态保持为本地 slash command。
- 不保留 `skills/handoff/SKILL.md`，以确保该插件只能通过 `/handoff` 命令触发。
- 未在“需要保留的本地魔改”中列出的文件默认跟随上游。

## 同步策略

- 对比策略：hash-first
- 自动应用：仅低风险变更
- 推送策略：用户确认同步后自动提交并推送
