# CLAUDE.local.md — terr-marketplace 管理入口

本目录用于维护、迭代 `shuiyu486/terr-marketplace` 的 Claude Code 插件市场。

## 重要原则

- 本文件是唯一自动加载入口；详细规则按下方路由读取 `references/marketplace/*.md`。
- 只读取当前任务命中的一个 reference 文件；不要预读整套 references。
- 如果当前目录缺少对应 reference 文件，到本地 marketplace 仓库根目录查找。


## 按需加载路由

| 任务意图 | 读取文件 | 不读取时 |
|---|---|---|
| 需要确认实际工作目录、仓库位置、是否应该在当前目录操作 git | `references/marketplace/workspace.md` | 只是讨论同步方案、文件设计或普通概念 |
| 准备实际添加/更新插件，或即将编辑插件版本、`.claude-plugin/marketplace.json` 条目 | `references/marketplace/plugin-lifecycle.md` | 只是询问是否可行、查看列表、解释现有文件，不会修改或发布 |
| 需要写 JSON、处理 PowerShell 编码、排查 `claude plugin validate .`、提交/推送/发布前检查 | `references/marketplace/validation-release.md` | 不涉及 JSON 写入、验证失败、提交、推送或发布 |


## 默认操作边界

- 用户只是询问概念、路径、是否需要同步时，不读取 reference 文件。
- 用户要求实际修改 marketplace、插件、版本、发布配置时，按路由读取对应文件。
- 不要把插件级历史 bug 写入本文件；插件细节放在插件目录自己的记忆或 references 中。
