# ida-mcp-router

`ida-mcp-router` 是一个可同步、可迭代的 `CLAUDE.local.md` 项目记忆模板包，用于 IDA MCP / ida-pro-mcp / idalib 逆向分析场景。

它不是运行时 skill/command 插件；核心价值是把一套上下文安全的项目记忆模板放进 marketplace，便于在多台设备之间同步、维护和迭代，然后按需复制到具体 RE 工作目录。

## 解决的问题

IDA MCP 的大范围 xref、callgraph、batch analysis、full disasm、type dump 等工具很容易把 Claude Code 主会话上下文撑大。一旦超过后端限制，`/compact` 也可能失败。

本模板通过项目级 `CLAUDE.local.md` 实现：

- 主会话只做单点精读、最终判断和 IDB 修改。
- 大范围探索默认交给子 agent 做只读筛选。
- 详细规则放在 `references/ida-mcp-router/` 中按需读取。
- 常驻 `CLAUDE.local.md` 只保留路由索引和硬边界。

## 模板内容

```text
template/
├─ CLAUDE.local.md
└─ references/
   └─ ida-mcp-router/
      ├─ tool-routing.md
      ├─ agent-prompts.md
      ├─ progressive-analysis.md
      └─ context-recovery.md
```

## 使用方式

把 `template/` 下的内容复制到目标 RE 项目根目录：

```text
<your-re-project>/
├─ CLAUDE.local.md
└─ references/
   └─ ida-mcp-router/
      ├─ tool-routing.md
      ├─ agent-prompts.md
      ├─ progressive-analysis.md
      └─ context-recovery.md
```

之后 Claude Code 在该项目中启动时，只会常驻加载轻量 `CLAUDE.local.md`；遇到具体任务时再按路由读取对应 reference。

## 推荐同步策略

- marketplace 插件是模板真源。
- 各 RE 项目中的 `CLAUDE.local.md` 和 `references/ida-mcp-router/` 是应用副本。
- 修改模板后，根据需要同步到各项目副本。

## Version policy

当前版本：`0.2.0`。

Claude 以后编辑此插件时，凡是用户可见行为变化，都必须自动同步 bump version，不等用户提醒。

需要同步版本的位置：

- `plugins/ida-mcp-router/.claude-plugin/plugin.json`
- 根 `.claude-plugin/marketplace.json`

Bump 规则：

- Patch：文字修正、reference 小幅改进、限额微调。
- Minor：新增 reference、新增工作流、改变模板结构但不破坏使用方式。
- Major：破坏性模板结构变化、默认安全假设改变、路径约定变化。

修改后运行：

```powershell
claude plugin validate .
```
