# IDA MCP context recovery

本文件只在上下文膨胀、`/compact` 失败、需要裁剪 transcript 或新会话恢复时读取。

## 立即止损

- 一旦出现 `input exceeds the context window`，不要继续追加 IDA MCP 查询。
- `/compact` 失败说明压缩请求本身也超过后端限制，继续重试通常无效。
- 优先保全 transcript，再裁剪或新会话接摘要。

## 安全恢复优先级

1. **新会话接摘要**：最安全。手动复制当前目标、关键地址、已验证结论。
2. **裁剪 transcript**：适合必须 resume 原会话时。先备份，再回滚到安全 user prompt。
3. **继续原会话**：只有在仍能正常请求时才考虑，并应立即降低 IDA MCP 输出规模。

## transcript 裁剪原则

- 先备份原 `.jsonl`。
- 裁剪点选在完整 user message 行，避免停在 tool_use/tool_result 中间。
- 优先回滚到“大型 IDA MCP 调用之前”的用户请求。
- 裁剪后验证每行都是合法 JSON。
- 不要删除后直接丢失备份。

## 新会话接摘要模板

```text
之前会话因 IDA MCP 输出过大导致 context 溢出，不能 /compact。请继续当前分析，但必须按小范围查询执行。

当前目标：<目标>
已知关键地址/函数：<列表>
已验证结论：<简短结论>
待验证问题：<下一步>
约束：不要批量 decompile/disasm；大范围搜索交给子 agent；主会话每轮只精读 1 个函数。
```

## 降级策略

- `survey_binary` 只用 `detail_level="minimal"`。
- `disasm` 限制 `max_instructions <= 120`。
- `xref/list/search` 限制 `count/limit <= 50`。
- 大函数先让子 agent 预读并摘要。
- 主会话只保留 1-3 个下一步地址。
