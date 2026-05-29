# IDA MCP tool routing

本文件只在需要判断具体 IDA MCP tool 的上下文风险和执行位置时读取。目标是按需路由：主会话保留精读和 IDB 修改，子 agent 隔离大结果探索。

## 路由总则

- 主会话：单地址、单函数、少量数据、最终结论、所有 IDB 修改；每轮最多 1 个重型 IDA MCP 调用。
- 子 agent：宽泛搜索、多函数/多范围候选筛选、调用图探索、大函数预读、批量综合分析。
- 子 agent 默认只读；除非用户明确授权，不得修改 IDB。
- 高风险 tool 的输出必须由子 agent 压缩为候选地址、证据、置信度、下一步。

## 低风险：可在主会话直接使用

| Tool | 用法 | 限制 |
|---|---|---|
| `lookup_funcs` | 按已知地址/名称确认函数 | 查询少量目标 |
| `get_string` | 读取已知字符串地址 | 少量地址 |
| `get_int` / `int_convert` | 读取或转换数值 | 优先用工具，不手算复杂进制 |
| `get_bytes` | 验证少量字节 | 控制 size |
| `get_global_value` | 读取少量全局值 | 少量目标 |
| `stack_frame` | 查看单函数栈帧 | 仅已知函数 |
| `read_struct` | 读取一个已知结构实例 | 少量地址 |

## 中风险：主会话可用，但必须限量

| Tool | 主会话限制 | 何时改子 agent |
|---|---|---|
| `decompile` | 一次 1 个已明确相关函数 | 多函数预读、大函数未知语义 |
| `disasm` | `max_instructions <= 120`，按 offset 分页 | 需要完整函数汇编或多函数汇编 |
| `xrefs_to` / `xref_query` | `count <= 50`，目标明确 | 引用很多、需要筛选候选 |
| `xrefs_to_field` | 单字段、小范围 | 字段引用很多或结构未知 |
| `basic_blocks` | 限制 `max_blocks`，只看已确认函数 | CFG 很大或需要路径筛选 |
| `callees` | 单函数调用列表 | 多层调用链探索 |
| `type_inspect` | 已知类型名 | 类型枚举或关系探索 |

## 高风险：默认子 agent

| Tool / 资源 | 风险 | 子 agent 输出要求 |
|---|---|---|
| `analyze_batch` | 聚合反编译、xref、字符串、常量、CFG，极易膨胀 | 只返回候选和摘要 |
| `analyze_component` | 多函数组件分析，结果大 | 返回组件角色和关键函数 |
| 大范围 `analyze_function` | 可能包含太多细节 | 摘要，不贴完整伪代码 |
| `callgraph` | 节点/边爆炸 | `max_depth <= 2` 起步，返回关键边 |
| `list_funcs` / `list_globals` / `imports` | 枚举型结果 | 返回匹配候选，不返回完整列表 |
| `find_regex` / `find_bytes` / `find` / `search_text` | 搜索结果可能很多；`search_text` 会扫描渲染 listing，尤其容易过宽 | `limit <= 50`，优先用结构化搜索；`search_text` 不作为第一步全局扫描；多范围搜索默认子 agent 串行执行，必要时先读 `search-narrowing.md` / `mcp-stability.md` |
| `type_query` / `search_structs` | 类型/结构枚举可能很大 | 返回候选类型和判断依据 |
| `ida://types` / `ida://structs` | 资源 dump 大 | 避免主会话直接读 |
| 多函数 `decompile` / `disasm` | 直接撑大上下文 | 子 agent 摘要后主会话精读单点 |

## 修改类 tool：必须主会话确认

以下 tool 会改变 IDB 或二进制视图，默认不得交给子 agent：

- `rename`
- `set_type` / `type_apply_batch`
- `set_comments` / `append_comments`
- `patch` / `patch_asm` / `put_int`
- `define_func` / `define_code` / `undefine`
- `declare_type` / `declare_stack` / `delete_stack`
- `idb_save` / `idalib_save`

执行前必须确认：目标地址、修改内容、为什么确定、是否需要保存 IDB。
