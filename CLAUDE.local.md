# CLAUDE.local.md — terr-marketplace 管理入口

本目录用于维护、迭代 `shuiyu486/terr-marketplace` 的 Claude Code 插件市场，但当前目录不一定是 marketplace git 仓库。

## 重要原则

- 不要在当前目录 clone `terr-marketplace`，除非用户明确要求。
- 真正修改 marketplace 或插件时，优先在本地 marketplace 仓库根目录操作。
- 详细维护规则在 `marketplace-manager.md`。
- 不要默认整篇读取 `marketplace-manager.md`；只在任务命中下方路由时读取相关 section。
- 如果当前目录没有 `marketplace-manager.md`，到本地 marketplace 仓库根目录查找。

## 仓库定位

本地 marketplace 仓库通常位于：

- Windows: `~\.claude\plugins\marketplaces\terr-marketplace`
- macOS/Linux: `~/.claude/plugins/marketplaces/terr-marketplace`

当前机器的实际路径以用户说明或文件系统为准。

## 按需加载路由

处理以下任务时，先用 `Grep` 在 `marketplace-manager.md` 中定位对应标题，再只读取该 section 附近内容。

| 任务类型 | 读取 section |
|---|---|
| 判断当前目录、找 marketplace 仓库、确认不要 clone | `## 仓库定位与工作目录` |
| 添加新插件、从 skill 转插件、注册 marketplace | `## 添加插件流程` |
| 修改已有插件、发布新版本、更新 marketplace 条目 | `## 更新插件流程` |
| 判断是否需要 bump version、同步哪些 version 文件 | `## 版本同步规则` |
| 修改 `.claude-plugin/marketplace.json`、source/path/metadata | `## marketplace.json 规则` |
| 在 Windows / PowerShell 下写 JSON、处理编码 | `## PowerShell 与 JSON 陷阱` |
| `claude plugin validate .` 失败 | `## validate 失败排查` |
| 准备 commit / push / PR 前检查 | `## 发布前检查清单` |

## 默认操作边界

- 用户只是询问概念、路径、是否需要同步时，不读取 `marketplace-manager.md`。
- 用户要求实际修改 marketplace、插件、版本、发布配置时，按路由读取相关 section。
- 不要把插件级历史 bug 写入本文件；插件细节放在插件目录自己的记忆或 references 中。
