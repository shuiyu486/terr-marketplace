# IDA MCP search narrowing

本文件只在搜索范围不明确、`search_text` 过宽、搜索结果过多或搜索调用被中断时读取。目标是把全局搜索改成“候选定位 → xref 收敛 → 单点精读”，避免主会话 context 膨胀。

## 核心原则

- 不把 `search_text` 当作第一步全局扫描工具。
- 优先用结构化查询定位候选：字符串、imports、函数名、常量、已知地址。
- 搜索类 tool 必须设置 `limit` / `count`，主会话默认不超过 50。
- 搜索命中很多时交给子 agent，只返回候选地址、证据摘要、置信度和下一步。
- 宽搜索中断后，不要立刻重试同一查询；改成已知地址附近的窄范围 `disasm` / `decompile` / `xref`。

## 推荐搜索顺序

1. **已知字符串或关键词**
   - 先用 `find_regex` 查字符串表。
   - 再对字符串地址做 `xrefs_to`。
   - 最后主会话精读 1-3 个相关函数。

2. **已知 API 或导入符号**
   - 先用 `imports_query` 查 import。
   - 再查调用点或 xref。
   - 避免直接 `search_text` 搜 API 名。

3. **已知函数名、符号名或地址**
   - 先用 `lookup_funcs` / `func_query` 确认范围。
   - 对单函数 `decompile`。
   - 必要时 `disasm`，并限制 `max_instructions <= 120`。

4. **已知常量、magic number 或字段偏移**
   - 用 `find` / `insn_query` / `xref_query` 限量查候选。
   - 命中多时交给子 agent 聚类。
   - 主会话只精读排序最高的地址。

5. **只知道宽泛语义**
   - 先让用户或主会话把目标收窄成 1-3 个搜索线索。
   - 不直接全局 `search_text` 搜泛词，例如 `error`、`fail`、`debug`、`log`。
   - 必要时启动子 agent 做只读候选筛选。

## `search_text` 使用规则

只有在以下情况才考虑主会话使用 `search_text`：

- 已经有明确 `pattern`；
- 设置 `limit <= 30`；
- 能指定 `start` 时指定；
- 能限制 `include` 时限制为 `disasm` 或 `comments`；
- 能限制代码段时使用 `code_only: true`。

示例：

```json
{
  "pattern": "specific_token",
  "include": "disasm",
  "code_only": true,
  "limit": 30
}
```

避免：

```json
{
  "pattern": "error|fail|debug|log",
  "regex": true
}
```

## 宽搜索中断后的降级流程

1. 不重试原始宽搜索。
2. 记录已经知道的地址、字符串、函数名或最后一个可靠线索。
3. 如果有地址：
   - `lookup_funcs` 确认所属函数；
   - `disasm` 限制 `max_instructions <= 120`；
   - 必要时单函数 `decompile`。
4. 如果只有关键词：
   - 改用 `find_regex` / `imports_query` / `func_query`。
5. 如果候选仍然很多：
   - 启动子 agent，只读筛选；
   - 主会话只接收最多 10 个候选摘要。

## 防漏检原则

- `limit` / `count` 是保护上下文的默认上限，不代表搜索完整。
- 如果候选质量低、结论低置信度或结果显示 truncated，应分页继续搜索或交给子 agent 扩展。
- 关键结论至少用两类证据验证，例如字符串 xref + 调用关系，或字段访问 + 返回路径。

## 子 agent 返回格式

```text
目标：<搜索目标>
搜索方式：<find_regex/imports_query/xref/search_text 等>
候选：
1. <addr/function> — <触发依据> — <为什么相关/可能误报> — 置信度：高/中/低
下一步建议：
- 主会话优先精读 <1-3 个地址>
限制：
- 未返回完整 tool output
- 未返回完整 decompile/disasm/xref 列表
```

## 可扩展记录模板

新增搜索经验时追加到本节：

```text
场景：<例如搜索某类注册函数>
不要：<容易过宽或误导的做法>
改用：<更窄的 tool 和参数>
主会话保留：<最多哪些信息>
子 agent 负责：<候选筛选标准>
```
