# IDA MCP Router 项目记忆

本项目使用 IDA Pro / ida-pro-mcp / idalib 做逆向分析。优先保护 Claude Code 主会话上下文，避免大规模 IDA MCP 结果导致 context 膨胀或 `/compact` 失败。

## 常驻原则

- 主会话只做单点精读、最终判断和 IDB 修改。
- 大范围搜索、多函数/多范围探索、xref/callgraph、批量分析、大函数预读默认交给子 agent 做只读筛选。
- 主会话只做少量精读和最终落盘；每轮最多发起 1 个重型 IDA MCP 查询，避免并发 `search_text`、大范围 `insn_query`、callgraph 或批量 decompile。
- 子 agent 只返回候选地址、证据摘要、置信度和下一步建议；不要返回完整 tool output。
- 不要把完整 decompile、disasm、CFG、xref 列表或类型 dump 带回主会话。
- 修改 IDB 前必须在主会话确认目标地址、类型、注释、命名或 patch 意图。
- `/compact` 失败时停止向同一会话追加 IDA MCP 查询，改裁剪 transcript 或新会话接摘要。

## 按需加载

只读取当前任务需要的一个文档：

| 任务 | 读取 |
|---|---|
| 判断某个 IDA MCP tool 应该在主会话还是子 agent 中跑 | `references/ida-mcp-router/tool-routing.md` |
| 准备启动子 agent 做 IDA MCP 探索 | `references/ida-mcp-router/agent-prompts.md` |
| 任务范围较大，需要规划逆向分析路径 | `references/ida-mcp-router/progressive-analysis.md` |
| 搜索过宽、`search_text` 中断、需要把全局搜索收敛为候选地址精读 | `references/ida-mcp-router/search-narrowing.md` |
| IDA MCP 卡住、并发/worker/GUI-headless 状态、分页 cursor 或稳定性问题 | `references/ida-mcp-router/mcp-stability.md` |
| 上下文膨胀、`/compact` 失败、需要裁剪或新会话恢复 | `references/ida-mcp-router/context-recovery.md` |


## 默认决策

- 已知地址/单函数/少量数据读取：主会话小范围查询。
- 多函数范围、多候选地址、多个相同 offset 搜索目标：默认交给子 agent 串行筛选，主会话不并发探测。
- 未知范围/多候选/可能大量结果：先读 tool routing，再交给子 agent。
- 用户说“继续分析”但范围不明确：先提出 1-3 个窄化方向，不要直接做大范围搜索。
