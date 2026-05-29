# IDA MCP stability policy

本文件只在 IDA MCP 调用卡住、响应很慢、分页/worker/GUI-headless 状态不明，或需要预防大查询拖垮会话时读取。目标是把官方 ida-pro-mcp/idalib-mcp 的使用注意事项转成稳定执行策略。

## 执行总则

- 大范围探索交给子 agent；主会话只做少量精读、最终判断和 IDB 落盘。
- 主会话每轮最多 1 个重型 IDA MCP 调用；不要并发 `search_text`、大范围 `insn_query`、callgraph、批量 decompile 或类型 dump。
- 多函数、多范围、多候选任务先让子 agent 做只读筛选；主会话只接收最多 10 个候选摘要和 1-3 个下一步地址。
- 任何查询如果 3-5 分钟仍无输出，视为过宽或 worker 卡住；不要原样重试，改为更小范围或新会话接摘要。

## 官方文档要点转化

- ida-pro-mcp/idalib-mcp 支持反编译、反汇编、xref、搜索、调用图、类型、注释、重命名和 patch；修改类操作必须主会话确认后执行。
- 搜索和枚举工具支持分页；`limit/count` 是保护上下文的上限，不代表结果完整。看到 `next`、`done`、truncated 或候选质量低时再分页扩展。
- 批量 API 可能对每一项返回 `error` 字段；结论前必须检查逐项错误，不把部分失败当成完整结果。
- 数值转换不要手算；使用 `int_convert` 或 `get_int`，避免进制、端序和符号位错误。
- 不要依据旧注释直接下结论；以当前 decompile、disasm、xref、字符串、常量、调用关系为准。

## worker / GUI-headless 注意事项

- headless `idalib-mcp` 默认存在 worker 限制；并发重查询可能排队或相互拖慢，不要把多个大查询同时发给同一数据库。
- 多 agent 共用同一 server 时，应使用隔离上下文或明确 database/session，避免活动数据库被其他 agent 切换。
- 如果 GUI IDA 打开了同一 IDB，服务可能优先使用 GUI 实例；GUI 关闭后可能回退到 headless worker。
- GUI 中未保存的修改不一定被 headless fallback 看到；需要让后续 headless 分析看到时，先保存 IDB。
- `idalib_switch` 只切换活动上下文，不代表 worker 空闲；切换后仍应先做小 health/lookup 验证。

## 防卡死参数起点

- `disasm`：主会话 `max_instructions <= 120`，用 offset 分页。
- `decompile`：主会话一次只反编译 1 个明确相关函数。
- `xrefs_to` / `xref_query`：主会话 `count <= 50`；引用很多交给子 agent 筛选。
- `insn_query`：主会话从 `count <= 80`、`max_scan_insns <= 5000` 起步；多范围查询交给子 agent 串行执行。
- `callgraph`：从 `max_depth <= 2` 起步，返回关键边，不返回完整图。
- `search_text`：不要用于函数范围内泛搜；只有明确 pattern 且 `limit <= 30` 时才考虑。
- `list_funcs` / `imports` / `type_query` / 资源 dump：默认子 agent 或分页摘要。

## 卡住后的恢复流程

1. 停止等待，不在主会话追加更多 IDA MCP 查询。
2. 记录当前目标、已知地址、正在跑的 tool、参数和最后可靠证据。
3. 不原样重试；把任务改成单地址、单函数、单页 disasm 或子 agent 串行筛选。
4. 如 worker 状态可疑，先做 `server_health` / `idalib_health` / 小范围 `lookup_funcs` 验证。
5. 如果上下文已经膨胀，转 `context-recovery.md`，新会话接摘要继续。

## 子 agent 约束补充

子 agent 可以承担大范围探索，但必须：

- 只读，不修改 IDB，不写文件。
- 重型查询串行收敛，不并发打满同一 IDA worker。
- 对分页结果说明是否完整、是否还有 `next`。
- 返回候选地址、证据摘要、置信度、下一步；不要返回完整 tool output。
- 如果工具卡住或部分失败，直接报告失败点和降级建议，不猜测结论。
