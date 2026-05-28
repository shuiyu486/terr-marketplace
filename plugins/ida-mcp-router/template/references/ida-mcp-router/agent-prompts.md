# IDA MCP sub-agent prompts

本文件只在准备启动子 agent 做 IDA MCP 探索时读取。目标是隔离大 tool result，同时让返回值保留足够证据，避免摘要造成信息偏差。

## 通用只读筛选模板

```text
你在当前 RE 项目中协助 IDA MCP 逆向分析。任务是只读候选筛选，不要修改 IDB，不要返回完整伪代码、完整汇编、完整 CFG、完整 xref 列表或原始 tool output。

目标：<具体问题>

允许：lookup、find/search、xref、callees/callgraph、decompile/disasm 的小范围只读查询。
禁止：rename、set_type、set_comments、patch、define/undefine、declare_type、idb_save。

限制：
- 每次最多精读 1 个函数。
- disasm max_instructions <= 120。
- xref/query/list/search limit 或 count <= 50。
- callgraph max_depth <= 2 起步。
- 不要调用无界 analyze_batch、full disasm、大范围 type dump。

返回最多 300-500 字：
1. 候选地址/函数名，最多 10 条。
2. 每条的触发依据：字符串、常量、xref、调用关系、字段偏移或关键条件。
3. 判断方向：为什么可能相关，或为什么可能是误报。
4. 置信度：高/中/低。
5. 建议主会话下一步精读的 1-3 个地址。
```

## 场景模板

- xref / 字段使用筛选：要求返回 xref 来源地址、所在函数、引用方式、候选角色。
- 字符串 / 常量搜索：要求聚类命中，不返回完整命中列表。
- callgraph 探索：从 `max_depth <= 2` 开始，只返回关键边和角色。
- 大函数预读：只提炼输入/输出、字段偏移、关键调用、关键条件、可能语义。

## 返回值质量要求

每条候选至少保留地址或函数名、触发依据、判断方向、置信度、下一步建议。不要返回大段代码、完整 tool result 或无筛选列表。
