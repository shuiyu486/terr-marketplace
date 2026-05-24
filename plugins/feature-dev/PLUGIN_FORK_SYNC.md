# feature-dev fork 同步账本

## 上游来源
- 仓库：https://github.com/anthropics/claude-code
- 路径：plugins/feature-dev
- 分支：main
- 最近同步基线：39e853e4074d90f27afdfb7ea601e0fc378bd0c5

## 本地插件
- 仓库：https://github.com/shuiyu486/terr-marketplace.git
- 路径：plugins/feature-dev
- 推送 remote：origin
- 推送分支：main

## 需要保留的本地魔改
- `.claude-plugin/plugin.json` — 保留 terr-marketplace 发布所需的 `repository`、`license`、`keywords` 元数据，并同步本地融合版描述和版本号；上游官方 plugin.json 当前只包含基础插件元数据。
- `commands/feature-dev.md` — Phase 1 已融合 `obra/superpowers` 的 brainstorming 思路，保留“探索上下文、逐步提问、提出方向、形成 Design Seed、等待批准”的本地工作流；后续 Phase 2-7 仍沿用官方 feature-dev 流程。
- `README.md` — 记录本地融合版 Phase 1 和版本信息，避免用户文档回退为官方原版描述。

## 跟随上游的内容
- `agents/code-architect.md` 默认跟随上游。
- `agents/code-explorer.md` 默认跟随上游。
- `agents/code-reviewer.md` 默认跟随上游。
- 未在“需要保留的本地魔改”中列出的文件默认跟随上游。
- 已经回归上游或与上游一致的文件不要写入本地魔改清单；回归原因写进 commit message。

## 同步策略
- 对比策略：hash-first
- 自动应用：仅低风险变更
- 推送策略：用户确认同步后自动提交并推送

## 额外灵感来源
- 仓库：https://github.com/obra/superpowers
- 路径：skills/brainstorming
- 许可证：MIT
- 用途：仅融合其 discovery/brainstorming 流程思想；未复制脚本或视觉伴侣资源。

## 同步备注
- `PLUGIN_FORK_SYNC.md` 是本地维护账本，不来自上游；同步上游时不要把它作为上游差异处理。
- 根 `.claude-plugin/marketplace.json` 的 `feature-dev` 条目属于 marketplace 注册信息，不是官方插件子目录的一部分；同步插件内容时需要单独保持版本和元数据一致。
