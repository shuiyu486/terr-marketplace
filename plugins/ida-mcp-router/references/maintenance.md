# ida-mcp-router maintenance

本插件是 `CLAUDE.local.md` 项目记忆模板包，不是运行时 skill/command 插件。

## 版本 bump 必须自动执行

Claude 以后编辑此插件时，凡是用户可见行为变化，都必须自动 bump version，不等用户提醒。

必须同步版本：

- `plugins/ida-mcp-router/.claude-plugin/plugin.json`
- 根 `.claude-plugin/marketplace.json`

如果未来新增 `package.json`，也要同步。

## Bump 规则

- Patch：文字修正、reference 小幅改进、限额微调。
- Minor：新增 reference、新增工作流、改变模板结构但不破坏使用方式。
- Major：破坏性模板结构变化、默认安全假设改变、路径约定变化。

## 结构原则

- `template/CLAUDE.local.md` 保持轻量，只做常驻路由索引和硬边界。
- 详细规则放入 `template/references/ida-mcp-router/`。
- 不要重新引入 `skills/` 或 `commands/`，除非用户明确改变插件定位。
- 修改模板后，提醒用户需要同步到目标 RE 项目的应用副本。

## 验证

修改后从 marketplace 根目录运行：

```powershell
claude plugin validate .
```
